from lsst.ts.statemachine.states import (EnabledState, DisabledState, StandbyState,
                                         FaultState, OfflineState, DefaultState)
from lsst.ts.statemachine.context import Context
from salpytools import salpylib
from threading import Event
import logging


__all__ = ['SimpleCSC', 'SimpleModel']


class SimpleModel:
    def __init__(self, subsystem_tag):
        self.log = logging.getLogger(type(self).__name__)
        self._dds = salpylib.DDSSend(subsystem_tag)
        self._ss_dict = {"OFFLINE": 5, "STANDBY": 4, "DISABLED": 1, "ENABLED": 2, "FAULT": 3, "MOVING": 6}
        self.state = "OFFLINE"
        self.previous_state = None
        self.status = None
        self.frequency = 0.05
        self.position = None
        self.status = None

    def change_state(self, state, cmd_id):
        self.log.debug('Changing state: %s -> %s', self.state, state)
        self.previous_state = self.state
        self.state = state
        self._dds.send_Event('SummaryState', summaryState=self._ss_dict[state])
        self.log.debug('New state: %s', self.state)


class SimpleCSC:
    def __init__(self, subsystem_tag, device_id=None):
        self.log = logging.getLogger(type(self).__name__)
        self.subsystem_tag = subsystem_tag
        self.device_id = device_id
        self.model = SimpleModel(self.subsystem_tag)

        self.states = {"OFFLINE": OfflineState(self.subsystem_tag), "STANDBY": StandbyState(self.subsystem_tag),
                       "DISABLED": DisabledState(self.subsystem_tag), "ENABLED": EnabledState(self.subsystem_tag),
                       "FAULT": FaultState(self.subsystem_tag)}

        self.context = Context(subsystem_tag=self.subsystem_tag, model=self.model, states=self.states)

        self.entercontrol = salpylib.DDSController(context=self.context, command='enterControl',
                                                   device_id=self.device_id)
        self.start = salpylib.DDSController(context=self.context, command='start',
                                            device_id=self.device_id)
        self.enable = salpylib.DDSController(context=self.context, command='enable',
                                             device_id=self.device_id)
        self.disable = salpylib.DDSController(context=self.context, command='disable',
                                              device_id=self.device_id)
        self.exitcontrol = salpylib.DDSController(context=self.context, command='exitControl',
                                                  device_id=self.device_id)

    def run(self):

        # start all controller threads
        self.entercontrol.start()
        self.start.start()
        self.enable.start()
        self.disable.start()
        self.exitcontrol.start()

    def stop(self, signum, frame):

        self.log.info('Received %s signal [%s]', signum, frame)

        self.log.debug('Stopping enter control...')
        self.entercontrol.stop()
        self.log.debug('Stopping start...')
        self.start.stop()
        self.log.debug('Stopping enable...')
        self.enable.stop()
        self.log.debug('Stopping disable...')
        self.disable.stop()
        self.log.debug('Stopping exit control...')
        self.exitcontrol.stop()

        self.log.debug('Waiting threads to finish...')
        self.entercontrol.join()
        self.start.join()
        self.enable.join()
        self.disable.join()
        self.exitcontrol.join()
        self.log.debug('Done')

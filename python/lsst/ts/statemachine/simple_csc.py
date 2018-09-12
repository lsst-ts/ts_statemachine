from lsst.ts.statemachine.states import (EnabledState, DisabledState, StandbyState,
                                         FaultState, OfflineState)
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

    def change_state(self, state):
        self.log.debug('Changing state: %s -> %s', self.state, state)
        self.previous_state = self.state
        self.state = state
        self._dds.send_Event('summaryState', summaryState=self._ss_dict[state])
        self.log.debug('New state: %s', self.state)

    def send_valid_settings(self):
        self.log.debug('Sending valid settings')


class SimpleOfflineState(OfflineState):
    def __init__(self, subsystem_tag, tsleep=0.5):
        super(SimpleOfflineState, self).__init__(subsystem_tag, tsleep)

    def enter_control(self, model):
        model.change_state("STANDBY")
        return 0, 'Done : OK'


class SimpleStandbyState(StandbyState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(SimpleStandbyState, self).__init__(subsystem_tag, tsleep)

    def exit_control(self, model):
        model.change_state("OFFLINE")
        return 0, 'Done : OK'

    def start(self, model):
        model.change_state("DISABLED")
        return 0, 'Done : OK'


class SimpleDisabledState(DisabledState):
    def __init__(self, subsystem_tag, tsleep=0.5):
        super(SimpleDisabledState, self).__init__(subsystem_tag, tsleep)

    def enable(self, model):
        model.change_state("ENABLED")
        return 0, 'Done : OK'

    def standby(self, model):
        model.change_state("STANDBY")
        return 0, 'Done : OK'


class SimpleEnabledState(EnabledState):
    def __init__(self, subsystem_tag, tsleep=0.5):
        super(SimpleEnabledState, self).__init__(subsystem_tag, tsleep)

    def disable(self, model):
        model.change_state("DISABLED")
        return 0, 'Done : OK'


class SimpleFaultState(FaultState):
    def __init__(self, subsystem_tag, tsleep=0.5):
        super(SimpleFaultState, self).__init__(subsystem_tag, tsleep)

    def exit_control(self, model):
        model.change_state("OFFLINE")
        return 0, 'Done : OK'


class SimpleCSC:
    def __init__(self, subsystem_tag, device_id=None):
        self.log = logging.getLogger(type(self).__name__)
        self.subsystem_tag = subsystem_tag
        self.device_id = device_id
        self.model = SimpleModel(self.subsystem_tag)

        self.states = {"OFFLINE": SimpleOfflineState(self.subsystem_tag),
                       "STANDBY": SimpleStandbyState(self.subsystem_tag),
                       "DISABLED": SimpleDisabledState(self.subsystem_tag),
                       "ENABLED": SimpleEnabledState(self.subsystem_tag),
                       "FAULT": SimpleFaultState(self.subsystem_tag)}

        self.context = Context(subsystem_tag=self.subsystem_tag, model=self.model, states=self.states)

        self.entercontrol = salpylib.DDSController(context=self.context, command='enterControl',
                                                   device_id=self.device_id)
        self.start = salpylib.DDSController(context=self.context, command='start',
                                            device_id=self.device_id)
        self.standby = salpylib.DDSController(context=self.context, command='standby',
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
        self.standby.start()
        self.enable.start()
        self.disable.start()
        self.exitcontrol.start()

        self.model.change_state('OFFLINE')

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
        self.log.debug('Stopping standby...')
        self.standby.stop()

        self.log.debug('Waiting threads to finish...')
        self.entercontrol.join()
        self.start.join()
        self.enable.join()
        self.disable.join()
        self.exitcontrol.join()
        self.standby.join()
        self.log.debug('Done')

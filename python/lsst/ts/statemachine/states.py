import time
import logging
import inspect
from lsst.ts.statemachine import StateTransitionException, SummaryState

class DefaultState:

    def __init__(self, name, subsystem_tag, tsleep=0.5):
        self.name = name
        self.subsystem_tag = subsystem_tag
        self.tsleep = tsleep
        self.log = logging.getLogger(self.name)

    #<----- Default State methods corresponding to UML design under here ------>

    def disable(self, model):
        raise StateTransitionException()

    def enable(self, model):
        raise StateTransitionException()

    def exit_control(self, model):
        raise StateTransitionException()

    def standby(self, model):
        raise StateTransitionException()

    def start(self, model):
        raise StateTransitionException()

    def enter_control(self, model):
        raise StateTransitionException()

    def exit(self, model):
        self.log.debug("Default: exit() not implemented")

    def do(self, model):
        self.log.debug("Default: do() not implemented")



class OfflineState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(OfflineState, self).__init__('OFFLINE', subsystem_tag, tsleep)

    def enter_control(self, model):
        model.state = "STANDBY"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["STANDBY"])

    def exit(self, model):
        self.log.debug("Offline: exit() not implemented")

    def do(self, model):
        self.log.debug("Offline: do() not implemented")


class StandbyState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(StandbyState, self).__init__('STANDBY', subsystem_tag, tsleep)

    def exit_control(self, model):
        model.state = "OFFLINE"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["OFFLINE"])

    def start(self, model):
        model.state = "DISABLED"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["DISABLED"])

    def exit(self, model):
        self.log.debug("Standby: exit() not implemented")

    def do(self, model):
        self.log.debug("Standby: do() not implemented")

    def on_heartbeat(self, model):
        pass

class DisabledState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(DisabledState, self).__init__('DISABLED', subsystem_tag, tsleep)

    def enable(self, model):
        model.state = "ENABLED"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["ENABLED"])

    def standby(self, model):
        model.state = "STANDBY"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["STANDBY"])

    def exit(self, model):
        self.log.debug("Disabled: exit() not implemented")

    def do(self, model):
        self.log.debug("Disabled: do() not implemented")

    def on_heartbeat(self, model):
        pass

    def on_incoming_messaging_error(self, model):
        pass

    def on_interrupt_end_loop(self, model):
        pass

    def on_interrupt_process_triggers(self, model):
        pass

class EnabledState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(EnabledState, self).__init__('ENABLED', subsystem_tag, tsleep)

    def disable(self, model):
        model.state = "DISABLED"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["DISABLED"])

    def exit(self, model):
        self.log.debug("Enabled: exit() not implemented")

    def do(self, model):
        self.log.debug("Enabled: do() not implemented")

    def on_hearbeat(self, model):
        pass

    def on_incoming_messaging_error(self, model):
        pass

    def on_interrupt_end_loop(self, model):
        pass

    def on_interrupt_process_triggers(self, model):
        pass

class FaultState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(FaultState, self).__init__('FAULT', subsystem_tag, tsleep)

    def go_to_standby(self, model):
        model.state = "STANDBY"
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["STANDBY"])

    def on_heartbeat(self, model):
        pass

    def on_incoming_messaging_error(self, model):
        pass

    def on_interrupt_end_loop(self, model):
        pass

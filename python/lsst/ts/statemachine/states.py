import logging
from lsst.ts.statemachine import StateTransitionException, SummaryState

class DefaultState:

    def __init__(self, name, subsystem_tag, tsleep=0.5):
        self.name = name
        self.subsystem_tag = subsystem_tag
        self.tsleep = tsleep
        self.data = None
        self.log = logging.getLogger(self.name)

    # <----- Default State methods corresponding to UML design under here ------>

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
        pass

    def do(self, model):
        pass


class OfflineState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(OfflineState, self).__init__('OFFLINE', subsystem_tag, tsleep)

    def enter_control(self, model):
        model.state = "STANDBY"
        return 0, 'Done : OK'
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["STANDBY"])

    def exit(self, model):
        pass

    def do(self, model):
        pass


class StandbyState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(StandbyState, self).__init__('STANDBY', subsystem_tag, tsleep)

    def exit_control(self, model):
        model.state = "OFFLINE"
        return 0, 'Done : OK'
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["OFFLINE"])

    def start(self, model):
        model.state = "DISABLED"
        return 0, 'Done : OK'
        # TODO model.send_summary_state(SUMMARY_STATE_ENUM["DISABLED"])

    def exit(self, model):
        pass

    def do(self, model):
        if model.previous_state == "OFFLINE":
            model.send_valid_settings()

    def on_heartbeat(self, model):
        pass


class DisabledState(DefaultState):

    def __init__(self, subsystem_tag, tsleep=0.5):
        super(DisabledState, self).__init__('DISABLED', subsystem_tag, tsleep)

    def enable(self, model):
        model.state = "ENABLED"
        return 0, 'Done : OK'

    def standby(self, model):
        model.state = "STANDBY"
        return 0, 'Done : OK'

    def exit(self, model):
        pass

    def do(self, model):
        pass

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
        return 0, 'Done : OK'

    def exit(self, model):
        pass

    def do(self, model):
        pass

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

    def exit_control(self, model):
        model.state = "OFFLINE"
        return 0, 'Done : OK'

    def on_heartbeat(self, model):
        pass

    def on_incoming_messaging_error(self, model):
        pass

    def on_interrupt_end_loop(self, model):
        pass

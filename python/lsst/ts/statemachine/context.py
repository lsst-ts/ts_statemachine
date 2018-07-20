from lsst.ts.statemachine import (OfflineState, StandbyState, DisabledState,
                                  EnabledState, FaultState,
                                  CommandNotRecognizedException)

class Context:
    """The Context orchestrates triggers from the states to the model.

    The context is where we interact with our defined states. All calls to our
    statemachine, begin by calling that method onto the Context class.
    When creating DDSControllers a Context is passed into it. When the
    DDSController recieves commands it delegates these actions to the Context.
    The context then delegates this to the active State.

    Attributes:
        subsystem_tag: A string of the name of the CSC we want. Must exactly
        match the Subsystem Tag defined in XML. Link to current Subsystem Tags
        https://stash.lsstcorp.org/projects/TS/repos/ts_xml/browse/sal_interfaces
        default_state: default state defined within states.py of this library.
        tsleep: A sleeper to prevent race conditions when sending log events.
        states: List of states this context will contain. In general use, these
        should be subclassed states with overriden behavior.
    """
    def __init__(self, subsystem_tag, model, default_state='OFFLINE', tsleep=0.5,
                 states=None):

        self.subsystem_tag = subsystem_tag
        self.model = model
        self.current_state = default_state
        self.tsleep = tsleep
        if states is not None:
            self.states = states
        else:
            # Loading default states
            self.states = dict()
            self.states["OFFLINE"] = OfflineState(self.subsystem_tag)
            self.states["STANDBY"] = StandbyState(self.subsystem_tag)
            self.states["DISABLED"] = DisabledState(self.subsystem_tag)
            self.states["ENABLED"] = EnabledState(self.subsystem_tag)
            self.states["FAULT"] = FaultState(self.subsystem_tag)
            self.states["INITIAL"] = self.states["OFFLINE"]
            self.states["FINAL"] = self.states["OFFLINE"]

        # Useful debug logging
        # self.log = create_logger(level=logging.NOTSET, name=self.subsystem_tag)
        # self.log.debug('{} Init beginning'.format(self.subsystem_tag))
        # self.log.debug('Starting with default state: {}'.format(default_state))


    def execute_command(self, command):
        """This method delegates commands recieved by a DDSController to the
        state.

        The model is passed so that the State object may call methods on
        it. Also the state is stored on the model only as a string
        representation. The actual state object is stored on this context
        object as self.states.

        Attributes:
            command: A string representation of the command recieved by a
            DDSController object.
        """

        if command == "ENTERCONTROL":

            # Get the current state
            current_state = self.states[self.model.state]
            # Call exit methods, killing threads perhaps
            current_state.exit(self.model)
            # Call our "change state" method
            current_state.enter_control(self.model)
            # Since the state we changed to is implementer decided, we re-get it
            current_state = self.states[self.model.state]
            # Call the do methods on the state we just entered, starting threads perhaps
            current_state.do(self.model)

        elif command == "START":
            current_state = self.states[self.model.state]
            current_state.exit(self.model)
            current_state.start(self.model)
            current_state = self.states[self.model.state]
            current_state.do(self.model)

        elif command == "ENABLE":
            current_state = self.states[self.model.state]
            current_state.exit(self.model)
            current_state.enable(self.model)
            current_state = self.states[self.model.state]
            current_state.do(self.model)

        elif command == "DISABLE":
            current_state = self.states[self.model.state]
            current_state.exit(self.model)
            current_state.disable(self.model)
            current_state = self.states[self.model.state]
            current_state.do(self.model)

        elif command == "STANDBY":
            current_state = self.states[self.model.state]
            current_state.exit(self.model)
            current_state.standby(self.model)
            current_state = self.states[self.model.state]
            current_state.do(self.model)

        elif command == "EXITCONTROL":
            current_state = self.states[self.model.state]
            current_state.exit(self.model)
            current_state.exit_control(self.model)
            current_state = self.states[self.model.state]
            current_state.do(self.model)

        else:
            raise CommandNotRecognizedException()

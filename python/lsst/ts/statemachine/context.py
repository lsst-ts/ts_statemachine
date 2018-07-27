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

        self._command_list = {'ENTERCONTROL': 'enter_control',
                              'START': 'start',
                              'ENABLE': 'enable',
                              'DISABLE': 'disable',
                              'STANDBY': 'standby',
                              'EXITCONTROL': 'exit_control'}

    def execute_command(self, command, data):
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

        if command in self._command_list:
            # Get the current state
            current_state = self.states[self.model.state]
            # Call exit methods, killing threads perhaps
            current_state.exit(self.model)
            # Call our "change state" method dynamically
            current_state.data = data
            err, msg = getattr(current_state, self._command_list[command])(self.model)
            # Since the state we changed to is implementer decided, we re-get it
            current_state = self.states[self.model.state]
            # Call the do methods on the state we just entered, starting threads perhaps
            current_state.do(self.model)
            return err, msg
        else:
            raise CommandNotRecognizedException()

    def add_command(self, name, method=None):
        '''
        Add a command to the list of valid commands.

        :param name: The name of the command.
        :param method: The method associated with that command.
        :return:
        '''

        uname = name.upper()

        if uname in self._command_list:
            raise IOError('{} already in the command list.'.format(name))
        elif method is None:
            self._command_list[uname] = name
        else:
            self._command_list[uname] = method

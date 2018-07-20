<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<tagfile>
  <compound kind="class">
    <name>lsst::ts::statemachine::context::Context</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1context_1_1Context.html</filename>
    <member kind="function">
      <type>def</type>
      <name>send_logEvent</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1context_1_1Context.html</anchorfile>
      <anchor>a91cdce51db2d88e255d1f0d7a5d97595</anchor>
      <arglist>(self, eventname, kwargs)</arglist>
    </member>
    <member kind="function">
      <type>def</type>
      <name>subscribe_logEvent</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1context_1_1Context.html</anchorfile>
      <anchor>a53016ff56ba4b0ab0b8bd74159041661</anchor>
      <arglist>(self, eventname)</arglist>
    </member>
    <member kind="function">
      <type>def</type>
      <name>get_current_state</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1context_1_1Context.html</anchorfile>
      <anchor>a109135ca1424a0e49a3e31e9f7668814</anchor>
      <arglist>(self)</arglist>
    </member>
    <member kind="function">
      <type>def</type>
      <name>execute_command</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1context_1_1Context.html</anchorfile>
      <anchor>a187d66ab944b7764e09b885889171f6d</anchor>
      <arglist>(self, command)</arglist>
    </member>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::DefaultState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1DefaultState.html</filename>
    <member kind="function">
      <type>def</type>
      <name>subscribe_logEvent</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1states_1_1DefaultState.html</anchorfile>
      <anchor>a4f2c32b6740624d72e1c49ac0987440e</anchor>
      <arglist>(self, eventname)</arglist>
    </member>
    <member kind="function">
      <type>def</type>
      <name>send_logEvent</name>
      <anchorfile>classlsst_1_1ts_1_1statemachine_1_1states_1_1DefaultState.html</anchorfile>
      <anchor>a302142c353918f82bbc7db0a132a71ce</anchor>
      <arglist>(self, eventname, kwargs)</arglist>
    </member>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::DisabledState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1DisabledState.html</filename>
    <base>lsst::ts::statemachine::states::DefaultState</base>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::EnabledState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1EnabledState.html</filename>
    <base>lsst::ts::statemachine::states::DefaultState</base>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::FaultState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1FaultState.html</filename>
    <base>lsst::ts::statemachine::states::DefaultState</base>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::OfflineState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1OfflineState.html</filename>
    <base>lsst::ts::statemachine::states::DefaultState</base>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::states::StandbyState</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1states_1_1StandbyState.html</filename>
    <base>lsst::ts::statemachine::states::DefaultState</base>
  </compound>
  <compound kind="class">
    <name>lsst::ts::statemachine::state_transition_exception::StateTransitionException</name>
    <filename>classlsst_1_1ts_1_1statemachine_1_1state__transition__exception_1_1StateTransitionException.html</filename>
  </compound>
  <compound kind="namespace">
    <name>lsst::ts::statemachine::states</name>
    <filename>namespacelsst_1_1ts_1_1statemachine_1_1states.html</filename>
    <class kind="class">lsst::ts::statemachine::states::DefaultState</class>
    <class kind="class">lsst::ts::statemachine::states::DisabledState</class>
    <class kind="class">lsst::ts::statemachine::states::EnabledState</class>
    <class kind="class">lsst::ts::statemachine::states::FaultState</class>
    <class kind="class">lsst::ts::statemachine::states::OfflineState</class>
    <class kind="class">lsst::ts::statemachine::states::StandbyState</class>
  </compound>
</tagfile>

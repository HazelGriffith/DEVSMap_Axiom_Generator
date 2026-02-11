
%-----DEVS TFF TYPES

tff(internal_transition_type,type,internal_transition : $o).

tff(external_transition_type,type,external_transition : $o).

tff(confluence_transition_type,type,confluence_transition : $o).

tff(output_type,type,output : $o).

tff(time_advance_type,type,time_advance : $real).

tff(time_passed_type,type,time_passed : $real).

tff(infinity_type,type,infinity : $real).

tff(input_rcvd_type,type,input_rcvd: $o).


%-----STATE VARIABLE DEFINITIONS

tff(state_type,type,(state : $real)).

tff(next_state_type,type,(next_state : $real)).

tff(sigma_type,type,(sigma : $real)).

tff(next_sigma_type,type,(next_sigma : $real)).

tff(aircraft_velocity_type,type,(aircraft_velocity : $real)).

tff(next_aircraft_velocity_type,type,(next_aircraft_velocity : $real)).


%-----INPUT PORT DEFINITIONS

tff(i_port_type,type,(i_port : $tType)).

tff(num_rcvd_type,type,(num_rcvd : i_port > $int)).

tff(pilot_takeover_type,type,(pilot_takeover : i_port)).

tff(val_rcvd_pilot_takeover_type,type,(val_rcvd_pilot_takeover : $o)).

tff(pilot_handover_type,type,(pilot_handover : i_port)).

tff(val_rcvd_pilot_handover_type,type,(val_rcvd_pilot_handover : $o)).

tff(request_reposition_type,type,(request_reposition : i_port)).

tff(val_rcvd_request_reposition_type,type,(val_rcvd_request_reposition : $o)).

tff(aircraft_state_type,type,(aircraft_state : i_port)).

tff(val_rcvd_aircraft_state_type,type,(val_rcvd_aircraft_state : $real)).

tff(hover_criteria_met_type,type,(hover_criteria_met : i_port)).

tff(val_rcvd_hover_criteria_met_type,type,(val_rcvd_hover_criteria_met : $o)).

tff(start_mission_type,type,(start_mission : i_port)).

tff(val_rcvd_start_mission_type,type,(val_rcvd_start_mission : $o)).

tff(only_i_ports,axiom,(
	! [IP : i_port] : (((((
		(IP = pilot_takeover) | 
		(IP = pilot_handover)) | 
		(IP = request_reposition)) | 
		(IP = aircraft_state)) | 
		(IP = hover_criteria_met)) | 
		(IP = start_mission)))).

tff(i_ports_are_distinct,axiom,
	$distinct(pilot_takeover,pilot_handover,request_reposition,aircraft_state,hover_criteria_met,start_mission)).

tff(always_pos_num_rcvd,axiom,
	! [IP : i_port] :
		$greatereq(num_rcvd(IP),0)).


%-----OUTPUT PORT DEFINITIONS

tff(o_port_type,type,(o_port : $tType)).

tff(num_output_type,type,(num_output : o_port > $int)).

tff(cancel_hover_type,type,(cancel_hover : o_port)).

tff(val_output_cancel_hover_type,type,(val_output_cancel_hover : $o)).

tff(fcc_command_velocity_type,type,(fcc_command_velocity : o_port)).

tff(val_output_fcc_command_velocity_type,type,(val_output_fcc_command_velocity : $real)).

tff(stabilize_type,type,(stabilize : o_port)).

tff(val_output_stabilize_type,type,(val_output_stabilize : $o)).

tff(lp_criteria_met_type,type,(lp_criteria_met : o_port)).

tff(val_output_lp_criteria_met_type,type,(val_output_lp_criteria_met : $o)).

tff(request_aircraft_state_type,type,(request_aircraft_state : o_port)).

tff(val_output_request_aircraft_state_type,type,(val_output_request_aircraft_state : $o)).

tff(update_boss_type,type,(update_boss : o_port)).

tff(val_output_update_boss_type,type,(val_output_update_boss : $o)).

tff(update_gcs_type,type,(update_gcs : o_port)).

tff(val_output_update_gcs_type,type,(val_output_update_gcs : $o)).

tff(set_mission_monitor_status_type,type,(set_mission_monitor_status : o_port)).

tff(val_output_set_mission_monitor_status_type,type,(val_output_set_mission_monitor_status : $o)).

tff(only_o_ports,axiom,(
	! [OP : o_port] : (((((((
		(OP = cancel_hover) | 
		(OP = fcc_command_velocity)) | 
		(OP = stabilize)) | 
		(OP = lp_criteria_met)) | 
		(OP = request_aircraft_state)) | 
		(OP = update_boss)) | 
		(OP = update_gcs)) | 
		(OP = set_mission_monitor_status)))).

tff(o_ports_are_distinct,axiom,
	$distinct(cancel_hover,fcc_command_velocity,stabilize,lp_criteria_met,request_aircraft_state,update_boss,update_gcs,set_mission_monitor_status)).


%-----INTERNAL TRANSITION FUNCTION AXIOMS

tff(delta_int_axiom_0,axiom,(((
		(internal_transition = $true) & 
		(state = 3.0)) => (
		(next_state = 4.0) & 
		(next_sigma = infinity))))).

tff(delta_int_axiom_1,axiom,(((
		(internal_transition = $true) & 
		(state = 5.0)) => (
		(next_state = 6.0) & 
		(next_sigma = 0.0))))).

tff(delta_int_axiom_2,axiom,(((
		(internal_transition = $true) & 
		(state = 6.0)) => (
		(next_state = 7.0) & 
		(next_sigma = infinity))))).

tff(delta_int_axiom_3,axiom,(((
		(internal_transition = $true) & 
		(state = 8.0)) => (
		(next_state = 9.0) & 
		(next_sigma = infinity))))).

tff(delta_int_axiom_4,axiom,(((
		(internal_transition = $true) & 
		(state = 10.0)) => (
		(next_state = 3.0) & 
		(next_sigma = infinity))))).

tff(delta_int_axiom_5,axiom,(((((((
		~(state = 3.0) & 
		~(state = 5.0)) & 
		~(state = 6.0)) & 
		~(state = 8.0)) & 
		~(state = 10.0)) & 
		(internal_transition = $true)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).


%-----EXTERNAL TRANSITION FUNCTION AXIOMS

tff(delta_ext_axiom_0,axiom,(((
		(external_transition = $true) & 
		(num_rcvd(pilot_takeover) != 0)) => (
		(next_state = 12.0) & 
		(next_sigma = infinity))))).

tff(delta_ext_axiom_1,axiom,(((
		(external_transition = $true) & 
		(num_rcvd(pilot_handover) != 0)) => (
		(next_state = 11.0) & 
		(next_sigma = infinity))))).

tff(delta_ext_axiom_2,axiom,(((
		(external_transition = $true) & 
		(num_rcvd(start_mission) != 0)) => (
		(next_state = 2.0) & 
		(next_sigma = infinity))))).

tff(delta_ext_axiom_3,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 2.0)) & 
		(num_rcvd(request_reposition) != 0)) => (
		(next_state = 3.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_4,axiom,(((((((
		~(num_rcvd(request_reposition) != 0) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 2.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_5,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 4.0)) & 
		(num_rcvd(aircraft_state) != 0)) => (
		(next_state = 5.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_6,axiom,(((((((
		~(num_rcvd(aircraft_state) != 0) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 4.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_7,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 5.0)) & 
		(num_rcvd(request_reposition) != 0)) => (
		(next_state = 3.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_8,axiom,(((((((
		~(num_rcvd(request_reposition) != 0) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 5.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_9,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 6.0)) & 
		(num_rcvd(request_reposition) != 0)) => (
		(next_state = 3.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_10,axiom,(((((((
		~(num_rcvd(request_reposition) != 0) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 6.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_11,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 7.0)) & 
		(num_rcvd(hover_criteria_met) != 0)) => (
		(next_state = 8.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_12,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 7.0)) & 
		(num_rcvd(request_reposition) != 0)) => (
		(next_state = 10.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_13,axiom,((((((((
		~(num_rcvd(hover_criteria_met) != 0) & 
		~(num_rcvd(request_reposition) != 0)) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 7.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_14,axiom,(((((((
		~(num_rcvd(pilot_takeover) != 0) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 8.0)) & 
		(num_rcvd(request_reposition) != 0)) => (
		(next_state = 10.0) & 
		(next_sigma = 0.0))))).

tff(delta_ext_axiom_15,axiom,(((((((
		~(num_rcvd(request_reposition) != 0) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) & 
		(state = 8.0)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).

tff(delta_ext_axiom_16,axiom,(((((((((((
		~(state = 2.0) & 
		~(state = 4.0)) & 
		~(state = 5.0)) & 
		~(state = 6.0)) & 
		~(state = 7.0)) & 
		~(state = 8.0)) & 
		~(num_rcvd(pilot_takeover) != 0)) & 
		~(num_rcvd(pilot_handover) != 0)) & 
		~(num_rcvd(start_mission) != 0)) & 
		(external_transition = $true)) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).


%-----CONFLUENCE TRANSITION FUNCTION AXIOMS

tff(delta_con_axiom_0,axiom,((
		(confluence_transition = $true) => ((
		(next_state = state) & 
		(next_sigma = sigma)) & 
		(next_aircraft_velocity = aircraft_velocity))))).


%-----LAMBDA AXIOMS

tff(lambda_axiom_0,axiom,(((
		(output = $true) & 
		(state = 3.0)) => 
		(val_output_request_aircraft_state = $true)))).

tff(lambda_axiom_1,axiom,(((
		(output = $true) & 
		(state = 5.0)) => 
		(val_output_fcc_command_velocity = aircraft_velocity)))).

tff(lambda_axiom_2,axiom,(((
		(output = $true) & 
		(state = 6.0)) => (((
		(val_output_stabilize = $true) & 
		(val_output_set_mission_monitor_status = $true)) & 
		(val_output_update_boss = $true)) & 
		(val_output_update_gcs = $true))))).

tff(lambda_axiom_3,axiom,(((
		(output = $true) & 
		(state = 8.0)) => 
		(val_output_lp_criteria_met = $true)))).

tff(lambda_axiom_4,axiom,(((
		(output = $true) & 
		(state = 10.0)) => 
		(val_output_cancel_hover = $true)))).


%-----TIME ADVANCE AXIOMS

tff(ta_axiom_0,axiom,(
		(time_advance = sigma))).


%-----DEVS TFF AXIOMS

tff(input_was_rcvd,axiom,
	? [IP : i_port] :
		num_rcvd(IP) != 0 => input_rcvd = $true).

tff(input_not_rcvd,axiom,
	! [IP : i_port] :
		num_rcvd(IP) = 0 => input_rcvd = $false).

tff(internal_transition_occurred,axiom,
	((($greatereq(time_passed,time_advance)) & 
		(~input_rcvd)) => (
		(internal_transition = $true) &
		(external_transition = $false) &
		(confluence_transition = $false) &
		(output = $true)))).

tff(external_transition_occurred,axiom,
	((($less(time_passed,time_advance)) & 
		(input_rcvd)) => (
		(internal_transition = $false) &
		(external_transition = $true) &
		(confluence_transition = $false) &
		(output = $false)))).

tff(confluence_transition_occurred,axiom,
	((($greatereq(time_passed,time_advance)) & 
		(input_rcvd)) => (
		(internal_transition = $false) &
		(external_transition = $false) &
		(confluence_transition = $true) &
		(output = $true)))).

tff(infinity_is_greater,axiom,
	infinity = $sum(time_passed,1.0)).

tff(state_value,axiom,state = 7.0).

tff(sigma_value,axiom,sigma = infinity).

tff(aircraft_velocity_value,axiom,aircraft_velocity = 5.0).

tff(time_passed_value,axiom,time_passed = 543.0).

tff(rcvd_request_reposition,axiom,num_rcvd(request_reposition) = 1).

tff(rcvd_hover_criteria_met,axiom,num_rcvd(hover_criteria_met) = 1).

tff(nothing_rcvd_pilot_handover,axiom,num_rcvd(pilot_handover) = 0).

tff(nothing_rcvd_pilot_takeover,axiom,num_rcvd(pilot_takeover) = 0).

tff(nothing_rcvd_start_mission,axiom,num_rcvd(start_mission) = 0).

tff(nothing_rcvd_aircraft_state,axiom,num_rcvd(aircraft_state) = 0).

tff(next_state_value,conjecture,next_state = 10.0 & next_state = 8.0).


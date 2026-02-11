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
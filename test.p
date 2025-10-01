
%-----STATE VARIABLE DEFINITIONS
tff(count, type, $int).
tff(next_count, type, $int).
tff(increment, type, $int).
tff(next_increment, type, $int).
tff(countUp, type, $o).
tff(next_countUp, type, $o).
tff(sigma, type, $real).
tff(next_sigma, type, $real).

%-----INPUT PORT DEFINITIONS
tff(i_port_type, type, i_port : $tType).
tff(direction_in, type, direction_in : i_port).
tff(rcvd_direction_in, type, rcvd_direction_in : $o).
tff(increment_in, type, increment_in : i_port).
tff(rcvd_increment_in, type, rcvd_increment_in : $int).
tff(only_i_ports, axiom,
	! [IP : i_port] :
		( IP = direction_in | IP = increment_in)).


%-----OUTPUT PORT DEFINITIONS
tff(o_port_type, type, o_port : $tType).
tff(count_out, type, count_out : o_port).
tff(only_o_ports, axiom,
	! [OP : o_port] :
		( OP = count_out)).


%-----INTERNAL TRANSITIONS

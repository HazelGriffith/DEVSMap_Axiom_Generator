%-----STATE VARIABLE DEFINITIONS
tff(count,type,$int).
tff(next_count,type,$int$int).).
tff(increment,type,$int).
tff(next_increment,type,$int$int).).
tff(countUp,type,$o).
tff(next_countUp,type,$o$o).).
tff(countDown,type,$o).
tff(next_countDown,type,$o$o).).
tff(sigma,type,$real).
tff(next_sigma,type,$real$real).).
%-----INPUT PORT DEFINITIONS
tff(i_port_type,type,i_port : $tType).
tff(direction_in,type,direction_in : i_port).
tff(num_rcvd_direction_in,type,num_rcvd_direction_in : $int).
tff(val_rcvd_direction_in,type,val_rcvd_direction_in : $o).
tff(increment_in,type,increment_in : i_port).
tff(num_rcvd_increment_in,type,num_rcvd_increment_in : $int).
tff(val_rcvd_increment_in,type,val_rcvd_increment_in : $int).
tff(only_i_ports,axiom,! [IP : i_port]IP = direction_in | IP = increment_in).
%-----OUTPUT PORT DEFINITIONS
tff(o_port_type,type,o_port : $tType).
tff(count_out,type,count_out : o_port).
tff(only_o_ports,axiom,! [OP : o_port]OP = count_out).
%-----INTERNAL TRANSITION FUNCTION AXIOMS
tff(delta_int_axiom_0,axiom,countUp = true => next_count = $sum(count,increment) & next_increment = $product(sigma,4)).
tff(delta_int_axiom_1,axiom,countUp = false => next_count = $difference(count,increment)).
tff(delta_int_axiom_2,axiom,~(countUp = true) & ~(countUp = false) => next_count = count & next_increment = increment & next_countUp = countUp & next_countDown = countDown & next_sigma = sigma).
%-----INTERNAL TRANSITION FUNCTION AXIOMS
tff(delta_ext_axiom_0,axiom,direction_in_bagSize != 0 => next_countUp = irection_in_ba).
tff(delta_ext_axiom_1,axiom,increment_in_bagSize != 0 => next_increment = ncrement_in_ba).
tff(delta_ext_axiom_2,axiom,~(direction_in_bagSize != 0) & ~(increment_in_bagSize != 0) => next_countUp = irection_in_ba & next_increment = ncrement_in_ba).

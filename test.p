
%-----STATE VARIABLE DEFINITIONS

tff(count,type,$int).

tff(next_count,type,$int).

tff(increment,type,$int).

tff(next_increment,type,$int).

tff(countUp,type,$o).

tff(next_countUp,type,$o).

tff(sigma,type,$real).

tff(next_sigma,type,$real).


%-----INPUT PORT DEFINITIONS

tff(i_port_type,type,i_port : $tType).

tff(num_rcvd_type,type,num_rcvd : i_port > $int).

tff(direction_in,type,direction_in : i_port).

tff(val_rcvd_direction_in_type,type,val_rcvd_direction_in : $o).

tff(increment_in,type,increment_in : i_port).

tff(val_rcvd_increment_in_type,type,val_rcvd_increment_in : $int).

tff(only_i_ports,axiom,
	! [IP : i_port](
		(IP = direction_in) | 
		(IP = increment_in))).


%-----OUTPUT PORT DEFINITIONS

tff(o_port_type,type,o_port : $tType).

tff(num_output_type,type,num_output : o_port > $int).

tff(count_out,type,count_out : o_port).

tff(val_output_count_out_type,type,val_output_count_out : $int).

tff(only_o_ports,axiom,
	! [OP : o_port]
		(OP = count_out)).


%-----INTERNAL TRANSITION FUNCTION AXIOMS

tff(delta_int_axiom_0,axiom,(
		(countUp = $true) => (
		(next_count = 
		$sum(count,increment)) & 
		(next_increment = 
		$product(sigma,4))))).

tff(delta_int_axiom_1,axiom,(
		(countUp = $false) => 
		(next_count = 
		$difference(count,increment)))).

tff(delta_int_axiom_2,axiom,((
		~(countUp = $true) & 
		~(countUp = $false)) => (((
		(next_count = count) & 
		(next_increment = increment)) & 
		(next_countUp = countUp)) & 
		(next_sigma = sigma)))).


%-----EXTERNAL TRANSITION FUNCTION AXIOMS

tff(delta_ext_axiom_0,axiom,(
		(num_rcvd(direction_in) != 0) => 
		(next_countUp = val_rcvd_direction_in))).

tff(delta_ext_axiom_1,axiom,(
		(num_rcvd(increment_in) != 0) => 
		(next_increment = val_rcvd_increment_in))).

tff(delta_ext_axiom_2,axiom,((
		~(num_rcvd(direction_in) != 0) & 
		~(num_rcvd(increment_in) != 0)) => (
		(next_countUp = val_rcvd_direction_in) & 
		(next_increment = val_rcvd_increment_in)))).


%-----CONFLUENCE TRANSITION FUNCTION AXIOMS

tff(delta_con_axiom_0,axiom,((
		(num_rcvd(direction_in) != 0) & 
		(val_rcvd_direction_in = $true)) => (
		(next_count = 
		$sum(count,increment)) & 
		(next_countUp = val_rcvd_direction_in)))).

tff(delta_con_axiom_1,axiom,((
		(num_rcvd(direction_in) != 0) & 
		(val_rcvd_direction_in = $false)) => (
		(next_count = 
		$difference(count,increment)) & 
		(next_countUp = val_rcvd_direction_in)))).

tff(delta_con_axiom_2,axiom,((
		~(val_rcvd_direction_in = $true) & 
		~(val_rcvd_direction_in = $false)) => (((
		(next_count = count) & 
		(next_increment = increment)) & 
		(next_countUp = countUp)) & 
		(next_sigma = sigma)))).


%-----LAMBDA AXIOMS

tff(lambda_axiom_0,axiom,
		(val_output_count_out = count)).


%-----TIME ADVANCE AXIOMS

tff(ta_axiom_0,axiom,
		(time_advance = sigma)).


%-----DEVS TFF AXIOMS


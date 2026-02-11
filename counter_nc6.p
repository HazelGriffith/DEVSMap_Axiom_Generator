tff(count_value,axiom,count = 5.0).

tff(increment_value,axiom,increment = 1.0).

tff(countUp_value,axiom,countUp = $true).

tff(sigma_value,axiom,sigma = 5.0).

tff(time_passed_value,axiom,time_passed = 5.0).

tff(nothing_received,axiom,
	! [IP : i_port] :
		(num_rcvd(IP) = 0)).

tff(next_count_value,conjecture,next_count = 6.0).
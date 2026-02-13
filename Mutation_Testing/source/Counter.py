class Counter:
    def __init__(self, count, increment, countUp, sigma):
        self.count = count
        self.increment = increment
        self.countUp = countUp
        self.sigma = sigma

    def internal_transition(self):
        if self.countUp:
            self.count += self.increment
        else:
            self.count -= self.increment

    def external_transition(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def confluence_transition(self, x):
        self.external_transition(x, .0)
        self.internal_transition()

    def output(self) -> int:
        return self.count

    def time_advance(self) -> float:
        return self.sigma
    
    def equal(self, counter): # pragma: no mutate
        if ((self.count == counter.count) and # pragma: no mutate
            (self.increment == counter.increment) and # pragma: no mutate
            (self.countUp == counter.countUp) and # pragma: no mutate
            (self.sigma == counter.sigma)): # pragma: no mutate
            return True # pragma: no mutate
        else: # pragma: no mutate
            return False # pragma: no mutate
        
    def __str__(self): # pragma: no mutate
        return f"count: {self.count}, increment: {self.increment}, countUp: {self.countUp}, sigma: {self.sigma}" # pragma: no mutate

def transition(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed >= time_advance:
        if input == True:
            output = counter_model.output()
            counter_model.confluence_transition(x)
            time_adv2 = counter_model.time_advance()
        elif input == False:
            output = counter_model.output()
            counter_model.internal_transition()
            time_adv2 = counter_model.time_advance()
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def copy_counter(counter1) -> Counter: # pragma: no mutate
    return Counter(counter1.count, counter1.increment, counter1.countUp, counter1.sigma) # pragma: no mutate
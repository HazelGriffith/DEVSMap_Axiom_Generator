class Counter:
    def __init__(self, count:int, increment:int, countUp:bool, sigma:float):
        self.count = count
        self.increment = increment
        self.countUp = countUp
        self.sigma = sigma

    def internal_transition(self):
        if self.countUp:
            self.count += self.increment
        else:
            self.count -= self.increment

    def external_transition(self, x, e:float):
        direction_in = x.at("direction_in")
        increment_in = x.at("increment_in")
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

def transition(counter_model:Counter, time_passed:float, x) -> Counter:
    input = False
    for x_port in x:
        if len(x_port) > 0:
            input = True

    output = None
    time_adv1 = counter_model.sigma

    if time_passed >= time_adv1:
        if input:
            output = counter_model.output()
            counter_model.confluence_transition(x)
        else:
            output = counter_model.output()
            counter_model.internal_transition()
    else:
        if input:
            counter_model.external_transition(x, time_passed)
    
    time_adv2 = counter_model.time_advance()
    return output, time_adv2
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result
class Counter:
    def xǁCounterǁ__init____mutmut_orig(self, count, increment, countUp, sigma):
        self.count = count
        self.increment = increment
        self.countUp = countUp
        self.sigma = sigma
    def xǁCounterǁ__init____mutmut_1(self, count, increment, countUp, sigma):
        self.count = None
        self.increment = increment
        self.countUp = countUp
        self.sigma = sigma
    def xǁCounterǁ__init____mutmut_2(self, count, increment, countUp, sigma):
        self.count = count
        self.increment = None
        self.countUp = countUp
        self.sigma = sigma
    def xǁCounterǁ__init____mutmut_3(self, count, increment, countUp, sigma):
        self.count = count
        self.increment = increment
        self.countUp = None
        self.sigma = sigma
    def xǁCounterǁ__init____mutmut_4(self, count, increment, countUp, sigma):
        self.count = count
        self.increment = increment
        self.countUp = countUp
        self.sigma = None
    
    xǁCounterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCounterǁ__init____mutmut_1': xǁCounterǁ__init____mutmut_1, 
        'xǁCounterǁ__init____mutmut_2': xǁCounterǁ__init____mutmut_2, 
        'xǁCounterǁ__init____mutmut_3': xǁCounterǁ__init____mutmut_3, 
        'xǁCounterǁ__init____mutmut_4': xǁCounterǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCounterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCounterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁCounterǁ__init____mutmut_orig)
    xǁCounterǁ__init____mutmut_orig.__name__ = 'xǁCounterǁ__init__'

    def xǁCounterǁinternal_transition__mutmut_orig(self):
        if self.countUp:
            self.count += self.increment
        else:
            self.count -= self.increment

    def xǁCounterǁinternal_transition__mutmut_1(self):
        if self.countUp:
            self.count = self.increment
        else:
            self.count -= self.increment

    def xǁCounterǁinternal_transition__mutmut_2(self):
        if self.countUp:
            self.count -= self.increment
        else:
            self.count -= self.increment

    def xǁCounterǁinternal_transition__mutmut_3(self):
        if self.countUp:
            self.count += self.increment
        else:
            self.count = self.increment

    def xǁCounterǁinternal_transition__mutmut_4(self):
        if self.countUp:
            self.count += self.increment
        else:
            self.count += self.increment
    
    xǁCounterǁinternal_transition__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCounterǁinternal_transition__mutmut_1': xǁCounterǁinternal_transition__mutmut_1, 
        'xǁCounterǁinternal_transition__mutmut_2': xǁCounterǁinternal_transition__mutmut_2, 
        'xǁCounterǁinternal_transition__mutmut_3': xǁCounterǁinternal_transition__mutmut_3, 
        'xǁCounterǁinternal_transition__mutmut_4': xǁCounterǁinternal_transition__mutmut_4
    }
    
    def internal_transition(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCounterǁinternal_transition__mutmut_orig"), object.__getattribute__(self, "xǁCounterǁinternal_transition__mutmut_mutants"), args, kwargs, self)
        return result 
    
    internal_transition.__signature__ = _mutmut_signature(xǁCounterǁinternal_transition__mutmut_orig)
    xǁCounterǁinternal_transition__mutmut_orig.__name__ = 'xǁCounterǁinternal_transition'

    def xǁCounterǁexternal_transition__mutmut_orig(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_1(self, x, e):
        direction_in = None
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_2(self, x, e):
        direction_in = x.get(None)
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_3(self, x, e):
        direction_in = x.get("XXdirection_inXX")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_4(self, x, e):
        direction_in = x.get("DIRECTION_IN")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_5(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = None
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_6(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get(None)
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_7(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("XXincrement_inXX")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_8(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("INCREMENT_IN")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_9(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) >= 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_10(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 1:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_11(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = None
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_12(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[+1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_13(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-2]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_14(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) >= 0:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_15(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 1:
            self.increment = increment_in[-1]

    def xǁCounterǁexternal_transition__mutmut_16(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = None

    def xǁCounterǁexternal_transition__mutmut_17(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[+1]

    def xǁCounterǁexternal_transition__mutmut_18(self, x, e):
        direction_in = x.get("direction_in")
        increment_in = x.get("increment_in")
        if len(direction_in) > 0:
            self.countUp = direction_in[-1]
    
        if len(increment_in) > 0:
            self.increment = increment_in[-2]
    
    xǁCounterǁexternal_transition__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCounterǁexternal_transition__mutmut_1': xǁCounterǁexternal_transition__mutmut_1, 
        'xǁCounterǁexternal_transition__mutmut_2': xǁCounterǁexternal_transition__mutmut_2, 
        'xǁCounterǁexternal_transition__mutmut_3': xǁCounterǁexternal_transition__mutmut_3, 
        'xǁCounterǁexternal_transition__mutmut_4': xǁCounterǁexternal_transition__mutmut_4, 
        'xǁCounterǁexternal_transition__mutmut_5': xǁCounterǁexternal_transition__mutmut_5, 
        'xǁCounterǁexternal_transition__mutmut_6': xǁCounterǁexternal_transition__mutmut_6, 
        'xǁCounterǁexternal_transition__mutmut_7': xǁCounterǁexternal_transition__mutmut_7, 
        'xǁCounterǁexternal_transition__mutmut_8': xǁCounterǁexternal_transition__mutmut_8, 
        'xǁCounterǁexternal_transition__mutmut_9': xǁCounterǁexternal_transition__mutmut_9, 
        'xǁCounterǁexternal_transition__mutmut_10': xǁCounterǁexternal_transition__mutmut_10, 
        'xǁCounterǁexternal_transition__mutmut_11': xǁCounterǁexternal_transition__mutmut_11, 
        'xǁCounterǁexternal_transition__mutmut_12': xǁCounterǁexternal_transition__mutmut_12, 
        'xǁCounterǁexternal_transition__mutmut_13': xǁCounterǁexternal_transition__mutmut_13, 
        'xǁCounterǁexternal_transition__mutmut_14': xǁCounterǁexternal_transition__mutmut_14, 
        'xǁCounterǁexternal_transition__mutmut_15': xǁCounterǁexternal_transition__mutmut_15, 
        'xǁCounterǁexternal_transition__mutmut_16': xǁCounterǁexternal_transition__mutmut_16, 
        'xǁCounterǁexternal_transition__mutmut_17': xǁCounterǁexternal_transition__mutmut_17, 
        'xǁCounterǁexternal_transition__mutmut_18': xǁCounterǁexternal_transition__mutmut_18
    }
    
    def external_transition(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCounterǁexternal_transition__mutmut_orig"), object.__getattribute__(self, "xǁCounterǁexternal_transition__mutmut_mutants"), args, kwargs, self)
        return result 
    
    external_transition.__signature__ = _mutmut_signature(xǁCounterǁexternal_transition__mutmut_orig)
    xǁCounterǁexternal_transition__mutmut_orig.__name__ = 'xǁCounterǁexternal_transition'

    def xǁCounterǁconfluence_transition__mutmut_orig(self, x):
        self.external_transition(x, .0)
        self.internal_transition()

    def xǁCounterǁconfluence_transition__mutmut_1(self, x):
        self.external_transition(None, .0)
        self.internal_transition()

    def xǁCounterǁconfluence_transition__mutmut_2(self, x):
        self.external_transition(x, None)
        self.internal_transition()

    def xǁCounterǁconfluence_transition__mutmut_3(self, x):
        self.external_transition(.0)
        self.internal_transition()

    def xǁCounterǁconfluence_transition__mutmut_4(self, x):
        self.external_transition(x, )
        self.internal_transition()

    def xǁCounterǁconfluence_transition__mutmut_5(self, x):
        self.external_transition(x, 1.0)
        self.internal_transition()
    
    xǁCounterǁconfluence_transition__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCounterǁconfluence_transition__mutmut_1': xǁCounterǁconfluence_transition__mutmut_1, 
        'xǁCounterǁconfluence_transition__mutmut_2': xǁCounterǁconfluence_transition__mutmut_2, 
        'xǁCounterǁconfluence_transition__mutmut_3': xǁCounterǁconfluence_transition__mutmut_3, 
        'xǁCounterǁconfluence_transition__mutmut_4': xǁCounterǁconfluence_transition__mutmut_4, 
        'xǁCounterǁconfluence_transition__mutmut_5': xǁCounterǁconfluence_transition__mutmut_5
    }
    
    def confluence_transition(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCounterǁconfluence_transition__mutmut_orig"), object.__getattribute__(self, "xǁCounterǁconfluence_transition__mutmut_mutants"), args, kwargs, self)
        return result 
    
    confluence_transition.__signature__ = _mutmut_signature(xǁCounterǁconfluence_transition__mutmut_orig)
    xǁCounterǁconfluence_transition__mutmut_orig.__name__ = 'xǁCounterǁconfluence_transition'

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

def x_transition__mutmut_orig(counter_model, time_advance, time_passed, x) -> Counter:
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

def x_transition__mutmut_1(counter_model, time_advance, time_passed, x) -> Counter:
    input = None
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

def x_transition__mutmut_2(counter_model, time_advance, time_passed, x) -> Counter:
    input = True
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

def x_transition__mutmut_3(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) >= 0:
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

def x_transition__mutmut_4(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 1:
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

def x_transition__mutmut_5(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = None

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

def x_transition__mutmut_6(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = False

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

def x_transition__mutmut_7(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = ""
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

def x_transition__mutmut_8(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = None

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

def x_transition__mutmut_9(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed > time_advance:
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

def x_transition__mutmut_10(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed >= time_advance:
        if input != True:
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

def x_transition__mutmut_11(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed >= time_advance:
        if input == False:
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

def x_transition__mutmut_12(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed >= time_advance:
        if input == True:
            output = None
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

def x_transition__mutmut_13(counter_model, time_advance, time_passed, x) -> Counter:
    input = False
    for x_bag in x.values():
        if len(x_bag) > 0:
            input = True

    output = None
    time_adv2 = time_advance

    if time_passed >= time_advance:
        if input == True:
            output = counter_model.output()
            counter_model.confluence_transition(None)
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

def x_transition__mutmut_14(counter_model, time_advance, time_passed, x) -> Counter:
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
            time_adv2 = None
        elif input == False:
            output = counter_model.output()
            counter_model.internal_transition()
            time_adv2 = counter_model.time_advance()
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_15(counter_model, time_advance, time_passed, x) -> Counter:
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
        elif input != False:
            output = counter_model.output()
            counter_model.internal_transition()
            time_adv2 = counter_model.time_advance()
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_16(counter_model, time_advance, time_passed, x) -> Counter:
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
        elif input == True:
            output = counter_model.output()
            counter_model.internal_transition()
            time_adv2 = counter_model.time_advance()
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_17(counter_model, time_advance, time_passed, x) -> Counter:
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
            output = None
            counter_model.internal_transition()
            time_adv2 = counter_model.time_advance()
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_18(counter_model, time_advance, time_passed, x) -> Counter:
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
            time_adv2 = None
    else:
        if input == True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_19(counter_model, time_advance, time_passed, x) -> Counter:
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
        if input != True:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_20(counter_model, time_advance, time_passed, x) -> Counter:
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
        if input == False:
            counter_model.external_transition(x, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_21(counter_model, time_advance, time_passed, x) -> Counter:
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
            counter_model.external_transition(None, time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_22(counter_model, time_advance, time_passed, x) -> Counter:
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
            counter_model.external_transition(x, None)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_23(counter_model, time_advance, time_passed, x) -> Counter:
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
            counter_model.external_transition(time_passed)
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_24(counter_model, time_advance, time_passed, x) -> Counter:
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
            counter_model.external_transition(x, )
            time_adv2 = counter_model.time_advance()
    
    return output, time_adv2, counter_model

def x_transition__mutmut_25(counter_model, time_advance, time_passed, x) -> Counter:
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
            time_adv2 = None
    
    return output, time_adv2, counter_model

x_transition__mutmut_mutants : ClassVar[MutantDict] = {
'x_transition__mutmut_1': x_transition__mutmut_1, 
    'x_transition__mutmut_2': x_transition__mutmut_2, 
    'x_transition__mutmut_3': x_transition__mutmut_3, 
    'x_transition__mutmut_4': x_transition__mutmut_4, 
    'x_transition__mutmut_5': x_transition__mutmut_5, 
    'x_transition__mutmut_6': x_transition__mutmut_6, 
    'x_transition__mutmut_7': x_transition__mutmut_7, 
    'x_transition__mutmut_8': x_transition__mutmut_8, 
    'x_transition__mutmut_9': x_transition__mutmut_9, 
    'x_transition__mutmut_10': x_transition__mutmut_10, 
    'x_transition__mutmut_11': x_transition__mutmut_11, 
    'x_transition__mutmut_12': x_transition__mutmut_12, 
    'x_transition__mutmut_13': x_transition__mutmut_13, 
    'x_transition__mutmut_14': x_transition__mutmut_14, 
    'x_transition__mutmut_15': x_transition__mutmut_15, 
    'x_transition__mutmut_16': x_transition__mutmut_16, 
    'x_transition__mutmut_17': x_transition__mutmut_17, 
    'x_transition__mutmut_18': x_transition__mutmut_18, 
    'x_transition__mutmut_19': x_transition__mutmut_19, 
    'x_transition__mutmut_20': x_transition__mutmut_20, 
    'x_transition__mutmut_21': x_transition__mutmut_21, 
    'x_transition__mutmut_22': x_transition__mutmut_22, 
    'x_transition__mutmut_23': x_transition__mutmut_23, 
    'x_transition__mutmut_24': x_transition__mutmut_24, 
    'x_transition__mutmut_25': x_transition__mutmut_25
}

def transition(*args, **kwargs):
    result = _mutmut_trampoline(x_transition__mutmut_orig, x_transition__mutmut_mutants, args, kwargs)
    return result 

transition.__signature__ = _mutmut_signature(x_transition__mutmut_orig)
x_transition__mutmut_orig.__name__ = 'x_transition'

def copy_counter(counter1) -> Counter: # pragma: no mutate
    return Counter(counter1.count, counter1.increment, counter1.countUp, counter1.sigma) # pragma: no mutate
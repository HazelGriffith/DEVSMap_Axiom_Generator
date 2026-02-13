import source.Counter as C
import os

def generate_tests() -> list:
    '''
    generate exhaustive Counter model tests with the following 
    transition function parameters
    
    Const Counter: count = 2, increment = 1, countUp = True, sigma = 5.0
    
    time_advance: positive float
    time_passed: positive float
    
    direction_in: list of Bools
    increment_in: list of positive int
    
    :return: list of tests to be printed
    :rtype: list[str]
    '''
    counter1 = C.Counter(2,1,True,5.0)
    
    
    tests_generated = []
    time_passed_values = [0.0, 5.0, 10.0]
    d_in_values = [None, False, True]
    inc_in_values = [None, 0, 1]
    
    for tp in time_passed_values:
        for d_in in d_in_values:
            if (d_in != None):
                d_in_list = [d_in]
            else:
                d_in_list=[]
            for inc_in in inc_in_values:
                if inc_in != None:
                    inc_in_list = [inc_in]
                else:
                    inc_in_list = []
                x = {"direction_in":d_in_list, "increment_in":inc_in_list}
                output, tadv, counter2 = C.transition(C.copy_counter(counter1), counter1.sigma, tp, x)
                test = (f"s1;{counter1.count},{counter1.increment},{counter1.countUp},{counter1.sigma};"+
                        f"ta;{counter1.sigma};tp;{tp};d_in;{d_in};inc_in;{inc_in};"+
                        f"s2;{counter2.count},{counter2.increment},{counter2.countUp},{counter2.sigma};"+
                        f"output;{output};tadv;{tadv}")
                tests_generated.append(test)
                    
    return tests_generated
    
def save(tests:list[str], filename:str):
    try:
        with open(f"tests/{filename}.txt", "x") as newFile:
            for trial in tests:
                newFile.write(trial+"\n")
    except Exception as e:
        os.remove(f"tests/{filename}.txt")
        save(tests, filename)
    
if __name__=="__main__":
    '''
    Generate Test Cases
    '''
    
    cwd = os.getcwd()
    
    if cwd.endswith("DEVSMap_Axiom_Generator"):
        os.chdir("Mutation_Testing")
        
    tests = generate_tests()
    save(tests, "counter_tests")
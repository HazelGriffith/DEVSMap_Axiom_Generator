import source.Counter as C
import os, pytest

def load_tests(filename:str):
    tests = {}
    with open(f"tests/{filename}.txt","r") as tests_file:
        line = tests_file.readline()
        lineNo = 1
        while line != "":
            test_values = {}
            params = line.split(";")
            s1 = params[1]
            ta1 = float(params[3])
            test_values.update({"ta1":ta1})
            tp = float(params[5])
            test_values.update({"tp":tp})
            
            d_in_str = params[7]
            if d_in_str != "None":
                if d_in_str == "False":
                    d_in = [False]
                else:
                    d_in = [True]
            else:
                d_in = []
                
            inc_in_str = params[9]
            if inc_in_str != "None":
                inc_in = [int(inc_in_str)]
            else:
                inc_in = []

            x = {"direction_in":d_in, "increment_in":inc_in}
            test_values.update({"x":x})
            s2 = params[11]
            
            
            output_str = params[13]
            if output_str != "None":
                output = int(output_str)
            else:
                output = None
                
            test_values.update({"output":output})
            ta2 = float(params[15])
            test_values.update({"ta2":ta2})
            s1_params = s1.split(",")
            if s1_params[2] == "False":
                counter1_countUp = False
            else:
                counter1_countUp = True
            counter1 = C.Counter(int(s1_params[0]), int(s1_params[1]), counter1_countUp, float(s1_params[3]))
            test_values.update({"counter1":counter1})
            s2_params = s2.split(",")
            
            if s2_params[2] == "False":
                counter2_countUp = False
            else:
                counter2_countUp = True
            counter2 = C.Counter(int(s2_params[0]), int(s2_params[1]), counter2_countUp, float(s2_params[3]))
            test_values.update({"counter2":counter2})
            
            tests.update({lineNo:test_values})
            
            line = tests_file.readline()
            lineNo+=1
    return tests
            

def pytest_generate_tests(metafunc):
    if "get_tests" in metafunc.fixturenames:
        tests = load_tests("counter_tests")
        test_ids = list(tests.keys())
        test_values = list(tests.values())
        metafunc.parametrize("get_tests", test_values, ids=test_ids)

def test_transition(get_tests):
    counter1 = get_tests["counter1"]
    ta1 = get_tests["ta1"]
    tp = get_tests["tp"]
    x = get_tests["x"]
    
    actual_output, actual_ta, actual_counter = C.transition(C.copy_counter(counter1), ta1, tp, x)
    print(counter1)
    print(f"ta: {ta1}")
    print(f"tp: {tp}")
    print(f"x: {x}")
    print(actual_counter)
    exp_counter = get_tests["counter2"]
    exp_ta = get_tests["ta2"]
    exp_output = get_tests["output"]
    
    assert(actual_counter.equal(exp_counter))
    assert(actual_output == exp_output)
    assert(actual_ta == exp_ta)
    
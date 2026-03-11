import source.Counter as C
import subprocess, shutil, time, os, pytest

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
        
@pytest.fixture(autouse=True)
def copy_problem_file():
    if os.path.exists("tests/counter_model_copy.p"):
        os.remove("tests/counter_model_copy.p")
    shutil.copy2("tests/counter_model.p","tests/counter_model_copy.p")
    
    yield
    
    if os.path.exists("tests/counter_model_copy.p"):
        os.remove("tests/counter_model_copy.p")

def test_transition(get_tests):

    counter1 = get_tests["counter1"]
    ta1 = get_tests["ta1"]
    tp = get_tests["tp"]
    x = get_tests["x"]
    d_in = x.get("direction_in")
    inc_in = x.get("increment_in")
    
    actual_output, actual_ta, actual_counter = C.transition(C.copy_counter(counter1), ta1, tp, x)


    axioms = []
    axioms.append(f"tff(count_value,axiom,count = {float(counter1.count)}).\n")
    axioms.append(f"tff(increment_value,axiom,increment = {float(counter1.increment)}).\n")
    countUp = str(counter1.countUp)
    if countUp == "False":
        countUp = "$false"
    else:
        countUp = "$true"
    axioms.append(f"tff(countUp_value,axiom,countUp = {countUp}).\n")
    axioms.append(f"tff(sigma_value,axiom,sigma = {float(counter1.sigma)}).\n")
    axioms.append(f"tff(ta_in_value,axiom,ta_in = {ta1}).\n")
    axioms.append(f"tff(time_passed_value,axiom,time_passed = {tp}).\n")
    axioms.append(f"tff(num_rcvd_direction_in,axiom,num_rcvd(direction_in) = {len(d_in)}).\n")
    axioms.append(f"tff(num_rcvd_increment_in,axiom,num_rcvd(increment_in) = {len(inc_in)}).\n")
    if len(d_in) > 0:
        d_in_value = str(d_in[-1])
        if d_in_value == "False":
            d_in_value = "$false"
        else:
            d_in_value = "$true"
        axioms.append(f"tff(val_rcvd_direction_in_value,axiom,val_rcvd_direction_in = {d_in_value}).\n")
        
    if len(inc_in) > 0:
        axioms.append(f"tff(val_rcvd_increment_in_value,axiom,val_rcvd_increment_in = {float(inc_in[-1])}).\n")
        
    countUp = str(actual_counter.countUp)
    if countUp == "False":
        countUp = "$false"
    else:
        countUp = "$true"

    if actual_output != None:
        output_cond = f"(val_output_count_out = {float(actual_output)})&"
    else:
        output_cond = ""

    axioms.append(f"tff(next_state_conjecture,conjecture,(next_count = {float(actual_counter.count)})&"+
                                                    f"(next_increment = {float(actual_counter.increment)})&"+
                                                    f"(next_countUp = {countUp})&"+
                                                    f"(next_sigma = {actual_counter.sigma})&"+
                                                    output_cond+
                                                    f"(ta_out = {actual_ta})).\n")
    
    


    with open("tests/counter_model_copy.p", "a") as test_file:
        test_file.write("\n")
        for axiom in axioms:
            test_file.write(axiom+"\n")
    
    filename = str(time.time())
    output = subprocess.run(["./tests/vampire", "-t", "1d", "-p", "off", "-om", "smtcomp", "tests/counter_model_copy.p"], capture_output=True, text=True)
    output_lines = output.stdout.splitlines()
    termination_reason = output_lines[1]
    if termination_reason != "unsat":
        shutil.copy2("tests/counter_model_copy.p",f"tests/notUnsat_{filename}.p")
    assert(termination_reason == "unsat")
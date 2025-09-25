import json
import re


class Axiom_Generator:
    integers = ["int", "unsigned int", "integer", "INT", "unsigned natural", "natural"]
    reals = ["double", "float", "unsigned double", "unsigned float"]
    conditionals = ["==", "!=", ">", "<", ">=", "<=", "&&", "||"]
    conditionalsWOEquals = [">", "<", ">=", "<=", "-", "+", "*", "/"]
    syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"product", "/":"$quotient", "&&":"&", "||":"|"}


    def __init__(self, model_file_path: str, init_state_file_path: str):
        #Getting atomic model file
        with open(model_file_path) as jfile:
            self.model_json = json.load(jfile)["counter"]

        #Getting initial state file
        with open(init_state_file_path) as jfile:
            self.init_state_json = json.load(jfile)

        #initializing variables
        self.tff_string = ''
        self.state_var_names = []
        self.in_port_names = []
        self.out_port_names = []

    '''
    Creates a new .p file with the given name containing the tff axioms generated
    args: filename = string
    '''
    def save(self, filename:str):
        try:
            with open(filename+".p", 'x') as pfile:
                pfile.write(self.tff_string)

        except Exception as e:
            print(e)

    '''
    Parses the JSON dictionary of the state variables and saves the tff statements in the class string
    '''
    def parse_state_vars(self):
        state = model["s"]
    
        self.tff_string+=("%-----STATE VARIABLE DEFINITIONS\n")
        for pos, key in enumerate(state):
            self.state_var_names.append(key)
            line = "tff("+key+", type, "
            if (state[key] in integers):
                line+= "$int)."
            elif (state[key] == "bool"):
                line+= "$o)."
            elif (state[key] in reals):
                line+= "$real)."
            self.tff_string+=(line+"\n")
            line = "tff(next_"+key+", type, "
            if (state[key] in integers):
                line+= "$int)."
            elif (state[key] == "bool"):
                line+= "$o)."
            elif (state[key] in reals):
                line+= "$real)."
            self.tff_string+=(line+"\n")
    
def parseDict_recurs(deltaDict, line):
    for pos, key in enumerate(deltaDict):
        newline = ""
        if (isinstance(deltaDict[key],dict)):
            if (pos+1 != len(delta_int)):
                condition = key.split()
                assert len(condition) == 3
                newline += "( "+condition[0]+" "+syntaxMap[condition[1]]+" "+condition[2]+" )"
                if (isinstance(deltaDict[key].values()[0],dict)):
                    newline += " &\n"
                else:
                    newline += " -> "
                parseDict_recurs(deltaDict[key],line+newline)
            else:
                assert key == "otherwise"
                print("otherwise")
        else:
            if (pos+1 != 1):
                newline += "& "
            newline += "(next_"+key+" = "
            result = deltaDict[key].split()
            if (len(result) == 3):
                if (result[1] in conditionalsWOEquals):
                    newline += "( "+syntaxMap[result[1]]+"("+result[0]+","+result[2]+") )"
                elif (result[1] == "=="):
                    newline += "( "+result[0]+" = "+result[1]+")"
                elif (result[1] == "!="):
                    newline += "( ~"+result[0]+" = "+result[1]+")"
            else:
                assert len(result) == 1
                    
            if (pos+1 == len(deltaDict)):
                newline += ").\n"
            else:
                newline += "\n"
    return line+newline
                    




    state = model["s"]
    
    pfile.write("%-----STATE VARIABLE DEFINITIONS\n")
    for pos, key in enumerate(state):
        state_var_names.append(key)
        line = "tff("+key+", type, "
        if (state[key] in integers):
            line+= "$int)."
        elif (state[key] == "bool"):
            line+= "$o)."
        elif (state[key] in reals):
            line+= "$real)."
        pfile.write(line+"\n")
        line = "tff(next_"+key+", type, "
        if (state[key] in integers):
            line+= "$int)."
        elif (state[key] == "bool"):
            line+= "$o)."
        elif (state[key] in reals):
            line+= "$real)."
        pfile.write(line+"\n")

    pfile.write("\n")

    in_ports = model["x"]

    pfile.write("%-----INPUT PORT DEFINITIONS\n")
    pfile.write("tff(i_port_type, type, i_port : $tType).\n")
    define_set = "tff(only_i_ports, axiom,\n\t! [IP : i_port] :\n\t\t( "
    for pos, key in enumerate(in_ports):
        in_port_names.append(key)
        pfile.write("tff("+key+", type, "+key+" : i_port).\n")
        line = "tff(rcvd_"+key+", type, rcvd_"+key+" : "
        if (in_ports[key] in integers):
            line += "$int)."
        elif (in_ports[key] == "bool"):
            line += "$o)."
        elif (in_ports[key] in reals):
            line += "$real)."
        pfile.write(line+"\n")
        define_set += "IP = "+key
        if (pos+1 != len(in_ports)):
            define_set += " | "
        else:
            define_set += ")).\n\n"
    pfile.write(define_set)

    out_ports = model["y"]

    pfile.write("%-----OUTPUT PORT DEFINITIONS\n")
    pfile.write("tff(o_port_type, type, o_port : $tType).\n")
    define_set = "tff(only_o_ports, axiom,\n\t! [OP : o_port] :\n\t\t( "
    for pos, key in enumerate(out_ports):
        out_port_names.append(key)
        pfile.write("tff("+key+", type, "+key+" : o_port).\n")
        define_set += "OP = "+key
        if (pos+1 != len(out_ports)):
            define_set += " | "
        else:
            define_set += ")).\n\n"
    pfile.write(define_set)

    delta_int = model["delta_int"]

    pfile.write("%-----INTERNAL TRANSITIONS\n")

    #Flatten the nested dictionary of conditions and state variable assignments
    #For the internal transition function
    flat_delta_int = {}
    stack = [(delta_int, '')]

    while stack:
        c, p = stack.pop()
        
        strings = []
        for k, v in c.items():
            
            if isinstance(v, dict):
                if len(v) > 0:
                    new_key = f"{p};{k}" if p else k
                    stack.append((v, new_key)) 
                else:
                    strings.append(k)
            else:
                strings.append(k+ " = "+v)
        if (len(strings) > 0):
            if (p == ''):
                flat_delta_int['otherwise'] = 'True'
            else:
                flat_delta_int[p] = strings
    
    for pos, key in enumerate(flat_delta_int):
        line = "tff(delta_int_"+str(pos)+",axiom,\n"
        conds = key.split(";")
        assert(len(conds > 0))
        if (len(conds)==1):

if __name__ == '__main___':
    axiom_gen = Axiom_Generator('DEVSMap_Files/counter_atomic.json', 'DEVSMap_Files/counter_tester_init_state.json')

    axiom_gen.save("test")
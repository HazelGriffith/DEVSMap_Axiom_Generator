import json
import os
import re


class Axiom_Generator:
    integers = ["int", "unsigned int", "integer", "INT", "unsigned natural", "natural"]
    reals = ["double", "float", "unsigned double", "unsigned float"]
    infixConds = ["=", "!=", "&", "|"]
    nonInfixConds = ["<", "<=", ">", ">=","--","+","*","/"]
    syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"product", "/":"$quotient", "&&":"&", "||":"|", "!=":"!="}


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
            os.remove(filename+".p")
            self.save(filename)


    '''
    Parses the JSON dictionary of the state variables and saves 
    the tff statements in the string
    '''
    def parse_state_vars(self):
        state = self.model_json["s"]
    
        self.tff_string+=("\n%-----STATE VARIABLE DEFINITIONS\n")
        for pos, key in enumerate(state):
            self.state_var_names.append(key)
            line = "tff("+key+", type, "
            if (state[key] in self.integers):
                line+= "$int)."
            elif (state[key] == "bool"):
                line+= "$o)."
            elif (state[key] in self.reals):
                line+= "$real)."
            self.tff_string+=(line+"\n")
            line = "tff(next_"+key+", type, "
            if (state[key] in self.integers):
                line+= "$int)."
            elif (state[key] == "bool"):
                line+= "$o)."
            elif (state[key] in self.reals):
                line+= "$real)."
            self.tff_string+=(line+"\n")

    '''
    Parses the JSON dictionary for the input port information and saves 
    it in tff axioms in the string
    '''
    def parse_i_ports(self):
        in_ports = self.model_json["x"]

        self.tff_string+=("\n%-----INPUT PORT DEFINITIONS\n")
        self.tff_string+=("tff(i_port_type, type, i_port : $tType).\n")
        define_set = "tff(only_i_ports, axiom,\n\t! [IP : i_port] :\n\t\t( "
        for pos, key in enumerate(in_ports):
            self.in_port_names.append(key)
            self.tff_string+=("tff("+key+", type, "+key+" : i_port).\n")
            line = "tff(rcvd_"+key+", type, rcvd_"+key+" : "
            if (in_ports[key] in self.integers):
                line += "$int)."
            elif (in_ports[key] == "bool"):
                line += "$o)."
            elif (in_ports[key] in self.reals):
                line += "$real)."
            self.tff_string+=(line+"\n")
            define_set += "IP = "+key
            if (pos+1 != len(in_ports)):
                define_set += " | "
            else:
                define_set += ")).\n\n"
        self.tff_string+=(define_set)
    
    '''
    Parses the JSON dictionary for the output port information and saves 
    it in tff axioms in the string
    '''
    def parse_o_ports(self):
        out_ports = self.model_json["y"]

        self.tff_string+=("\n%-----OUTPUT PORT DEFINITIONS\n")
        self.tff_string+=("tff(o_port_type, type, o_port : $tType).\n")
        define_set = "tff(only_o_ports, axiom,\n\t! [OP : o_port] :\n\t\t( "
        for pos, key in enumerate(out_ports):
            self.out_port_names.append(key)
            self.tff_string+=("tff("+key+", type, "+key+" : o_port).\n")
            define_set += "OP = "+key
            if (pos+1 != len(out_ports)):
                define_set += " | "
            else:
                define_set += ")).\n\n"
        self.tff_string+=(define_set)

    '''
    Parses the JSON dictionary for the internal transition function
    information and saves it in tff axioms in the string
    '''
    def parse_delta_int(self):
        delta_int = self.model_json["delta_int"]

        self.tff_string+=("\n%-----INTERNAL TRANSITIONS\n")

        #Flatten the nested dictionary of conditions and state variable assignments
        #For the internal transition function
        flat_delta_int = self.flatten_dict(delta_int)
        print(flat_delta_int)
        flat_delta_int.pop("otherwise")
        flat_delta_int.pop("Otherwise")

        for pos, key in enumerate(flat_delta_int):
            line = "tff(delta_int_"+str(pos)+",axiom,\n"
            conds = key.split(";")
            assert(len(conds) > 0)
            for pos, condition in enumerate(conds):
                if pos+1 == 1:
                    line+="("
                ops = condition.split(" ")
                assert(len(ops) > 0)
                if (len(ops) == 1):
                    op1 = ops[0]
                    op1 = self.find_replace_not(op1)
                    line+=f"({op1})"
                elif (len(ops) == 3):
                    op1 = self.find_replace_not(ops[0])
                    op1 = self.find_replace_bool(op1)
                    op3 = self.find_replace_not(ops[2])
                    op3 = self.find_replace_bool(op3)
                    op2 = self.syntaxMap[ops[1]]
                    if (op2 in self.infixConds):
                        line+= f"({op1} {op2} {op3})"
                    elif (op2 in self.nonInfixConds):
                        line+= f"{op2}({op1},{op3})"
                    else:
                        assert False, f"{op2} is an unrecognized conditional operator: {op1}{op2}{op3}"
                else:
                    assert False, "cannot have 2 or more than three ops in a condition"
                if pos+1 == len(conds):
                    line+=") -> \n"
                else:
                    line+= " & "
            self.tff_string+=line
    '''
    Flatten the nested dictionary of conditions and state variable assignments
    Args: d = dictionary
    returns: dictionary
    '''
    def flatten_dict(self, d:dict) -> dict:
        flat_d = {}
        stack = [(d, '')]

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
                    flat_d[strings[0]] = 'True'
                else:
                    flat_d[p] = strings
        return flat_d
    
    '''
    When given a string it will check if the not function "!" is at the start
    and replace it with the TPTP syntax "~" not function
    Args: s = string
    returns: string
    '''
    def find_replace_not(self, s:str) -> str:
        if s.startswith("!"):
            s.replace("!","~")
        return s

    '''
    When given a string that contains a boolean of true 
    or false it will return the TPTP syntax version
    Args: s = string
    returns: string
    '''
    def find_replace_bool(self, s:str) -> str:
        if (s == "true" or s == "True"):
            return "$true"
        elif (s == "false" or s == "False"):
            return "$false"
        else:
            return s
'''
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
'''
if __name__ == "__main__":

    axiom_gen = Axiom_Generator('DEVSMap_Files/counter_atomic.json', 'DEVSMap_Files/counter_tester_init_state.json')
    axiom_gen.parse_state_vars()
    axiom_gen.parse_i_ports()
    axiom_gen.parse_o_ports()
    axiom_gen.parse_delta_int()
    axiom_gen.save("test")
import json
import os
import re
from axiom import Axiom, Binary_Formula, Unary_Formula, Formula, Constant
from Equation import Expression



class Axiom_Generator:
    integers = ["int", "unsigned int", "integer", "INT", "unsigned natural", "natural"]
    reals = ["double", "float", "unsigned double", "unsigned float"]
    infixConds = ["==", "!=", "&&", "||"]
    prefixConds = ["<", "<=", ">", ">=","--","-","+","*","/"]
    syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"$product", "/":"$quotient", "&&":"&", "||":"|", "!=":"!="}

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
        self.axioms = []

    '''
    Creates a new .p file with the given name containing the tff axioms generated
    args: filename = string
    '''
    def save(self, filename:str):
        try:
            with open(filename+".p", 'x') as pfile:
                for ax in self.axioms:
                    pfile.write(ax)

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
            line = "tff("+key+", type, "
            self.state_var_names.append(key)
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
            self.tff_string+=f"tff(num_rcvd_{key}, type, num_rcvd_{key} : $int).\n"
            line = "tff(val_rcvd_"+key+", type, val_rcvd_"+key+" : "
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
    Recursively parses and generates axioms from the trans function dictionaries
    args: axiom_num = int, cond_list = list<string>, transition_function = dict<string: dict<>> or dict<string: string>, translation(int, list<string>, dict<string:string>) -> string
    returns: axiom_num = int, axiom = string
    '''

    def parse_devsmap_dict(self, axiom_num:int, cond_list, transition_function, translation):
        #Assumes no dictionary will have different key-value types within itself
        if (len(transition_function) == 0) or isinstance(list(transition_function.values())[0], str):
            axiom = translation(axiom_num, cond_list, transition_function)
            return axiom, axiom_num+1
        elif isinstance(list(transition_function.values())[0], dict):
            other_conds = []
            num = axiom_num
            for pos, key in enumerate(transition_function):
                if key.casefold() != "otherwise":
                    other_conds.append(key)
                    new_cond_list = cond_list.copy()
                    new_cond_list.append(key)
                    axiom, num = self.parse_devsmap_dict(num, new_cond_list, transition_function[key], translation)
                    if axiom is None:
                        return None, num
                    else:
                        self.axioms.append(axiom)
            other_conds = self.negate_conds(other_conds)
            if 'otherwise' in transition_function.keys():
                axiom, num = self.parse_devsmap_dict(num, other_conds, transition_function['otherwise'], translation)
            else:
                axiom, num = self.parse_devsmap_dict(num, other_conds, {}, translation)

            if axiom is None:
                return None, num
            else:
                self.axioms.append(axiom)
            return None, num
        else:
            assert False, "The transition functions keys and values can only ever be strings or nested dictionaries"

    '''
    Receives a list of tff strings that need to be negated
    args: cond_list = list<string>
    returns: cond_list = list<string
    '''
    def negate_conds(self, cond_list):
        
        for i in range(len(cond_list)):
            if (cond_list[i].startswith("!")):
                cond_list[i].replace("!","")
            else:
                cond_list[i] = f"!({cond_list[i]})"
        return cond_list


    '''
    Accepts the axiom number, list of condition statements, and the variable assignments to create a tff axiom
    describing one axiom of the internal transition function
    args: axiom_num = int, cond_list = list<string>, assignment_dict = dict<string: string>
    returns: axiom = string
    '''
    def gen_delta_int_tff(self, axiom_num:int, cond_list, assignments_dict):
        
        new_cond_list = self.parse_clauses(cond_list)
        if (len(new_cond_list) > 1):
            lhs = self.build_CNF(Binary_Formula("",new_cond_list.pop(0),new_cond_list.pop(0),"&&"), new_cond_list)
        else:
            lhs = new_cond_list[0]

        assignments = []
        if len(assignments_dict) > 0:
            for pos, key in enumerate(assignments_dict.keys()):
                assignment_values = self.parse_clauses([assignments_dict[key]])
                assignment_value = assignment_values[0]
                assignments.append(Binary_Formula("", Constant(f"next_{key}"), assignment_value, "=="))
        else:
            for pos, var in enumerate(self.state_var_names):
                assignments.append(Binary_Formula("",Constant(f"next_{var}"),Constant(f"{var}"), "=="))
        if (len(assignments) > 1):
            rhs = self.build_CNF(Binary_Formula("",assignments.pop(0),assignments.pop(0),"&&"), assignments)
        elif (len(assignments) == 1):
            rhs = assignments[0]
        else:
            assert False, "There cannot be zero assignments"
        f1 = Binary_Formula("", lhs, rhs, "=>")
        return Axiom('tff',f"axiom_{axiom_num}","axiom",f1)
    
    '''
    Accepts the axiom number, list of condition statements, and the variable assignments to create a tff axiom
    describing one axiom of the external transition function
    args: axiom_num = int, cond_list = list<string>, assignment_dict = dict<string: string>
    returns: axiom = string
    '''
    def gen_delta_ext_tff(self, axiom_num:int, cond_list, assignments_dict):
        axiom = f"tff(delta_ext_{axiom_num},axiom,\n\t("
        new_cond_list = self.parse_clauses(cond_list)
        for pos, cond in enumerate(new_cond_list):
            axiom += f"{cond}"
            if (pos+1) == len(new_cond_list):
                axiom += f") =>\n\t\t("
            else:
                axiom += f" & "
        if len(assignments_dict) > 0:
            for pos, key in enumerate(assignments_dict.keys()):
                assignment_value = self.parse_clauses([assignments_dict[key]])
                axiom += f"next_{key} = {assignment_value[0]}"
                if (pos+1) == len(assignments_dict):
                    axiom += ")).\n"
                else:
                    axiom += " & "
        else:
            for pos, var in enumerate(self.state_var_names):
                axiom += f"next_{var} = {var}"
                if (pos+1) == len(self.state_var_names):
                    axiom += ")).\n"
                else:
                    axiom += " & "
        return axiom
    
    '''
    translates every math operation into TPTP syntax
    args: clauses = list<string>
    returns: new_clauses = list<Constant | Formula>
    '''
    def parse_clauses(self, clauses):
        new_clauses = []
        for i in range(len(clauses)):
            clause = clauses[i]
            clause = clause.replace("||","|")
            clause = clause.replace("&&","&")
            clause = clause.replace("()","")
            clause = clause.replace("(-1)","")
            clause = clause.replace(".","_")
            new_clauses.append(self.parse_clause(str(Expression(clause))))
        return new_clauses

    '''
    Use SymPy to parse the string expression's abstract syntax tree and convert it to Formula/Constant objects
    Args: clause = string
    returns: Formula | Constant
    '''
    def parse_clause(self, clause):
        
        clause = clause.replace("\\left(","(")
        clause = clause.replace("\\right)",")")
        clause = clause.replace(" = ", " == ")
        clause = clause.replace("\\lor", "||")
        clause = clause.replace("\\land", "&&")
        clause = clause.replace("\\neg ", "!")
        clause = clause.replace("\\neq", "!=")
        clause = clause.replace("\\leq", "<=")
        clause = clause.replace("\\geq", ">=")
        clause = clause.replace("\\times", "*")
        
        if clause.startswith("!"):
            return Unary_Formula("",self.parse_clause("("+clause[1:]+")"), "!")
        else:
            clause = clause[1:-1]
            lb = clause.find("(")
            if lb == -1:
                ops = clause.split(" ")
                if (len(ops) == 1):
                    return Constant(ops[0])
                elif (len(ops) == 3):
                    return Binary_Formula("",ops[0], ops[2], ops[1])
                else:
                    assert False, f"{ops} should only have 1 or 3 elements split by whitespaces"
            elif lb >= 0:
                stack = 0
                outside_start = 0
                outside_end = 0
                whitespace = 0
                outside = ""
                for i in range(len(clause)):
                    if (clause[i] == "("):
                        stack += 1
                    elif (clause[i] == ")"):
                        stack -= 1
                    elif (stack == 0):
                        if (clause[i] == " "):
                            whitespace += 1
                            if (whitespace == 2):
                                outside_end = i
                            elif (whitespace == 1):
                                outside_start = i
                        else:
                            outside += clause[i]
                lhs = clause[:outside_start].strip()
                rhs = clause[outside_end:].strip()
                return Binary_Formula("",self.parse_clause(lhs),self.parse_clause(rhs), outside.strip())
            else:
                assert False, f"{lb} cannot be lower than -1"

    '''
    Recursively builds the antecedent in Clausal Normal Form
    Args: lhs = Binary_Formula, remaining_clauses = list[Constant|Formula]
    Returns: Binary_Formula
    '''
    def build_CNF(self, lhs:Binary_Formula, remaining_clauses) -> Binary_Formula:
        if (len(remaining_clauses) > 0):
            rhs = remaining_clauses.pop(0)
            if (len(remaining_clauses) == 0):
                return Binary_Formula("", lhs, rhs, "&&")
            else:
                return self.build_CNF(Binary_Formula("",lhs,rhs,"&&"), remaining_clauses)
        else:
            return lhs


    '''
    Function that checks if the string contains a constant expression or a Unary Not Formula
    Args: s = string
    Returns: Constant | Unary_Formula
    '''
    def parse_not_formulas(self, s:str) -> Constant | Unary_Formula:
        if s.startswith("!"):
            s = s.replace("!","")
            if (s.startswith("(") and s.endswith(")")):
                s = s.replace("(","")
                s = s.replace(")","")
            result = Unary_Formula("",Constant(s),"!")
        else:
            result = Constant(s)
        return result

    '''
    Parses the JSON dictionary for the internal transition function
    information and saves it in tff axioms in the string
    '''
    def parse_delta_int(self):
        delta_int = self.model_json["delta_int"]

        self.tff_string+=("\n%-----INTERNAL TRANSITIONS\n")

        self.parse_devsmap_dict(0,[],delta_int,self.gen_delta_int_tff)
    
    '''
    Parses the JSON dictionary for the external transition function
    information and saves it in tff axioms in the string
    '''
    def parse_delta_ext(self):
        delta_ext = self.model_json["delta_ext"]

        self.tff_string+=("\n&-----EXTERNAL TRANSITIONS\n")

        self.parse_devsmap_dict(0,[],delta_ext,self.gen_delta_ext_tff)

    '''
    When given a string it will check if the not function "!" is at the start
    and replace it with the TPTP syntax "~" not function
    Args: s = string
    returns: string
    '''
    def find_replace_not(self, s:str) -> str:
        if s.startswith("!"):
            return s.replace("!","~")
        else:
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
    When given a string that contains a bag function
    the function will return its TPTP equivalent
    Args: s = string
    returns: string
    '''
    def find_replace_bag_funcs(self, s:str) -> str:
        if s.endswith("bagSize()"):
            for port in self.in_port_names:
                if port in s:
                    if s.startswith("!") or s.startswith("~"):
                        return f"!(num_rcvd({port}))"
                    else:
                        return f"num_rcvd({port})"
            assert False, f"bagSize must be associated with an in_port not {s}"
        elif s.endswith("bag(-1)"):
            for port in self.in_port_names:
                if port in s:
                    if s.startswith("!") or s.startswith("~"):
                        return f"!(val_rcvd({port}))"
                    else:
                        return f"val_rcvd({port})"
            assert False, f"bag(-1) must be associated with an in_port not {s}"
        else:
            return s
        
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
                    flat_d[strings[0].casefold()] = ['True']
                else:
                    flat_d[p.casefold()] = strings
        return flat_d

if __name__ == "__main__":

    axiom_gen = Axiom_Generator('DEVSMap_Files/counter_atomic.json', 'DEVSMap_Files/counter_tester_init_state.json')
    axiom_gen.parse_state_vars()
    axiom_gen.parse_i_ports()
    axiom_gen.parse_o_ports()
    axiom_gen.parse_delta_int()
    axiom_gen.parse_delta_ext()
    axiom_gen.save("test")
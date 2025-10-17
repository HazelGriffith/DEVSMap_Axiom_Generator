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
    section_names = ["state_var_axioms", "i_port_axioms", "o_port_axioms", "delta_int_axioms", "delta_ext_axioms", "delta_con_axioms", "lambda_axioms", "ta_axioms"]

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
        self.axioms = {}
        for section in self.section_names:
            self.axioms.update({section:[]})

    '''
    Creates a new .p file with the given name containing the tff axioms generated
    args: filename = string
    '''
    def save(self, filename:str):
        try:
            with open(filename+".p", 'x') as pfile:
                for section in self.section_names:
                    if section == "state_var_axioms":
                        pfile.write("\n%-----STATE VARIABLE DEFINITIONS\n\n")
                    elif section == "i_port_axioms":
                        pfile.write("\n%-----INPUT PORT DEFINITIONS\n\n")
                    elif section == "o_port_axioms":
                        pfile.write("\n%-----OUTPUT PORT DEFINITIONS\n\n")
                    elif section == "delta_int_axioms":
                        pfile.write("\n%-----INTERNAL TRANSITION FUNCTION AXIOMS\n\n")
                    elif section == "delta_ext_axioms":
                        pfile.write("\n%-----EXTERNAL TRANSITION FUNCTION AXIOMS\n\n")
                    elif section == "delta_con_axioms":
                        pfile.write("\n%-----CONFLUENCE TRANSITION FUNCTION AXIOMS\n\n")
                    elif section == "lambda_axioms":
                        pfile.write("\n%-----LAMBDA AXIOMS\n\n")
                    elif section == "ta_axioms":
                        pfile.write("\n%-----TIME ADVANCE AXIOMS\n\n")
                    
                    axioms = self.axioms[section]
                    for axiom in axioms:
                        pfile.write(axiom.__str__()+"\n")

                pfile.write(self.add_devs_tff_axioms())

        except Exception as e:
            os.remove(filename+".p")
            self.save(filename)


    def add_devs_tff_axioms(self):
        line = ""
        line += "\n%-----DEVS TFF AXIOMS\n\n"
        axiom1 = ("tff(internal_transition_occurred,axiom,\n\t" +
                    "! [IP : i_port]\n\t\t" +
                        "((($greatereq(time_passed,time_advance)) & \n\t\t" +
                        "(num_rcvd(IP) = 0)) => (\n\t\t"+
                        "(internal_transition = $true) &\n\t\t" +
                        "(external_transition = $false) &\n\t\t" +
                        "(confluence_transition = $false) &\n\t\t" +
                        "(output = $true)))).\n\n")
        
        axiom2 = ("tff(external_transition_occurred,axiom,\n\t" +
                    "? [IP : i_port]\n\t\t" +
                        "((($less(time_passed,time_advance)) & \n\t\t" +
                        "(num_rcvd(IP) != 0)) => (\n\t\t"+
                        "(internal_transition = $false) &\n\t\t" +
                        "(external_transition = $true) &\n\t\t" +
                        "(confluence_transition = $false) &\n\t\t" +
                        "(output = $false)))).\n\n")
                
        axiom3 = ("tff(confluence_transition_occurred,axiom,\n\t" +
                    "? [IP : i_port]\n\t\t" +
                        "((($greatereq(time_passed,time_advance)) & \n\t\t" +
                        "(num_rcvd(IP) != 0)) => (\n\t\t"+
                        "(internal_transition = $false) &\n\t\t" +
                        "(external_transition = $false) &\n\t\t" +
                        "(confluence_transition = $true) &\n\t\t" +
                        "(output = $true)))).\n\n")
        line += axiom1
        line += axiom2
        line += axiom3
        return line



    '''
    Parses the JSON dictionary of the state variables and saves 
    the tff statements in the string
    '''
    def parse_state_vars(self):
        state = self.model_json["s"]
        state_var_axioms = []

        for pos, key in enumerate(state):
            var_type = ""
            self.state_var_names.append(key)
            if (state[key] in self.integers):
                var_type = "$int"
            elif (state[key] == "bool"):
                var_type = "$o"
            elif (state[key] in self.reals):
                var_type = "$real"
            else:
                assert False, f"{state[key]} variable type is unsupported"

            state_var_axioms.append(Axiom("tff", key, "type", Constant(var_type)))
            state_var_axioms.append(Axiom("tff",f"next_{key}", "type", Constant(var_type)))

        self.axioms.update({"state_var_axioms":state_var_axioms})


    '''
    Parses the JSON dictionary for the input port information and saves 
    it in tff axioms in the string
    '''
    def parse_i_ports(self):
        in_ports = self.model_json["x"]
        i_port_axioms = []

        i_port_axioms.append(Axiom("tff","i_port_type","type", Constant("i_port : $tType")))
        i_port_axioms.append(Axiom("tff","num_rcvd_type", "type", Constant(f"num_rcvd : i_port > $int")))
        
        for pos, key in enumerate(in_ports):
            self.in_port_names.append(key)
            i_port_axioms.append(Axiom("tff",key,"type", Constant(f"{key} : i_port")))

            p_type = ""
            if (in_ports[key] in self.integers):
                p_type = "$int"
            elif (in_ports[key] == "bool"):
                p_type = "$o"
            elif (in_ports[key] in self.reals):
                p_type = "$real"
            else:
                assert False, f"{p_type} is an unsupported variable type"

            i_port_axioms.append(Axiom("tff",f"val_rcvd_{key}_type", "type", Constant(f"val_rcvd_{key} : {p_type}")))

        if (len(self.in_port_names) > 0):
            if (len(self.in_port_names) == 1):
                only_i_ports_f = Binary_Formula("! [IP : i_port]", Constant("IP"), Constant(self.in_port_names[0]), "==")
            elif (len(self.in_port_names) == 2):
                lhs = Binary_Formula("", Constant("IP"), Constant(self.in_port_names[0]), "==")
                rhs = Binary_Formula("", Constant("IP"), Constant(self.in_port_names[1]), "==")
                only_i_ports_f = Binary_Formula("! [IP : i_port]", lhs, rhs, "||")
            elif (len(self.in_port_names) > 2):
                lhs = Binary_Formula("", Constant("IP"), Constant(self.in_port_names[0]), "==")
                rhs = Binary_Formula("", Constant("IP"), Constant(self.in_port_names[1]), "==")
                only_i_ports_f = Binary_Formula("", lhs, rhs, "||")
                for i in range(2,len(self.in_port_names)):
                    rhs = Binary_Formula("", Constant("IP"), Constant(self.in_port_names[i]), "==")
                    if i == len(self.in_port_names):
                        only_i_ports_f = Binary_Formula("! [IP : i_port]", only_i_ports_f, rhs, "||")
                    else:
                        only_i_ports_f = Binary_Formula("", only_i_ports_f, rhs, "||")

            i_port_axioms.append(Axiom("tff","only_i_ports","axiom", only_i_ports_f))
        
        self.axioms.update({"i_port_axioms":i_port_axioms})
    
    '''
    Parses the JSON dictionary for the output port information and saves 
    it in tff axioms in the string
    '''
    def parse_o_ports(self):
        out_ports = self.model_json["y"]
        o_port_axioms = []

        o_port_axioms.append(Axiom("tff", "o_port_type", "type", Constant("o_port : $tType")))
        o_port_axioms.append(Axiom("tff",f"num_output_type", "type", Constant(f"num_output : o_port > $int")))

        for pos, key in enumerate(out_ports):
            self.out_port_names.append(key)
            o_port_axioms.append(Axiom("tff",key,"type", Constant(f"{key} : o_port")))

            p_type = ""
            if (out_ports[key] in self.integers):
                p_type = "$int"
            elif (out_ports[key] == "bool"):
                p_type = "$o"
            elif (out_ports[key] in self.reals):
                p_type = "$real"
            else:
                assert False, f"{p_type} is an unsupported variable type"

            o_port_axioms.append(Axiom("tff",f"val_output_{key}_type", "type", Constant(f"val_output_{key} : {p_type}")))

        if (len(self.out_port_names) > 0):
            if (len(self.out_port_names) == 1):
                only_o_ports_f = Binary_Formula("! [OP : o_port]", Constant("OP"), Constant(self.out_port_names[0]), "==")
            elif (len(self.out_port_names) == 2):
                lhs = Binary_Formula("", Constant("OP"), Constant(self.out_port_names[0]), "==")
                rhs = Binary_Formula("", Constant("OP"), Constant(self.out_port_names[1]), "==")
                only_o_ports_f = Binary_Formula("! [OP : o_port]", lhs, rhs, "||")
            elif (len(self.out_port_names) > 2):
                lhs = Binary_Formula("", Constant("OP"), Constant(self.out_port_names[0]), "==")
                rhs = Binary_Formula("", Constant("OP"), Constant(self.out_port_names[1]), "==")
                only_o_ports_f = Binary_Formula("", lhs, rhs, "||")
                for i in range(2,len(self.out_port_names)):
                    rhs = Binary_Formula("", Constant("OP"), Constant(self.out_port_names[i]), "==")
                    if i == len(self.out_port_names):
                        only_o_ports_f = Binary_Formula("! [OP : o_port]", only_o_ports_f, rhs, "||")
                    else:
                        only_o_ports_f = Binary_Formula("", only_o_ports_f, rhs, "||")

            o_port_axioms.append(Axiom("tff","only_o_ports","axiom", only_o_ports_f))

        self.axioms.update({"o_port_axioms":o_port_axioms})

    '''
    Recursively parses and generates axioms from the trans function dictionaries
    args: axiom_num = int, cond_list = list<string>, transition_function = dict<string: dict<>> or dict<string: string>, translation(int, list<string>, dict<string:string>) -> string
    returns: axiom_num = int, axiom = string
    '''

    def parse_devsmap_dict(self, axiom_num:int, cond_list, transition_function, axiom_type:str):
        #Assumes no dictionary will have different key-value types within itself
        if (len(transition_function) == 0) or isinstance(list(transition_function.values())[0], str):
            axiom = self.gen_delta_axiom(axiom_num, cond_list, transition_function, axiom_type)
            return axiom, axiom_num+1
        elif isinstance(list(transition_function.values())[0], dict):
            other_conds = []
            num = axiom_num
            for pos, key in enumerate(transition_function):
                if key.casefold() != "otherwise":
                    other_conds.append(key)
                    new_cond_list = cond_list.copy()
                    new_cond_list.append(key)
                    axiom, num = self.parse_devsmap_dict(num, new_cond_list, transition_function[key], axiom_type)
                    if axiom is None:
                        return None, num
                    else:
                        axiom_list = self.axioms[f"{axiom_type}_axioms"]
                        axiom_list.append(axiom)
                        self.axioms.update({f"{axiom_type}_axioms":axiom_list})
            if axiom_type != "lambda":
                other_conds = self.negate_conds(other_conds)
                other_conds.extend(cond_list.copy())
                if 'otherwise' in transition_function.keys():
                    axiom, num = self.parse_devsmap_dict(num, other_conds, transition_function['otherwise'], axiom_type)
                else:
                    axiom, num = self.parse_devsmap_dict(num, other_conds, {}, axiom_type)

                if axiom is None:
                    return None, num
                else:
                    axiom_list = self.axioms[f"{axiom_type}_axioms"]
                    axiom_list.append(axiom)
                    self.axioms.update({f"{axiom_type}_axioms":axiom_list})
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
    def gen_delta_axiom(self, axiom_num:int, cond_list, assignments_dict, axiom_type:str):
        implication = True
        if len(cond_list) > 0:
            new_cond_list = self.parse_clauses(cond_list)
            if (len(new_cond_list) > 1):
                lhs = self.build_CNF(Binary_Formula("",new_cond_list.pop(0),new_cond_list.pop(0),"&&"), new_cond_list)
            else:
                lhs = new_cond_list[0]
        elif len(cond_list) == 0:
            implication = False
        else:
            assert False, "the cond_list length cannot be less than 0"

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
        if implication:
            f1 = Binary_Formula("", lhs, rhs, "=>")
        else:
            f1 = rhs
        return Axiom('tff',f"{axiom_type}_axiom_{axiom_num}","axiom",f1)
    
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
        clause = clause.replace(" \\neg ", " != ")
        clause = clause.replace("\\neg", "!")
        clause = clause.replace("\\leq", "<=")
        clause = clause.replace("\\geq", ">=")
        clause = clause.replace("\\times", "*")
        
        if clause.startswith("!"):
            return Unary_Formula("",self.parse_clause(clause[1:]), "!")
        else:
            if clause.startswith("("):
                clause = clause[1:-1]
            lb = clause.find("(")
            if lb == -1:
                ops = clause.split(" ")
                if (len(ops) == 1):
                    return Constant(ops[0])
                elif (len(ops) == 3):
                    return Binary_Formula("",Constant(ops[0]), Constant(ops[2]), ops[1])
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
                lhs = "("+clause[:outside_start].strip()+")"
                rhs = "("+clause[outside_end:].strip()+")"
                return Binary_Formula("",self.parse_clause(lhs),self.parse_clause(rhs), clause[outside_start:outside_end+1])
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

        self.parse_devsmap_dict(0,["interal_transition == true"],delta_int,"delta_int")
    
    '''
    Parses the JSON dictionary for the external transition function
    information and saves it in tff axioms in the string
    '''
    def parse_delta_ext(self):
        delta_ext = self.model_json["delta_ext"]

        self.parse_devsmap_dict(0,["external_transition == true"],delta_ext,"delta_ext")

    def parse_delta_con(self):
        delta_con = self.model_json["delta_con"]

        self.parse_devsmap_dict(0,["confluence_transition = true"],delta_con,"delta_con")

    def parse_lambda(self):
        lambda_func = self.model_json["lambda"]
        if (len(lambda_func) == 1) and ("otherwise" in list(lambda_func.keys())[0].casefold()):
            assignments = lambda_func["otherwise"]
            lambda_func.pop("otherwise")
            lambda_func.update({"output == true" : assignments})
            self.parse_devsmap_dict(0,[],lambda_func,"lambda")
        else:
            self.parse_devsmap_dict(0,["output == true"],lambda_func,"lambda")

    def parse_ta(self):
        ta_func = self.model_json['ta']

        self.parse_devsmap_dict(0,[],ta_func,"ta")

if __name__ == "__main__":

    axiom_gen = Axiom_Generator('DEVSMap_Files/counter_atomic.json', 'DEVSMap_Files/counter_tester_init_state.json')
    axiom_gen.parse_state_vars()
    axiom_gen.parse_i_ports()
    axiom_gen.parse_o_ports()
    axiom_gen.parse_delta_int()
    axiom_gen.parse_delta_ext()
    axiom_gen.parse_delta_con()
    axiom_gen.parse_lambda()
    axiom_gen.parse_ta()
    axiom_gen.save("test")
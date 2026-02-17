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
    transition_function_names = ["delta_int", "delta_ext", "delta_con"]
    
    def __init__(self, model_file_path: str, model_name: str, init_state_file_path: str):
        #Getting atomic model file
        with open(model_file_path) as jfile:
            self.model_json = json.load(jfile)[model_name]

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

                pfile.write(self.add_devs_tff_types())

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

                    if section == "i_port_axioms":
                        if len(self.in_port_names) > 1:
                            pfile.write(self.add_distinct_port_axiom("i"))
                        pfile.write(self.add_func_result_always_pos("num_rcvd", "i_port", "IP", True))
                    elif section == "o_port_axioms":
                        if len(self.out_port_names) > 1:
                            pfile.write(self.add_distinct_port_axiom("o"))

                pfile.write(self.add_devs_tff_axioms())

        except Exception as e:
            os.remove(filename+".p")
            self.save(filename)

    def add_devs_tff_types(self):
        line = "\n%-----DEVS TFF TYPES\n\n"

        iTBool = ("tff(internal_transition_type,type,internal_transition : $o).\n\n")
        eTBool = ("tff(external_transition_type,type,external_transition : $o).\n\n")
        cTBool = ("tff(confluence_transition_type,type,confluence_transition : $o).\n\n")
        oBool = ("tff(output_type,type,output : $o).\n\n")
        taIn = ("tff(ta_in_type,type,ta_in : $real).\n\n")
        taOut = ("tff(ta_out_type,type,ta_out : $real).\n\n")
        taActual = ("tff(time_passed_type,type,time_passed : $real).\n\n")
        infinity = ("tff(infinity_type,type,infinity : $real).\n\n")
        input_rcvd = ("tff(input_rcvd_type,type,input_rcvd: $o).\n\n")

        line += iTBool
        line += eTBool
        line += cTBool
        line += oBool
        line += taIn
        line += taOut
        line += taActual
        line += infinity
        line += input_rcvd
        return line

    def add_devs_tff_axioms(self):
        line = ""
        line += "\n%-----DEVS TFF AXIOMS\n\n"

        input_rcvd_axiom = ("tff(input_was_rcvd,axiom,\n\t" +
                                "? [IP : i_port] :\n\t\t" +
                                    "num_rcvd(IP) != 0 => input_rcvd = $true).\n\n")
        
        input_not_rcvd_axiom = ("tff(input_not_rcvd,axiom,\n\t" +
                                "! [IP : i_port] :\n\t\t" +
                                    "num_rcvd(IP) = 0 => input_rcvd = $false).\n\n")

        iTAxiom = ("tff(internal_transition_occurred,axiom,\n\t" +
                        "((($greatereq(time_passed,ta_in)) & \n\t\t" +
                        "(~input_rcvd)) => (\n\t\t"+
                        "(internal_transition = $true) &\n\t\t" +
                        "(external_transition = $false) &\n\t\t" +
                        "(confluence_transition = $false) &\n\t\t" +
                        "(output = $true)))).\n\n")
        
        eTAxiom = ("tff(external_transition_occurred,axiom,\n\t" +
                        "((($less(time_passed,ta_in)) & \n\t\t" +
                        "(input_rcvd)) => (\n\t\t"+
                        "(internal_transition = $false) &\n\t\t" +
                        "(external_transition = $true) &\n\t\t" +
                        "(confluence_transition = $false) &\n\t\t" +
                        "(output = $false)))).\n\n")
                
        cTAxiom = ("tff(confluence_transition_occurred,axiom,\n\t" +
                        "((($greatereq(time_passed,ta_in)) & \n\t\t" +
                        "(input_rcvd)) => (\n\t\t"+
                        "(internal_transition = $false) &\n\t\t" +
                        "(external_transition = $false) &\n\t\t" +
                        "(confluence_transition = $true) &\n\t\t" +
                        "(output = $true)))).\n\n")
        
        nothing_changes_assignments = ""
        for pos, var in enumerate(self.state_var_names):
           nothing_changes_assignments += f"(next_{var} = {var})"
           if pos+1 != len(self.state_var_names):
               nothing_changes_assignments += " &\n\t\t"
        nothingAxiom = ("tff(nothing_happened_axiom,axiom,\n\t" +
                            "((($less(time_passed,ta_in)) &\n\t\t" +
                            "(~input_rcvd)) => (\n\t\t" +
                            "(ta_out = ta_in) &\n\t\t" +
                            nothing_changes_assignments +
                            "))).\n\n")
        
        infAxiom = ("tff(infinity_is_greater,axiom,\n\t" +
                        "infinity = $sum(time_passed,1.0)).\n\n")
        
        line += input_rcvd_axiom
        line += input_not_rcvd_axiom
        line += iTAxiom
        line += eTAxiom
        line += cTAxiom
        line += nothingAxiom
        line += infAxiom
        return line

    def add_distinct_port_axiom(self,portType : str) -> str:
        distinct_ports_axiom = (f"tff({portType}_ports_are_distinct,axiom,\n\t" + 
                                  "$distinct(")
        if portType.casefold() == "i":
            port_names = self.in_port_names
        elif portType.casefold() == "o":
            port_names = self.out_port_names
        else:
            assert False, "not a valid port type"
        for pos, port in enumerate(port_names):
            distinct_ports_axiom += port
            if (pos == len(port_names)-1):
                distinct_ports_axiom += ")).\n\n"
            else:
                distinct_ports_axiom += ","
        return distinct_ports_axiom

    def add_func_result_always_pos(self, funcName : str, funcType : str, variable : str, intOrReal : bool) -> str:
        if (intOrReal):
            zero = "0"
        else:
            zero = "0.0"
        
        always_pos_func_axiom = (f"tff(always_pos_{funcName},axiom,\n\t" +
                                    f"! [{variable} : {funcType}] :\n\t\t" +
                                        f"$greatereq({funcName}({variable}),{zero})).\n\n")
        return always_pos_func_axiom
    
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
            if (state[key] in self.integers) or (state[key] in self.reals):
                var_type = "$real"
            elif (state[key] == "bool"):
                var_type = "$o"
            else:
                assert False, f"{state[key]} variable type is unsupported"

            state_var_axioms.append(Axiom("tff", f"{key}_type", "type", Constant(f"{key} : {var_type}")))
            state_var_axioms.append(Axiom("tff",f"next_{key}_type", "type", Constant(f"next_{key} : {var_type}")))

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
            i_port_axioms.append(Axiom("tff",f"{key}_type","type", Constant(f"{key} : i_port")))

            p_type = ""
            if (in_ports[key] in self.integers) or (in_ports[key] in self.reals):
                p_type = "$real"
            elif (in_ports[key] == "bool"):
                p_type = "$o"
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
                    if i == len(self.in_port_names)-1:
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
            o_port_axioms.append(Axiom("tff",f"{key}_type","type", Constant(f"{key} : o_port")))

            p_type = ""
            if (out_ports[key] in self.integers) or (out_ports[key] in self.reals):
                p_type = "$real"
            elif (out_ports[key] == "bool"):
                p_type = "$o"
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
                    if i == len(self.out_port_names)-1:
                        only_o_ports_f = Binary_Formula("! [OP : o_port]", only_o_ports_f, rhs, "||")
                    else:
                        only_o_ports_f = Binary_Formula("", only_o_ports_f, rhs, "||")

            o_port_axioms.append(Axiom("tff","only_o_ports","axiom", only_o_ports_f))

        self.axioms.update({"o_port_axioms":o_port_axioms})

    '''
    Recursively parses and generates axioms from the trans function dictionaries
    args: axiom_num = int, cond_list = list<string>, devsmap_dict = dict<string: dict<>> or dict<string: string>, axiom_type = string
    returns: axiom_num = int, axiom = string
    '''

    def parse_devsmap_dict(self, axiom_num:int, cond_list, devsmap_dict, axiom_type:str):
        #Assumes no dictionary will have different key-value types within same tier
        if (len(devsmap_dict) == 0) or isinstance(list(devsmap_dict.values())[0], str):
            #If the dictionary is empty it will create a NULL axiom
            #If the dictionary has values that are strings, then an axiom declaring these strings are true will be generated
            axiom = self.gen_delta_axiom(axiom_num, cond_list, devsmap_dict, axiom_type)
            #The axiom is returned along with an increased number
            return axiom, axiom_num+1
        elif isinstance(list(devsmap_dict.values())[0], dict):
            #else if the dictionary has values that are dictionaries
            other_conds = [] #other_conds refers to conditions for the Otherwise axiom
            num = axiom_num #variable copy to ensure correct value is used
            for key in devsmap_dict:
                #For every condition, recursively access the variable assignments
                if key.casefold() != "otherwise": #If the condition is not the Otherwise condition
                    other_conds.append(key)
                    new_cond_list = cond_list.copy() #cond_list is the conditions from the next highest tier
                    new_cond_list.append(key) #This key's condition is appended to the cond list before recursively checking the next key-value pair
                    axiom, num = self.parse_devsmap_dict(num, new_cond_list, devsmap_dict[key], axiom_type) #NoneType axioms are returned to finish execution
                    if axiom is not None:
                        axiom_list = self.axioms[f"{axiom_type}_axioms"]
                        axiom_list.append(axiom)
                        self.axioms.update({f"{axiom_type}_axioms":axiom_list})
            if axiom_type != "lambda":
                if 'otherwise' in devsmap_dict.keys():
                    other_conds = self.negate_conds(other_conds)
                    other_conds.extend(cond_list.copy())
                    axiom, num = self.parse_devsmap_dict(num, other_conds, devsmap_dict['otherwise'], axiom_type)
                    if axiom is not None:
                        axiom_list = self.axioms[f"{axiom_type}_axioms"]
                        axiom_list.append(axiom)
                        self.axioms.update({f"{axiom_type}_axioms":axiom_list})
            return None, num
        else:
            assert False, "The devsmap dictionary keys and values can only ever be strings or nested dictionaries"

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
    The time advance must be calculated with the next state's variables, and not the current state's, so this
    function recursively accesses the uses of state variables, and adds the "next_" string to make it correct
    args: assignment = Constant | Formula
    returns: assignment = Constant | Formula
    '''
    def process_ta_values(self, assignment):
        if isinstance(assignment, Constant):
            if assignment.value in self.state_var_names:
                assignment.value = f"next_{assignment.value}"
            return assignment
        elif isinstance(assignment, Unary_Formula):
            assignment.operand = self.process_ta_values(assignment.operand)
            return assignment
        elif isinstance(assignment, Binary_Formula):
            assignment.lhs = self.process_ta_values(assignment.lhs)
            assignment.rhs = self.process_ta_values(assignment.rhs)
            return assignment
        else:
            assert False, "An assignment must be a Constant or a Formula"

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
        state_vars_missing = self.state_var_names.copy()
        if len(assignments_dict) > 0:
            
            for pos, key in enumerate(assignments_dict.keys()):
                if (axiom_type in self.transition_function_names):
                    if key in state_vars_missing:
                        state_vars_missing.remove(key)
                    else:
                        assert False, "for transition functions, the variable assignment must be for a state variable"
                assignment_values = self.parse_clauses([assignments_dict[key]])
                assignment_value = assignment_values[0]
                if (axiom_type == "ta"):
                    assignment_value = self.process_ta_values(assignment_value)
                    
                assignments.append(Binary_Formula("", Constant(f"next_{key}"), assignment_value, "=="))
            if (axiom_type in self.transition_function_names):
                for state_var in state_vars_missing:
                    assignments.append(Binary_Formula("",Constant(f"next_{state_var}"),Constant(f"{state_var}"), "=="))
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
            numbers = re.findall(r"\(?(-?\d+\.\d+|-?\d+)\)?", clause)
            for number in numbers:
                clause = clause.replace(number,f"constValue{number}")
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

        self.parse_devsmap_dict(0,["internal_transition == true"],delta_int,"delta_int")
    
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

    axiom_gen = Axiom_Generator('DEVSMap_Files/counter/counter_atomic.json', 'counter', 'DEVSMap_Files/counter/counter_tester_init_state.json')
    axiom_gen.parse_state_vars()
    axiom_gen.parse_i_ports()
    axiom_gen.parse_o_ports()
    axiom_gen.parse_delta_int()
    axiom_gen.parse_delta_ext()
    axiom_gen.parse_delta_con()
    axiom_gen.parse_lambda()
    axiom_gen.parse_ta()
    axiom_gen.save("counter_model")
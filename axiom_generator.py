import json
import re

integers = ["int", "unsigned int", "integer", "INT", "unsigned natural", "natural"]
reals = ["double", "float", "unsigned double", "unsigned float"]
conditionals = ["==", "!=", ">", "<", ">=", "<=", "&&", "||"]
conditionalsWOEquals = [">", "<", ">=", "<=", "-", "+", "*", "/"]
syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"product", "/":"$quotient", "&&":"&", "||":"|"}

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
                    

#filename = input("Enter atomic model filename: ")
filename = 'DEVSMap_Files/counter_atomic.json'
with open(filename) as jfile:
    model = json.load(jfile)["counter"]

filename = 'DEVSMap_Files/counter_tester_init_state.json'
with open(filename) as jfile:
    init_state = json.load(jfile)

with open("test.p", "x") as pfile:
    state = model["s"]
    
    pfile.write("%-----STATE VARIABLE DEFINITIONS\n")
    for pos, key in enumerate(state):
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
        pfile.write("tff("+key+", type, "+key+" : o_port).\n")
        define_set += "OP = "+key
        if (pos+1 != len(out_ports)):
            define_set += " | "
        else:
            define_set += ")).\n\n"
    pfile.write(define_set)

    delta_int = model["delta_int"]

    pfile.write("%-----INTERNAL TRANSITIONS\n")

    flat_delta_int = {}
    stack = [(delta_int, '')]

    while stack:
        c, p = stack.pop()
        
        strings = []
        for k, v in c.items():
            
            
            if isinstance(v, dict):
                new_key = f"{p}_{k}" if p else k
                stack.append((v, new_key)) 
            else:
                strings.append(k+ " = "+v)
        if (len(strings) > 0):
            flat_delta_int[p] = strings
        
    print(flat_delta_int)
    

        
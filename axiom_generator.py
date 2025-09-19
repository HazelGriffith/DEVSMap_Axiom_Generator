import json
import re

integers = ["int", "unsigned int", "integer", "INT", "unsigned natural", "natural"]
reals = ["double", "float", "unsigned double", "unsigned float"]
conditionals = ["==", "!=", ">", "<", ">=", "<=", "&&", "||"]
syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"product", "/":"$quotient"}



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
        pfile.write(line+"\n\n")

    pfile.write("")

    in_ports = model["x"]

    pfile.write("%-----INPUT PORT DEFINITIONS\n")
    pfile.write("tff(i_port_type, type, i_port : $tType).\n")
    define_set = "tff(only_i_ports, axiom,\n\t! [IP : i_port] :\n\t\t( "
    for pos, key in enumerate(in_ports):
        pfile.write("tff("+key+", type, "+key+" : i_port).\n")
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
    for pos, key in enumerate(delta_int):
        line = "tff("+key+"_deltaint, axiom,\n\t"
        if (pos+1 != len(delta_int)):
            condition = key.split()
            assert len(condition) == 3
            line += "( "+condition[0]+" "+syntaxMap[condition[1]]+" "+condition[2]+" -> "
        else:
            assert key == "otherwise"
            print("otherwise")
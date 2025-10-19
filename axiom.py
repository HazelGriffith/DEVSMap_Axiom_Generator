from abc import ABC, abstractmethod

infixConds = ["==", "!=", "&&", "||", "=", "&", "|", "=>", "\\lor"]
prefixConds = ["<", "<=", ">", ">=","--","-","+","*","/", "$less", "$lesseq", "$greater", "$greatereq", "$uminus", "$sum", "$difference", "$product", "$quotient"]
syntaxMap = {"true":"$true", "false":"$false", "==":"=", "<":"$less", "<=":"$lesseq", ">":"$greater", ">=":"$greatereq", "--":"$uminus", "+":"$sum", "-":"$difference", "*":"$product", "/":"$quotient", "&&":"&", "||":"|", "!=":"!=", "!":"~", "=>":"=>"}

class Constant:

    def __init__(self, value:str):
        self.value = value

    def translate(self):
        if (self.value.casefold() == "true"):
            self.value = "$true"
        elif (self.value.casefold() == "false"):
            self.value = "$false"
        elif self.value.endswith("_bagSize"):
            self.value = self.value.replace("_bagSize","")
            self.value = f"num_rcvd({self.value})"
        elif self.value.endswith("_bag"):
            self.value = self.value.replace("_bag","")
            self.value = f"val_rcvd_{self.value}"
        elif self.value.endswith(".addMessage"):
            self.value = self.value.replace(".addMessage","")
            if self.value.startswith("next_"):
                self.value = self.value.replace("next_","")
            self.value = f"val_output_{self.value}"
        elif self.value.endswith("time_advance"):
            if self.value.startswith("next_"):
                self.value = self.value.replace("next_","")
            self.value = "time_advance"
        elif self.value.startswith("constValue"):
            self.value = self.value.replace("constValue","")
            self.value = self.value.replace("_",".")


    def __str__(self) -> str:
        self.translate()
        return f"{self.value}"

class Formula(ABC):

    @abstractmethod
    def translate(self):
        pass

class Binary_Formula(Formula):

    def __init__(self, quantifier:str, lhs:Constant | Formula, rhs:Constant | Formula, operator:str):
        self.quantifier = quantifier

        if isinstance(lhs, Constant) or isinstance(lhs, Formula):
            self.lhs = lhs
        else:
            assert False, "lhs must be a Constant or Formula"

        if isinstance(rhs, Constant) or isinstance(rhs, Formula):
            self.rhs = rhs
        else:
            assert False, "rhs must be a Constant or Formula"

        self.operator = operator
        self.inUnary = False

    def isInUnary(self):
        self.inUnary = True

    def translate(self):
        try:
            self.operator = syntaxMap[self.operator]
        except Exception as e:
            print(e)
            assert False, f"The operator {self.operator} is unsupported"

    def __str__(self) -> str:
        self.translate()
        line = ""
        
        
        if self.quantifier != "":
            line += f"\n\t{self.quantifier} : "

        if isinstance(self.lhs, Constant) and self.inUnary == False:
            line += "\n\t\t"

        if self.operator in infixConds:
            line += f"({self.lhs} {self.operator} {self.rhs})"
        elif self.operator in prefixConds:
            line += f"{self.operator}({self.lhs},{self.rhs})"
        else: 
            assert False, f"The operator {self.operator} is unsupported"
        return line
        
class Unary_Formula(Formula):

    def __init__(self, quantifier:str, operand:Constant | Formula, operator:str):
        self.quantifier = quantifier
        
        if isinstance(operand, Constant) or isinstance(operand, Formula):
            self.operand = operand
        else:
            assert False, "operand must be a Constant or Formula"

        if isinstance(operand, Formula):
            self.operand.isInUnary()

        self.operator = operator
        self.inUnary = False

    def isInUnary(self):
        self.inUnary = True

    def translate(self):
        try:
            self.operator = syntaxMap[self.operator]
        except Exception as e:
            print(e)
            assert False, f"The operator {self.operator} is unsupported"

    def __str__(self) -> str:
        self.translate()
        line = ""
        if self.quantifier != "":
            line += f"\n\t{self.quantifier} : "

        if self.inUnary == False:
            line += "\n\t\t"
        line += f"{self.operator}{self.operand}"
        return line

class Axiom:

    def __init__(self, language:str, name:str, role:str, formula:Formula):
        self.language = language
        self.name = name
        self.role = role
        self.formula = formula

    def __str__(self) -> str:
        if (self.language == "tff"):
            line = f"tff({self.name},{self.role},({self.formula})).\n"
        else:
            assert False, "The selected language is unsupported"
        return line
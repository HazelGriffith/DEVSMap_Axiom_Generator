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
        elif self.value.endswith(".bagSize()"):
            self.value = self.value.replace(".bagSize()","")
            self.value = f"num_rcvd({self.value})"
        elif self.value.endswith(".bag(-1)"):
            self.value = self.value.replace(".bag(-1)","")
            self.value = f"val_rcvd({self.value})"

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
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator

    def translate(self):
        try:
            self.operator = syntaxMap[self.operator]
        except Exception as e:
            print(e)
            assert False, f"The operator {self.operator} is unsupported"

    def __str__(self) -> str:
        self.translate()
        if self.operator in infixConds:
            return f"{self.lhs} {self.operator} {self.rhs}"
        elif self.operator in prefixConds:
            return f"{self.operator}({self.lhs},{self.rhs})"
        else: 
            assert False, f"The operator {self.operator} is unsupported"
        
class Unary_Formula(Formula):

    def __init__(self, quantifier:str, operand:Constant | Formula, operator:str):
        self.quantifier = quantifier
        self.operand = operand
        self.operator = operator

    def translate(self):
        try:
            self.operator = syntaxMap[self.operator]
        except Exception as e:
            print(e)
            assert False, f"The operator {self.operator} is unsupported"

    def __str__(self) -> str:
        self.translate()
        return f"{self.operator}({self.operand})"

class Axiom:

    def __init__(self, language:str, name:str, role:str, formula:Formula):
        self.language = language
        self.name = name
        self.role = role
        self.formula = formula

    def __str__(self) -> str:
        if (self.language == "tff"):
            line = f"tff({self.name},{self.role},{self.formula})."
        else:
            assert False, "The selected language is unsupported"
        return line
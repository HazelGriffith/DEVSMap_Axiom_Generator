class Axiom:

    def __init__(self, language:str, name:str, role:str, formula:str):
        self.language = language
        self.name = name
        self.role = role
        self.formula = formula

    def print(self) -> str:
        if (self.language == "tff"):
            line = f"tff({self.name},{self.role},{self.formula})."
        else:
            assert False, "The selected language is unsupported"
        return line
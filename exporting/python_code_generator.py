class PythonCodeGenerator:
    """
    Since approx. 2004 `+=` for strings is a little bit faster than `"".join` due to in-place resizing
    """

    def __init__(self, indent_str='\t', line_break_str='\n'):
        self.indent_str = indent_str
        self.line_break_str = line_break_str
        self.__code = ""

    @property
    def code(self):
        return self.__code

    def add(self, code: str):
        self.__code += code

    def line_break(self):
        return self.line_break_str

    def indent(self):
        return self.indent_str

    def indent_block(self, code: str, indent_depth: int = 1):
        s = ""
        for l in code.split('\n'):
            s += self.indent() * indent_depth
            s += l

        return s

    @staticmethod
    def surrounded(code: str, left: str, right: str):
        return f"{left}{code}{right}"

    @staticmethod
    def par(code: str):
        return PythonCodeGenerator.surrounded(code, "(", ")")

    def func(self, func_name: str, arguments: str, code: str):
        s = "def {}{}:{}".format(
            func_name,
            self.par(','.join(arguments)),
            self.line_break(),
        )
        s += self.indent_block(code)

        return s

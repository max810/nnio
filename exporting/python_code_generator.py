from typing import Iterable


class PythonCodeGenerator:
    """
    Since approx. 2004 `+=` for strings is a little bit faster than `"".join` due to in-place resizing
    """

    def __init__(self, indent_str='\t', line_break_str='\n'):
        self.indent_str = indent_str
        self.line_break_str = line_break_str
        self.__code = ""

    @staticmethod
    def wrap_literal(value: str):
        try:
            # value is a valid python literal
            eval(str(value))
            return value
        except (NameError, SyntaxError):
            # adding quotes for possible string literals
            return f'"{value}"'

    @property
    def code(self):
        return self.__code

    def add(self, code: str):
        self.__code += code

    def add_line(self, code: str = ''):
        self.add(code)
        self.add(self.line_break())

    def add_block(self, code: str, indent_depth: int = 1):
        self.add(self.indent_block(code, indent_depth))

    def clear(self):
        self.__code = ""

    def __enter__(self):
        self.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

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

    @staticmethod
    def sequence(items: Iterable[str], trailing_comma: bool = False, trailing_space: bool = False):
        s = ", ".join(map(str, items))
        if trailing_comma and s:
            s += ","

        if trailing_space and s:
            s += " "

        return s

    def func(self, func_name: str, arguments: str, code: str):
        s = "def {}{}:{}".format(
            func_name,
            self.par(','.join(arguments)),
            self.line_break(),
        )
        s += self.indent_block(code)

        return s

    def call(self, callable_name: str, *args: str, **kwargs: str):
        s = callable_name
        all_arguments = self.sequence(
            args,
            trailing_comma=True,
            trailing_space=True
        )
        kw_list = ["{}={}".format(k, v) for k, v in kwargs.items()]
        all_arguments += self.sequence(kw_list)
        s += self.par(all_arguments)

        return s

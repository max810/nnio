from BLL.exporting.keras_generators import KerasSequentialGenerator, KerasFunctionalGenerator
from .python_code_generator import PythonCodeGenerator
from models import NetworkModel, FrameworkError


def export_model(model: NetworkModel, framework: str, line_break: str, indent: str, **kwargs):
    exporter = exporters[framework]
    cg = PythonCodeGenerator(indent_str=indent, line_break_str=line_break)

    # by passing **kwargs key-word arguments of method will be automatically mapped to those in dict
    return exporter(model, cg, **kwargs)


def export_keras(model: NetworkModel, cg: PythonCodeGenerator, **kwargs):
    use_sequential = kwargs.get('keras_prefer_sequential', False)

    if use_sequential:
        try:
            gen = KerasSequentialGenerator(model, cg)
            return gen.generate_code()
        except FrameworkError:
            # if the model is not Sequential, we will switch to Functional Api instead
            pass

    gen = KerasFunctionalGenerator(model, cg)

    return gen.generate_code()


exporters = {
    "keras": export_keras
}
KNOWN_FRAMEWORKS = list(exporters.keys())

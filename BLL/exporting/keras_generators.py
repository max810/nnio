from abc import ABC
from collections import deque, defaultdict
from typing import Dict

from .framework_code_generator import FrameworkCodeGenerator
from .python_code_generator import PythonCodeGenerator
from models import NetworkModel, FrameworkError, LayerTypes, Layer


class KerasGenerator(FrameworkCodeGenerator, ABC):
    def _parse_regularizer(self, regularizer_params: dict):
        return self.cg.call('l1_l2', l1=regularizer_params['l1'], l2=regularizer_params['l2'])

    def _generate_imports(self) -> str:
        s = "from keras.layers import "
        layers_types = set([l.type.value for l in self.model.layers])
        s += self.cg.par(self.cg.sequence(layers_types))
        s += self.cg.line_break()

        for l in self.model.layers:
            for k in l.params.keys():
                if str(k).endswith('regularizer'):
                    s += "from keras.regularizers import l1_l2" + self.cg.line_break()
                    break
            # breaking out of inner and outer loops
            else:
                continue
            break

        s += self.cg.line_break()

        return s


class KerasSequentialGenerator(KerasGenerator):
    def __init__(self, model: NetworkModel, cg: PythonCodeGenerator):
        if not self._is_sequential(model):
            raise FrameworkError("Model given is NOT sequential.")

        seq_model = self._to_sequential_format(model)
        super().__init__(seq_model, cg)

    @staticmethod
    def _to_sequential_format(model: NetworkModel):
        if model.layers[0].type == LayerTypes.Input:
            input_shape = model.layers[0].params['shape']
            model.layers[1].params['input_shape'] = input_shape
            model.layers.pop(0)

        return model

    @staticmethod
    def _is_sequential(model: NetworkModel):
        for l in model.layers:
            if len(l.outputs) > 1 or len(l.inputs) > 1:
                return False

        return True

    def _generate_imports(self) -> str:
        s = "from keras.models import Sequential" + self.cg.line_break()
        s += super()._generate_imports()

        return s

    def generate_code(self) -> str:
        with self.cg as cg:
            cg.add_line(self._generate_imports())
            name = cg.wrap_literal(self.model.name)

            cg.add_line(f"model = {cg.call('Sequential', name=name)}")

            l = self.model.layers[0]
            while True:
                params = l.params.copy()
                for k, v in params.items():
                    if str(k).endswith('regularizer'):
                        params[k] = self._parse_regularizer(v)
                    else:
                        params[k] = cg.wrap_literal(params[k])

                params['name'] = cg.wrap_literal(l.name)
                layer_code = cg.call(l.type.value, **params)
                cg.add_line("model.add" + cg.par(layer_code))

                if l.outputs:
                    l = l.outputs[0]
                else:
                    break

            cg.add_line()
            cg.add_line('''print("INPUT: {}, OUTPUT: {}".format(model.input_shape, model.output_shape))''')
            cg.add_line("model.summary()")

            return cg.code


class KerasFunctionalGenerator(KerasGenerator):
    def __init__(self, model: NetworkModel, cg: PythonCodeGenerator):
        func_model = self._to_functional_format(model)
        super().__init__(func_model, cg)

    @staticmethod
    def _to_functional_format(model: NetworkModel):
        input_layers = [l for l in model.layers if l.type == LayerTypes.Input]

        if not any(input_layers):
            first_layers = [l for l in model.layers if len(l.inputs) == 0]
            for l in first_layers:
                inp = Layer(
                    name=l.name + '_input',
                    inputs=[],
                    outputs=[l],
                    type=LayerTypes.Input,
                    params=dict(
                        shape=l.params['input_shape']
                    )
                )
                l.inputs.append(inp)
                del l.params['input_shape']
                model.layers.append(inp)

        return model

    def _generate_imports(self) -> str:
        s = "from keras.models import Model" + self.cg.line_break()
        s += super()._generate_imports()

        return s

    @staticmethod
    def _generate_variable_name(layer_type: LayerTypes, layer_depth: int, names_counter: Dict[str, int]):
        name = "{}_{}_{}".format(
            layer_type.value.lower(),
            layer_depth,
            names_counter[layer_type.value]
        )

        names_counter[layer_type.value] += 1

        return name

    def generate_code(self) -> str:
        with self.cg as cg:
            cg.add_line(self._generate_imports())
            name = cg.wrap_literal(self.model.name)

            input_layers = [l for l in self.model.layers if l.type == LayerTypes.Input]
            output_layers = [l for l in self.model.layers if not l.outputs]

            variable_names_counter = defaultdict(lambda: 0)  # only for generating variable names
            existing_tensor_variables = dict()  # for accessing tensor variables created earlier

            # breadth-first traverse of the model graph
            levels_of_layers_left = deque([input_layers])
            depth = 0
            while levels_of_layers_left:
                current_level_layers = levels_of_layers_left.popleft()
                next_level_layers = dict()  # dict not to include same layers (key by name) multiple times

                for l in current_level_layers:
                    params = l.params.copy()
                    for k, v in params.items():
                        if str(k).endswith('regularizer'):
                            params[k] = self._parse_regularizer(v)
                        else:
                            params[k] = cg.wrap_literal(params[k])

                    params['name'] = cg.wrap_literal(l.name)

                    layer_var_name = self._generate_variable_name(l.type, depth, variable_names_counter)
                    existing_tensor_variables[l.name] = layer_var_name
                    layer_line = "{} = {}".format(
                        layer_var_name,
                        cg.call(l.type, **params)
                    )

                    if l.inputs:
                        layer_inputs_var_names = [existing_tensor_variables[i.name] for i in l.inputs]
                        if len(layer_inputs_var_names) == 1:
                            layer_call_inputs_args = layer_inputs_var_names[0]
                        else:
                            layer_call_inputs_args = cg.list(cg.sequence(layer_inputs_var_names))

                        layer_line += cg.call('', layer_call_inputs_args)

                    if l.outputs:
                        for output in l.outputs:
                            next_level_layers[output.name] = output

                    cg.add_line(layer_line)

                if next_level_layers:
                    levels_of_layers_left.append(list(next_level_layers.values()))

                depth += 1

            model_inputs_args = [existing_tensor_variables[l.name] for l in input_layers]
            model_outputs_args = [existing_tensor_variables[l.name] for l in output_layers]

            if len(model_inputs_args) == 1:
                model_inputs_str = model_inputs_args[0]
            else:
                model_inputs_str = cg.list(cg.sequence(model_inputs_args))

            if len(model_outputs_args) == 1:
                model_outputs_str = model_outputs_args[0]
            else:
                model_outputs_str = cg.list(cg.sequence(model_outputs_args))

            cg.add_line()
            cg.add_line('model = ' + cg.call('Model', inputs=model_inputs_str, outputs=model_outputs_str, name=name))
            cg.add_line('''print("INPUT: {}, OUTPUT: {}".format(model.input_shape, model.output_shape))''')
            cg.add_line("model.summary()")

            return cg.code

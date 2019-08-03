from abc import ABC

from .framework_code_generator import FrameworkCodeGenerator


class KerasGenerator(FrameworkCodeGenerator, ABC):
    def _generate_imports(self) -> str:
        s = "from keras.layers import "
        layers_types = set([l.type.value for l in self.model.layers])
        s += self.cg.par(self.cg.sequence(layers_types))
        s += self.cg.line_break()

        return s


class KerasSequentialGenerator(KerasGenerator):
    def _generate_imports(self) -> str:
        s = super()._generate_imports()
        s += "from keras.models import Sequential" + self.cg.line_break()

        for l in self.model.layers:
            for k in l.params.keys():
                if str(k).endswith('regularizer'):
                    s += "from keras.regularizers import l1, l2, l1_l2" + self.cg.line_break()
                    break
            # breaking out of inner and outer loops
            else:
                continue
            break

        s += self.cg.line_break()

        return s

    def generate_code(self) -> str:
        with self.cg as cg:
            cg.add_line(self._generate_imports())
            name = cg.wrap_literal(self.model.name)

            cg.add_line(f"model = {cg.call('Sequential', name=name)}")

            for l in self.model.layers:
                params = l.params.copy()
                for k, v in params.items():
                    if str(k).endswith('regularizer'):
                        params[k] = cg.call(v['type'], v['l'])
                    else:
                        params[k] = cg.wrap_literal(params[k])
                layer_code = cg.call(l.type.value, **params)
                cg.add_line("model.add" + cg.par(layer_code))

            cg.add_line()
            cg.add_line('''print("INPUT: {}, OUTPUT: {}".format(model.input_shape, model.output_shape))''')
            cg.add_line("model.summary()")

            return cg.code


class KerasFunctionalGenerator(KerasGenerator):
    def generate_code(self) -> str:
        return "Not implemented"

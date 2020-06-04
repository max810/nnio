import enum
from collections import deque, OrderedDict
from datetime import datetime
from typing import List, Dict, Iterable
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DAL import db_models
from configs import SessionLocal

indents = {
    'tabs': "\t",
    "spaces_2": " " * 2,
    "spaces_4": " " * 4,
    "spaces_8": " " * 8,
}

line_breaks = {
    "crlf": "\r\n",
    "lf": "\n",
}


class FrameworkError(Exception):
    pass


def load_layers():
    sess: Session = SessionLocal()
    try:
        layers = [schema.layer_type for schema in sess.query(db_models.LayerSchema)]
        return layers
    finally:
        sess.close()


known_layers = load_layers()
LayerTypes = enum.Enum('LayerTypes', zip(known_layers, known_layers))


class LayerBase(BaseModel):
    name: str
    type: LayerTypes
    params: dict


class LayerData(LayerBase):
    inputs: List[str]


class Layer(LayerBase):
    inputs: List['Layer'] = []
    outputs: List['Layer'] = []

    @staticmethod
    def from_layer_data_empty(layer_data: LayerData):
        layer_attrs = layer_data.dict()
        layer_attrs['inputs'] = []
        layer_attrs['outputs'] = []

        return Layer(**layer_attrs)

    def __repr__(self):
        return f"{self.name}({self.type})"


Layer.update_forward_refs()


class ModelBase(BaseModel):
    name: str


class ArchitectureDataModel(ModelBase):
    date_created: datetime
    id: str
    layers: List[LayerData]


class NetworkModel(ModelBase):
    layers: List[Layer]

    def __init__(self, layers: List[Layer], name: str = "Model", **kwargs):
        kwargs['layers'] = layers
        kwargs['name'] = name
        super().__init__(**kwargs)

    @staticmethod
    def from_data_model(data_model: ArchitectureDataModel):
        return NetworkModel.from_data_layers(data_model.layers, data_model.name)

    @staticmethod
    def from_data_layers(layers_data: List[LayerData], name: str = "Model"):
        linked_layers = NetworkModel._link_layers(layers_data)

        return NetworkModel(name=name, layers=linked_layers)

    @staticmethod
    def _link_layers(layers: Iterable[LayerData]) \
            -> List[Layer]:

        output_layers: List[LayerData] = NetworkModel._find_outputs_layers(layers)
        layer_names = map(lambda x: x.name, layers)
        layers_data_lookup = dict(zip(layer_names, layers))
        existing_layers_lookup: Dict[str, Layer] = OrderedDict()
        layers_left = deque(output_layers)
        try:
            while layers_left:
                layer_data = layers_left.popleft()
                if layer_data.name not in existing_layers_lookup:
                    l = Layer.from_layer_data_empty(layer_data)
                    existing_layers_lookup[l.name] = l
                else:
                    l = existing_layers_lookup[layer_data.name]

                inputs = (layers_data_lookup[name] for name in layer_data.inputs)

                for i in inputs:
                    if i.name not in existing_layers_lookup:
                        li = Layer.from_layer_data_empty(i)
                        existing_layers_lookup[li.name] = li
                        layers_left.append(i)
                    else:
                        li = existing_layers_lookup[i.name]

                    li.outputs.append(l)
                    l.inputs.append(li)
        except KeyError as e:
            raise ValueError(f'Layer with name "{e.args[0]} does not exist, but is being referenced in the model."')

        return list(existing_layers_lookup.values())[::-1]

    @staticmethod
    def _find_outputs_layers(layers: Iterable[LayerBase]):
        input_names = set()
        for l in layers:
            input_names.update(l.inputs)

        return list(filter(lambda x: x.name not in input_names, layers))

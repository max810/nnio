from datetime import datetime
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel


class LayerTypes(str, Enum):
    Dense = "Dense"
    Input = "Input"
    BatchNormalization = "BatchNormalization"
    Dropout = "Dropout"
    Flatten = "Flatten"


class Layer(BaseModel):
    name: str
    type: LayerTypes
    inputs: List[str]
    params: Dict[str, Any]


class ArchitectureModel(BaseModel):
    date_created: datetime
    id: str
    layers: List[Layer]
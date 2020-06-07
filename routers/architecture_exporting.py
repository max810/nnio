import json
import logging
import enum
from collections import deque
from copy import copy, deepcopy
from json import JSONDecodeError

import starlette.status as status
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse
from fastapi import HTTPException, File, APIRouter, Query, Depends
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from pydantic import ValidationError as PydanticValidataionError

from BLL.exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents, FrameworkError, LayerTypes, Layer
from routers.admin import get_layers_schemas
from routers.common import get_db

router = APIRouter()

Frameworks = enum.Enum('Frameworks', zip(KNOWN_FRAMEWORKS, KNOWN_FRAMEWORKS))
LineBreaks = enum.Enum('LineBreaks', zip(line_breaks.keys(), line_breaks.keys()))
Indents = enum.Enum('Indents', zip(indents.keys(), indents.keys()))


@router.post("/export-from-json-file")
async def export_from_json_file(framework: Frameworks,
                                architecture_file: bytes = File(..., alias='architecture-file'),
                                line_break: LineBreaks = LineBreaks.lf,
                                indent: Indents = Indents.spaces_4,
                                keras_prefer_sequential: bool = False,
                                db: Session = Depends(get_db)):
    """
    Example request file: https://jsoneditoronline.org/?id=24ce7b7c485c42f7bec3c27a4f437afd
    """
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureDataModel(**architecture_dict)
    except (PydanticValidataionError, JSONDecodeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    return await export_from_json_body(framework, model, line_break, indent,
                                       keras_prefer_sequential=keras_prefer_sequential, db=db)


@router.post("/export-from-json-body")
async def export_from_json_body(framework: Frameworks,
                                model: ArchitectureDataModel,
                                line_break: LineBreaks = LineBreaks.lf,
                                indent: Indents = Indents.spaces_4,
                                keras_prefer_sequential: bool = False,
                                db: Session = Depends(get_db)):
    framework = framework.value.lower()

    line_break = line_break.value.lower()

    indent = indent.value.lower()

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)

    layer_schemas = json.loads(get_layers_schemas(db).body)
    validate_model(model, layer_schemas)
    try:
        net_model = NetworkModel.from_data_model(model)
    except ValueError as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Invalid model structure: ' + e.args[0],
        )
    validate_is_acyclic(deepcopy(net_model))
    line_break_str = line_breaks[line_break]
    indent_str = indents[indent]

    framework_specific_params = dict(
        keras_prefer_sequential=keras_prefer_sequential
    )

    try:
        source_code = export_model(net_model, framework, line_break_str, indent_str, **framework_specific_params)
        return PlainTextResponse(source_code)
    except FrameworkError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


def validate_model(model: ArchitectureDataModel, layer_schemas):
    if len(model.layers) < 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Model must have at least 1 layer."
        )

    input_layers = [l for l in model.layers if l.type == LayerTypes.Input]

    if len(input_layers) < 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Model must have at least 1 input layer\n' +
            '(dedicated layer(s) with type=Input and some `shape` parameter given.'
        )

    layers_schema_validation_errors = []
    for l in model.layers:
        try:
            validate(l.dict(), layer_schemas[l.type.name])
        except JsonSchemaValidationError as e:
            layers_schema_validation_errors.append(str(e))

    if len(layers_schema_validation_errors):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            '\n'.join(layers_schema_validation_errors)
        )


def validate_member_in(member, collection, member_name):
    if member not in collection:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"Unknown {member_name} {member}, known {member_name}s are: {collection}")


def validate_is_acyclic(net_model: NetworkModel):
    # https://www.cs.hmc.edu/~keller/courses/cs60/s98/examples/acyclic/

    leaf_nodes_left = deque()
    num_leafs = 0
    if len(net_model.layers) == 0:
        # kind of workaround (model will have 0 layers if no output layers are found)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Architecture contains a cycle.")

    for l in net_model.layers:
        if len(l.outputs) == 0:
            leaf_nodes_left.append(l)

    while len(leaf_nodes_left) != 0:
        l: Layer = leaf_nodes_left.popleft()
        num_leafs += 1

        for l_adj in l.inputs:
            # this is stupidly inefficient
            l_adj.outputs = [l_adj_out for l_adj_out in l_adj.outputs if l_adj_out.name != l.name]

            if len(l_adj.outputs) == 0:
                leaf_nodes_left.append(l_adj)

    if num_leafs != len(net_model.layers):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Architecture contains a cycle.")


def model_to_string(model: NetworkModel):
    res = ""
    for l in model.layers:
        if l.inputs:
            res += ", ".join(i.name for i in l.inputs)
            res += " -> "
        res += l.name
        if l.outputs:
            res += " -> "
            res += ", ".join(o.name for o in l.outputs)
        res += '<br>'

    return res

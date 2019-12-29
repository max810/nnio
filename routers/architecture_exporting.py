import json
import logging
import enum
import starlette.status as status
from starlette.responses import PlainTextResponse

from fastapi import HTTPException, File, APIRouter, Query
from pydantic import ValidationError

from BLL.exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents, FrameworkError, LayerTypes

router = APIRouter()

Frameworks = enum.Enum('Frameworks', zip(KNOWN_FRAMEWORKS, KNOWN_FRAMEWORKS))
LineBreaks = enum.Enum('LineBreaks', zip(line_breaks.keys(), line_breaks.keys()))
Indents = enum.Enum('Indents', zip(indents.keys(), indents.keys()))


@router.post("/export-from-json-file")
async def export_from_json_file(framework: Frameworks,
                                architecture_file: bytes = File(..., alias='architecture-file'),
                                line_break: LineBreaks = LineBreaks.lf,
                                indent: Indents = Indents.spaces_4,
                                keras_prefer_sequential: bool = False):
    """
    Example request file: https://jsoneditoronline.org/?id=24ce7b7c485c42f7bec3c27a4f437afd
    """
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureDataModel(**architecture_dict)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    return await export_from_json_body(framework, model, line_break, indent,
                                       keras_prefer_sequential=keras_prefer_sequential)


@router.post("/export-from-json-body")
async def export_from_json_body(framework: Frameworks,
                                model: ArchitectureDataModel,
                                line_break: LineBreaks = LineBreaks.lf,
                                indent: Indents = Indents.spaces_4,
                                keras_prefer_sequential: bool = False):
    framework = framework.value.lower()

    line_break = line_break.value.lower()

    indent = indent.value.lower()

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)

    validate_model(model)
    net_model = NetworkModel.from_data_model(model)

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


def validate_model(model: ArchitectureDataModel):
    if len(model.layers) < 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Model must have at least 1 layer."
        )

    input_layers = [l for l in model.layers if l.type == LayerTypes.Input]
    first_layers = [l for l in model.layers if len(l.inputs) == 0 and l.type != LayerTypes.Input]

    if len(input_layers) < 1 and len(first_layers) < 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Model must have at least 1 input layer\n' +
            '(either dedicated layer(s) with type=Input or just some layer(s) with inputs=[])'
        )

    for il in input_layers:
        if 'shape' not in il.params:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                'All type=Input layers must have `shape` property of type list defined in `params`'
            )

    for fl in first_layers:
        if 'input_shape' not in fl.params:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                'All `first` layers (with inputs=[]) must have `input_shape` property of type list defined in `params`'
            )


def validate_member_in(member, collection, member_name):
    if member not in collection:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"Unknown {member_name} {member}, known {member_name}s are: {collection}")


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

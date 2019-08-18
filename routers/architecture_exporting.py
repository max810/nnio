import json
import logging
import enum
from http import HTTPStatus
from starlette.responses import PlainTextResponse

from fastapi import HTTPException, File, APIRouter, Query
from pydantic import ValidationError

from BLL.exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents, FrameworkError

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
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    return await export_from_json_body(framework, model, line_break, indent,
                                       keras_prefer_sequential=keras_prefer_sequential)


@router.post("/export-from-json-body")
async def export_from_json_body(framework: Frameworks,
                                model: ArchitectureDataModel,
                                line_break: LineBreaks = LineBreaks.lf,
                                indent: Indents = Indents.spaces_4,
                                keras_prefer_sequential: bool = False):
    framework = framework.value.lower()
    # validate_member_in(framework, KNOWN_FRAMEWORKS, "framework")

    line_break = line_break.value.lower()
    # validate_member_in(line_break, line_breaks, "line_break")

    indent = indent.value.lower()
    # validate_member_in(indent, indents, "indent")

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)

    if len(model.layers) == 0:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Model should have at least 1 layer.")

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
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


def validate_member_in(member, collection, member_name):
    if member not in collection:
        raise HTTPException(HTTPStatus.BAD_REQUEST,
                            f"Unknown {member_name} {member}, known {member_name}s are: {collection}")


# @router.post("/test")
# async def test(**kwargs):
#     return kwargs
#

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

import json
import logging
from http import HTTPStatus
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from fastapi import HTTPException, File, APIRouter, Query
from pydantic import ValidationError

from BLL.exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents, FrameworkError

router = APIRouter()


@router.post("/export-from-json-file")
async def export_from_json_file(framework: str,
                                request: Request,
                                architecture_file: bytes = File(..., alias='architecture-file'),
                                line_break: str = "lf",
                                indent: str = "4_spaces"):
    """
    Example request file: https://jsoneditoronline.org/?id=24ce7b7c485c42f7bec3c27a4f437afd
    """
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureDataModel(**architecture_dict)
    except ValidationError as e:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    return await export_from_json_body(framework, request, model, line_break, indent)


@router.post("/export-from-json-body")
async def export_from_json_body(framework: str,
                                request: Request,
                                model: ArchitectureDataModel,
                                line_break: str = "lf",
                                indent: str = "4_spaces"):
    framework = framework.lower()
    validate_member_in(framework, KNOWN_FRAMEWORKS, "framework")

    line_break = line_break.lower()
    validate_member_in(line_break, line_breaks, "line_break")

    indent = indent.lower()
    validate_member_in(indent, indents, "indent")

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)
    net_model = NetworkModel.from_data_model(model)

    line_break_str = line_breaks[line_break]
    indent_str = indents[indent]

    # framework_specific_params = dict(request.query_params)
    for p in ['framework', 'line_break', 'indent']:
        if p in framework_specific_params:
            del framework_specific_params[p]

    try:
        source_code = export_model(net_model, framework, line_break_str, indent_str, **framework_specific_params)
        return PlainTextResponse(source_code)
    except FrameworkError as e:
        return HTTPException(HTTPStatus.BAD_REQUEST, str(e))


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

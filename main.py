import json
import logging
from http import HTTPStatus
from starlette.requests import Request
import uvicorn

from fastapi import FastAPI, HTTPException, File
from pydantic import ValidationError

from exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
print("STARTED")


@app.post("/architecture/export-from-json-file")
async def export_from_json_file(framework: str,
                                request: Request,
                                architecture_file: bytes = File(..., alias='architecture-file'),
                                line_break: str = line_breaks["lf"],
                                indent: str = indents["4_spaces"]):
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


@app.post("/architecture/export-from-json-body")
async def export_from_json_body(framework: str,
                                request: Request,
                                model: ArchitectureDataModel,
                                line_break: str = line_breaks["lf"],
                                indent: str = indents["4_spaces"]):
    framework = framework.lower()
    validate_member_in(framework, KNOWN_FRAMEWORKS, "framework")

    line_break = line_break.lower()
    validate_member_in(line_break, list(line_breaks), "line_break")

    indent = indent.lower()
    validate_member_in(indent, list(indents), "indent")

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)
    net_model = NetworkModel.from_data_model(model)

    return export_model(net_model, framework, line_break, indent, **request)


def validate_member_in(member, collection, member_name):
    if member not in collection:
        raise HTTPException(HTTPStatus.BAD_REQUEST,
                            f"Unknown {member_name} {member}, known {member_name}s are: {collection}")


@app.post("/test")
async def test(**kwargs):
    return kwargs


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

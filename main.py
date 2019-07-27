import json
import logging
from http import HTTPStatus

import uvicorn

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import ValidationError

from model_exporting import KNOWN_FRAMEWORKS
from models import ArchitectureDataModel, LayerData, NetworkModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
print("STARTED")


@app.post("/architecture/export-from-json-file")
async def export_from_json_file(framework: str,
                                architecture_file: bytes = File(..., alias='architecture-file')) -> str:
    """
    Example request file: https://jsoneditoronline.org/?id=24ce7b7c485c42f7bec3c27a4f437afd
    """
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureDataModel(**architecture_dict)
    except ValidationError as e:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    return await export_from_json_body(framework, model)  # export_model(framework, model)


@app.post("/architecture/export-from-json-body")
async def export_from_json_body(framework: str,
                                model: ArchitectureDataModel) -> str:
    framework = framework.lower()
    if framework not in KNOWN_FRAMEWORKS:
        raise HTTPException(HTTPStatus.BAD_REQUEST,
                            "Unknown framework {}, known frameworks are: {}".format(framework, KNOWN_FRAMEWORKS))

    logging.info(framework)
    logging.info(model.id)
    logging.info(model.date_created)
    net_model = NetworkModel.from_data_model(model)

    return dict(id=model.id, num_layers=len(model.layers), model=model_to_string(net_model))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


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

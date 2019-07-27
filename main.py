import json
import logging
from http import HTTPStatus

import uvicorn

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import ValidationError

from models import ArchitectureDataModel, LayerData, NetworkModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
print("STARTED")


@app.post("/architecture/load-from-json-file")
async def load_from_json_file(architecture_file: bytes = File(..., alias='architecture-file')):
    """
    Example request file: https://jsoneditoronline.org/?id=24ce7b7c485c42f7bec3c27a4f437afd
    """
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureDataModel(**architecture_dict)
    except ValidationError as e:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    logging.info(model.id)
    logging.info(model.date_created)
    net_model = NetworkModel.from_data_model(model)

    return dict(id=model.id, num_layers=len(model.layers), model=model_to_string(net_model))


@app.post("/architecture/load-from-json-body")
async def load_from_json_body(model: ArchitectureDataModel):
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

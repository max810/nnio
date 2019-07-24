import json
import logging
from http import HTTPStatus

import uvicorn

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import ValidationError

from models import ArchitectureModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
print("STARTED")


@app.post("/architecture/load-from-json-file")
async def load_from_json_file(architecture_file: bytes = File(..., alias='architecture-file')):
    # by using `bytes` the FastAPI will read the file and give me its content in `bytes`
    try:
        architecture_dict = json.loads(architecture_file)
        model = ArchitectureModel(**architecture_dict)
    except ValidationError as e:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid architecture file:\n{}".format(e))

    logging.info(model.id)
    logging.info(model.date_created)

    return dict(id=model.id, num_layers=len(model.layers))


@app.post("/architecture/load-from-json-body")
async def load_from_json_body(model: ArchitectureModel):
    logging.info(model.id)
    logging.info(model.date_created)

    return dict(id=model.id, num_layers=len(model.layers))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

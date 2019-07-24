import logging

from fastapi import FastAPI
from models import ArchitectureModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
print("STARTED")


@app.post("/architecture/load_from_json_body")
async def update_item(model: ArchitectureModel):
    # repr = format_architecture_model(model)
    logging.info(model.id)
    logging.info(model.date_created)
    return dict(id=model.id, num_layers=len(model.layers))


def format_architecture_model(model: ArchitectureModel):
    res = "\nMODEL {} from {}\n".format(model.id, model.date_created)
    res += "LAYERS:\n"
    for l in model.layers:
        res += "\tNAME {}, TYPE {}, INPUT_FROM {}\n".format(l.name, l.type, l.inputs)
        for k, v in l.params.items():
            res += "\t\t{}: {}\n".format(k, v)

    return res

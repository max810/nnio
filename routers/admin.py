import json
from pathlib import Path

from starlette.requests import Request
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from routers.common import oauth2_scheme, templates

router = APIRouter()


@router.get("/admin_page")
def get_admin_page(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/layers_schemas")
def get_layers_schemas(token: str = Depends(oauth2_scheme)):
    p_layer_schemas = Path('BLL/layer_schemas')
    layer_schemas = {}
    for p_schema in p_layer_schemas.glob("*.json"):
        schema = json.load(open(p_schema))
        layer_schemas[p_schema.stem] = schema

    # TODO - don't deserialize JSON, just combine strings and return
    return layer_schemas


@router.post("/save_layers_schemas")
def post_save_layers_schemas(body: dict, token: str = Depends(oauth2_scheme)):
    for layer_type, layer_schema in body.items():
        json.dump(layer_schema, open('BLL/layer_schemas_experimental/{}.json'.format(layer_type), 'wt'))

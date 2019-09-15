import json
from pathlib import Path

from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import Depends, FastAPI, HTTPException, APIRouter

from DAL import db_models
from routers.common import oauth2_scheme, templates
from routers.users import get_db

router = APIRouter()


@router.get("/admin_page")
def get_admin_page(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/layers_schemas")
def get_layers_schemas(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    layer_schemas = {}
    for schema in db.query(db_models.LayerSchema):
        layer_schemas[schema.layer_type] = json.loads(schema.layer_schema)

    return layer_schemas


@router.post("/save_layers_schemas")
def post_save_layers_schemas(body: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db.query(db_models.LayerSchema).delete()

    for layer_type, layer_schema in body.items():
        db.add(db_models.LayerSchema(layer_type, json.dumps(layer_schema)))
    db.commit()
    # json.dump(layer_schema, open('BLL/layer_schemas_experimental/{}.json'.format(layer_type), 'wt'))

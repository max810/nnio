import json

from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import Depends, APIRouter
from starlette.responses import Response

from DAL import db_models
from routers.common import oauth2_scheme, templates
from routers.users import get_db

router = APIRouter()


@router.get("/admin_page")
def get_admin_page(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/layers_schemas")
def get_layers_schemas(db: Session = Depends(get_db)):
    layer_schemas_strs = []
    # concatenating JSON representationsF from db (they are already serialized strings)
    for schema in db.query(db_models.LayerSchema):
        layer_schemas_strs.append('"{}": {}'.format(schema.layer_type, schema.layer_schema))

    res_str = ",".join(layer_schemas_strs)
    res_str = "{" + res_str + "}"

    return Response(content=res_str, media_type='application/json')


@router.post("/save_layers_schemas")
def post_save_layers_schemas(body: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db.query(db_models.LayerSchema).delete()

    for layer_type, layer_schema in body.items():
        db.add(db_models.LayerSchema(
            # such separators -> minified JSON (no spaces and no indents)
            layer_type=layer_type, layer_schema=json.dumps(layer_schema, separators=(',', ':'))
        ))
    db.commit()

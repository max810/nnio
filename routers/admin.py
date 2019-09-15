import json
from pathlib import Path

from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from starlette.responses import JSONResponse, Response

from DAL import db_models
from routers.common import oauth2_scheme, templates
from routers.users import get_db

router = APIRouter()


@router.get("/admin_page")
def get_admin_page(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/layers_schemas")
def get_layers_schemas(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    layer_schemas_strs = []
    for schema in db.query(db_models.LayerSchema):
        layer_schemas_strs.append('"{}": {}'.format(schema.layer_type, schema.layer_schema))

    res_str = ",".join(layer_schemas_strs)
    res_str = "{" + res_str + "}"

    return Response(content=res_str, media_type='application/json')


@router.post("/save_layers_schemas")
def post_save_layers_schemas(body: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db.query(db_models.LayerSchema).delete()

    for layer_type, layer_schema in body.items():
        #
        db.add(db_models.LayerSchema(layer_type, json.dumps(layer_schema, separators=(',', ':'))))
    db.commit()
    # json.dump(layer_schema, open('BLL/layer_schemas_experimental/{}.json'.format(layer_type), 'wt'))

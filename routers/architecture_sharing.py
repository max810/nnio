import json
import logging
import enum

import starlette.status as status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse
from fastapi import HTTPException, File, APIRouter, Query, Depends, Body
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from pydantic import ValidationError as PydanticValidataionError

from BLL.exporting.model_exporting import KNOWN_FRAMEWORKS, export_model
from DAL.architecture_repository import store_new_architecture, get_architecture_by_id
from models import ArchitectureDataModel, NetworkModel, line_breaks, indents, FrameworkError, LayerTypes
from routers.admin import get_layers_schemas
from routers.common import get_db

router = APIRouter()


@router.post("/share")
def share_architecture(model: ArchitectureDataModel,
                       db: Session = Depends(get_db)):
    arch_string = json.dumps(jsonable_encoder(model))
    arch_record = store_new_architecture(db, arch_string)

    return arch_record.id


@router.get("/load")
def load_arch(arch_id: int, db: Session = Depends(get_db)):
    return json.loads(get_architecture_by_id(db, arch_id).data)

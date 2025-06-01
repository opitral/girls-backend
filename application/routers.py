from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from application import schemas
from application.database import get_db
from application.models import Lang
from application.services import GirlService, ServiceService

girl_router = APIRouter(prefix="/girls", tags=["girls"])

@girl_router.get("/", response_model=List[schemas.GirlShort])
def get_girls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = GirlService(db)
    girls = service.get_girls(skip=skip, limit=limit)
    return girls


@girl_router.get("/{girl_id}", response_model=schemas.Girl)
def get_girl(
    girl_id: int,
    lang: Lang = Query(default=Lang.UK),
    db: Session = Depends(get_db)
):
    service = GirlService(db)
    girl = service.get_girl(girl_id)
    if girl is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Girl not found")

    girl_schema = schemas.Girl.model_validate(girl, from_attributes=True)
    girl_schema.lang = lang

    for service in girl_schema.services:
        service.lang = lang

    return girl_schema


service_router = APIRouter(prefix="/services", tags=["services"])

@service_router.get("/", response_model=List[schemas.Service])
def get_services(skip: int = 0, limit: int = 100, lang: Lang = Lang.UK, db: Session = Depends(get_db)):
    service = ServiceService(db)
    services = service.get_services(skip=skip, limit=limit)

    service_schemas = []
    for service in services:
        service_schema = schemas.Service.model_validate(service, from_attributes=True)
        service_schema.lang = lang
        service_schemas.append(service_schema)

    return service_schemas

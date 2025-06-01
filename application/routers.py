from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from application import schemas
from application.database import get_db
from application.models import Lang
from application.services import GirlService, ServiceService, SortBy

girl_router = APIRouter(prefix="/girls", tags=["girls"])

@girl_router.get("/", response_model=List[schemas.GirlShort])
def get_girls(
        min_age: int = Query(default=18, ge=18, le=80),
        max_age: int = Query(default=80, gt=18, le=80),
        min_height: int = Query(default=150, ge=150, le=200),
        max_height: int = Query(default=200, gt=150, le=200),
        min_weight: int = Query(default=40, ge=40, le=100),
        max_weight: int = Query(default=100, gt=40, le=100),
        min_breast: float = Query(default=0.0, ge=0.0, le=7.0),
        max_breast: float = Query(default=7.0, gt=0.0, le=7.0),
        min_price: int = Query(default=1000, ge=1000, le=15000),
        max_price: int = Query(default=15000, gt=1000, le=15000),
        service_ids: List[int] = Query(default=None),
        sort_by: SortBy = Query(default=SortBy.DEFAULT),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    service = GirlService(db)
    girls = service.get_girls(
        skip=skip,
        limit=limit,
        age_min=min_age,
        age_max=max_age,
        height_min=min_height,
        height_max=max_height,
        weight_min=min_weight,
        weight_max=max_weight,
        breast_min=min_breast,
        breast_max=max_breast,
        price_min=min_price,
        price_max=max_price,
        service_ids=service_ids,
        sort_by=sort_by
    )
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
def get_services(
    skip: int = 0,
    limit: int = 100,
    lang: Lang = Lang.UK,
    db: Session = Depends(get_db)
):
    service = ServiceService(db)
    services = service.get_services(
        skip=skip,
        limit=limit
    )

    service_schemas = []
    for service in services:
        service_schema = schemas.Service.model_validate(service, from_attributes=True)
        service_schema.lang = lang
        service_schemas.append(service_schema)

    return service_schemas

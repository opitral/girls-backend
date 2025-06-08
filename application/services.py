from datetime import date, timedelta
from enum import Enum
from typing import Optional

from sqlalchemy.orm import Session

from application import models, schemas
from application.models import Girl


class SortBy(str, Enum):
    DEFAULT = "default"
    PRICE_UP = "price_up"
    PRICE_DOWN = "price_down"
    AGE_UP = "age_up"
    AGE_DOWN = "age_down"
    WEIGHT_UP = "weight_up"
    WEIGHT_DOWN = "weight_down"
    BUST_UP = "bust_up"
    BUST_DOWN = "bust_down"


class GirlService:
    def __init__(self, db: Session):
        self.db = db

    def get_girls(
        self,
        skip: int = 0,
        limit: int = 100,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        height_min: Optional[int] = None,
        height_max: Optional[int] = None,
        weight_min: Optional[int] = None,
        weight_max: Optional[int] = None,
        breast_min: Optional[float] = None,
        breast_max: Optional[float] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        service_ids: Optional[list[int]] = None,
        sort_by: SortBy = SortBy.DEFAULT,
    ) -> list[type[Girl]]:

        query = self.db.query(models.Girl)

        if age_min is not None:
            max_birth_date = date.today() - timedelta(days=age_min * 365)
            query = query.filter(models.Girl.birth_date <= max_birth_date)
        if age_max is not None:
            min_birth_date = date.today() - timedelta(days=age_max * 365)
            query = query.filter(models.Girl.birth_date >= min_birth_date)

        if height_min is not None:
            query = query.filter(models.Girl.height >= height_min)
        if height_max is not None:
            query = query.filter(models.Girl.height <= height_max)

        if weight_min is not None:
            query = query.filter(models.Girl.weight >= weight_min)
        if weight_max is not None:
            query = query.filter(models.Girl.weight <= weight_max)

        if breast_min is not None:
            query = query.filter(models.Girl.breast_size >= breast_min)
        if breast_max is not None:
            query = query.filter(models.Girl.breast_size <= breast_max)

        if service_ids:
            query = query.join(models.GirlService).filter(models.GirlService.service_id.in_(service_ids))

        if sort_by == SortBy.AGE_UP:
            query = query.order_by(models.Girl.birth_date.desc())
        elif sort_by == SortBy.AGE_DOWN:
            query = query.order_by(models.Girl.birth_date.asc())
        elif sort_by == SortBy.WEIGHT_UP:
            query = query.order_by(models.Girl.weight.asc())
        elif sort_by == SortBy.WEIGHT_DOWN:
            query = query.order_by(models.Girl.weight.desc())
        elif sort_by == SortBy.BUST_UP:
            query = query.order_by(models.Girl.breast_size.asc())
        elif sort_by == SortBy.BUST_DOWN:
            query = query.order_by(models.Girl.breast_size.desc())
        else:
            query = query.order_by(models.Girl.id.asc())

        girls = query.offset(skip).limit(limit).all()

        if price_min is not None:
            girls_price_min = []
            for girl in girls:
                if girl.min_price >= price_min:
                    girls_price_min.append(girl)
            girls = girls_price_min

        if price_max is not None:
            girls_price_max = []
            for girl in girls:
                if girl.min_price <= price_max:
                    girls_price_max.append(girl)
            girls = girls_price_max

        if sort_by == SortBy.PRICE_UP:
            girls.sort(key=lambda x: x.min_price)

        elif sort_by == SortBy.PRICE_DOWN:
            girls.sort(key=lambda x: x.min_price, reverse=True)

        return girls


    def get_girl(self, girl_id: int) -> models.Girl | None:
        return self.db.query(models.Girl).filter(models.Girl.id == girl_id).first()

    def create_girl(self, girl: schemas.GirlCreate) -> models.Girl:
        db_girl = models.Girl(**girl.model_dump())
        self.db.add(db_girl)
        self.db.commit()
        self.db.refresh(db_girl)
        return db_girl

    def update_girl(self, girl_id: int, girl: schemas.GirlCreate) -> models.Girl:
        db_girl = self.get_girl(girl_id)
        if db_girl:
            for key, value in girl.model_dump().items():
                setattr(db_girl, key, value)
            self.db.commit()
            self.db.refresh(db_girl)
        return db_girl

    def delete_girl(self, girl_id: int) -> models.Girl:
        db_girl = self.get_girl(girl_id)
        if db_girl:
            self.db.delete(db_girl)
            self.db.commit()
        return db_girl


class ServiceService:
    def __init__(self, db: Session):
        self.db = db

    def get_services(self) -> list[type[models.Service]]:
        return self.db.query(models.Service).all()

    def get_service(self, service_id: int) -> models.Service | None:
        return self.db.query(models.Service).filter(models.Service.id == service_id).first()

    def create_service(self, service: schemas.ServiceCreate) -> models.Service:
        db_service = models.Service(**service.model_dump())
        self.db.add(db_service)
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def update_service(self, service_id: int, service: schemas.ServiceCreate) -> models.Service:
        db_service = self.get_service(service_id)
        if db_service:
            for key, value in service.model_dump().items():
                setattr(db_service, key, value)
            self.db.commit()
            self.db.refresh(db_service)
        return db_service

    def delete_service(self, service_id: int) -> models.Service:
        db_service = self.get_service(service_id)
        if db_service:
            self.db.delete(db_service)
            self.db.commit()
        return db_service

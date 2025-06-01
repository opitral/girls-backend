from sqlalchemy.orm import Session

from application import models, schemas


class GirlService:
    def __init__(self, db: Session):
        self.db = db

    def get_girls(self, skip: int = 0, limit: int = 100) -> list[type[models.Girl]]:
        return self.db.query(models.Girl).offset(skip).limit(limit).all()

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

    def get_services(self, skip: int = 0, limit: int = 100) -> list[type[models.Service]]:
        return self.db.query(models.Service).offset(skip).limit(limit).all()

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
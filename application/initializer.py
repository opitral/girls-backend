import datetime
import logging
from pathlib import Path

from application.database import SessionLocal
from application.models import BodyType, BreastType, HairColor, Photo, Service, Price
from application.schemas import ServiceCreate, GirlCreate
from application.services import ServiceService, GirlService

logger = logging.getLogger(__name__)


class Initializer:
    def __init__(self):
        self.db = SessionLocal()
        self.files = self.find_json_files()

    @staticmethod
    def find_json_files() -> dict[str, Path]:
        directory = Path(__file__).parent.parent / "resources" / "init_data"
        json_files = list(directory.glob("*.json"))
        files = {}
        for file in json_files:
            files[file.name.split(".")[0]] = file
        return files

    @staticmethod
    def json_to_dict(file_path: Path) -> dict:
        import json
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def dict_to_service(data: dict) -> ServiceCreate:
        return ServiceCreate(
            order=data.get("order"),
            name_ua=data.get("name_ua"),
            name_ru=data.get("name_ru"),
            name_en=data.get("name_en")
        )

    def init_service(self):
        service_service = ServiceService(self.db)

        if not service_service.get_services(limit=1):
            if self.files.get("services"):
                services_data = self.json_to_dict(self.files["services"])
                for service in services_data:
                    new_service = self.dict_to_service(service)
                    service_service.create_service(new_service)
                    logger.info(f"Service '{new_service.name_en}' initialized.")
        else:
            logger.info("Services already initialized, skipping.")

    @staticmethod
    def dict_to_girl_create(data: dict) -> GirlCreate:
        return GirlCreate(
            name=data.get("name"),
            birth_date=datetime.date.fromisoformat(data.get("birth_date")),
            phone=data.get("phone"),
            height=data.get("height"),
            weight=data.get("weight"),
            breast_size=data.get("breast_size"),
            hair_color=HairColor(data.get("hair_color")),
            ethnicity= data.get("ethnicity"),
            body_type=BodyType(data.get("body_type")),
            breast_type=BreastType(data.get("breast_type")),
            has_tattoo=data.get("has_tattoo"),
            has_piercing=data.get("has_piercing"),
            is_verified=data.get("is_verified"),
            description_ua=data.get("description_ua"),
            description_ru=data.get("description_ru"),
            description_en=data.get("description_en")
        )

    @staticmethod
    def dict_to_photos(data: dict, girl_id: int) -> list[Photo]:
        photos = []
        for photo in data.get("photos", []):
            photos.append(Photo(
                file_path=photo.get("file_path"),
                order=photo.get("order"),
                girl_id=girl_id
            ))
        return photos

    @staticmethod
    def dict_to_prices(data: dict, girl_id: int) -> list[Price]:
        prices = []
        for price in data.get("prices", []):
            prices.append(Price(
                hours=price.get("hours"),
                current_cost=price.get("current_cost"),
                old_cost=price.get("old_cost"),
                girl_id=girl_id
            ))
        return prices

    def dict_to_services(self, data: dict) -> list[Service]:
        service_service = ServiceService(self.db)
        services = []
        for service_id in data.get("services", []):
            service = service_service.get_service(service_id)
            if service:
                services.append(service)
        return services

    def init_girls(self):
        girl_service = GirlService(self.db)

        if not girl_service.get_girls(limit=1):
            if self.files.get("girls"):
                girls_data = self.json_to_dict(self.files["girls"])
                for girl_data in girls_data:
                    new_girl = girl_service.create_girl(self.dict_to_girl_create(girl_data))
                    new_photos = self.dict_to_photos(girl_data, new_girl.id)
                    new_prices = self.dict_to_prices(girl_data, new_girl.id)
                    new_services = self.dict_to_services(girl_data)
                    new_girl.photos.extend(new_photos)
                    new_girl.prices.extend(new_prices)
                    new_girl.services.extend(new_services)
                    self.db.add(new_girl)
                    self.db.commit()

    def init_all(self):
        if self.files.get("services"):
            self.init_service()
        if self.files.get("girls"):
            self.init_girls()

    def __del__(self):
        self.db.close()
        logger.info("Database session closed.")

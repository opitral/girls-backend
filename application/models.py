from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, Date, String, Float, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from application.database import Base


class Lang(str, PyEnum):
    UK = "uk"
    RU = "ru"
    EN = "en"


class HairColor(str, PyEnum):
    BLONDE = "blonde"
    BRUNETTE = "brunette"
    FAIR = "fair"
    REDHEAD = "redhead"
    BROWN = "brown"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "blonde": {Lang.UK: "Блондинка", Lang.RU: "Блондинка", Lang.EN: "Blondes"},
            "brunette": {Lang.UK: "Брюнетка", Lang.RU: "Брюнетка", Lang.EN: "Brunettes"},
            "fair": {Lang.UK: "Русява", Lang.RU: "Русая", Lang.EN: "Fair-haired"},
            "redhead": {Lang.UK: "Руда", Lang.RU: "Рыжая", Lang.EN: "Redheads"},
            "brown": {Lang.UK: "Шатенка", Lang.RU: "Шатенка", Lang.EN: "Brown-haired"},
        }
        return translations[self.value].get(lang, self.value)


class Ethnicity(str, PyEnum):
    ASIAN = "asian"
    MULATTO = "mulatto"
    SLAVIC = "slavic"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "asian": {Lang.UK: "Азіатка", Lang.RU: "Азиатка", Lang.EN: "Asians"},
            "mulatto": {Lang.UK: "Мулатка", Lang.RU: "Мулатка", Lang.EN: "Mulatto"},
            "slavic": {Lang.UK: "Слов'янка", Lang.RU: "Славянка", Lang.EN: "Slavic"},
        }
        return translations[self.value].get(lang, self.value)


class BodyType(str, PyEnum):
    SLIM = "slim"
    FIT = "fit"
    SPORT = "sport"
    DENSE = "dense"
    FAT = "fat"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "slim": {Lang.UK: "Худа", Lang.RU: "Худая", Lang.EN: "Slim"},
            "fit": {Lang.UK: "Струнка", Lang.RU: "Стройная", Lang.EN: "Fit"},
            "sport": {Lang.UK: "Спортивна", Lang.RU: "Спортивная", Lang.EN: "Sporty"},
            "dense": {Lang.UK: "Щільна", Lang.RU: "Плотная", Lang.EN: "Dense"},
            "fat": {Lang.UK: "Товста", Lang.RU: "Полная", Lang.EN: "Fat"},
        }
        return translations[self.value].get(lang, self.value)


class BreastType(str, PyEnum):
    NATURAL = "natural"
    SILICONE = "silicone"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "natural": {
                Lang.UK: "Натуральні",
                Lang.RU: "Натуральная",
                Lang.EN: "Natural",
            },
            "silicone": {
                Lang.UK: "Силіконова",
                Lang.RU: "Силиконовая",
                Lang.EN: "Silicone",
            },
        }
        return translations[self.value].get(lang, self.value)


class Girl(Base):
    __tablename__ = "girls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String(13), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    breast_size = Column(Float, nullable=False)
    hair_color = Column(Enum(HairColor), nullable=False)
    ethnicity = Column(Enum(Ethnicity), nullable=False)
    body_type = Column(Enum(BodyType), nullable=False)
    breast_type = Column(Enum(BreastType), nullable=False)
    has_tattoo = Column(Boolean, default=False)
    has_piercing = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    description_ua = Column(String(512))
    description_ru = Column(String(512))
    description_en = Column(String(512))

    photos = relationship("Photo", back_populates="girl")
    prices = relationship("Price", back_populates="girl")
    services = relationship("GirlService", back_populates="girl")

    def get_description(self, lang: Lang) -> str | None:
        if lang == Lang.UK:
            return self.description_ua or None
        elif lang == Lang.RU:
            return self.description_ru or None
        elif lang == Lang.EN:
            return self.description_en or None
        return None

    @property
    def min_price(self) -> int:
        if self.prices:
            return min(price.current_cost for price in self.prices)
        return 0


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(256), nullable=False)
    order = Column(Integer, nullable=False)
    girl_id = Column(Integer, ForeignKey("girls.id"))

    girl = relationship("Girl", back_populates="photos")


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    hours = Column(Integer, nullable=False)
    current_cost = Column(Integer, nullable=False)
    old_cost = Column(Integer)
    girl_id = Column(Integer, ForeignKey("girls.id"))

    girl = relationship("Girl", back_populates="prices")


class GirlService(Base):
    __tablename__ = "girl_services"

    girl_id = Column(Integer, ForeignKey("girls.id"), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"), primary_key=True)
    additional_cost = Column(Integer)

    girl = relationship("Girl", back_populates="services")
    service = relationship("Service", back_populates="girl_services")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name_ua = Column(String(32), nullable=False)
    name_ru = Column(String(32), nullable=False)
    name_en = Column(String(32), nullable=False)
    order = Column(Integer, nullable=False)

    girl_services = relationship("GirlService", back_populates="service")

    def get_name(self, lang: Lang) -> str:
        if lang == Lang.UK:
            return self.name_ua
        elif lang == Lang.RU:
            return self.name_ru
        elif lang == Lang.EN:
            return self.name_en
        return self.name_ua

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
            "blonde": {Lang.UK: "Блондинки", Lang.RU: "Блондинки", Lang.EN: "Blondes"},
            "brunette": {Lang.UK: "Брюнетки", Lang.RU: "Брюнетки", Lang.EN: "Brunettes"},
            "fair": {Lang.UK: "Русяві", Lang.RU: "Русые", Lang.EN: "Fair-haired"},
            "redhead": {Lang.UK: "Руді", Lang.RU: "Рыжие", Lang.EN: "Redheads"},
            "brown": {Lang.UK: "Шатенки", Lang.RU: "Шатенки", Lang.EN: "Brown-haired"},
        }
        return translations[self.value].get(lang, self.value)


class Ethnicity(str, PyEnum):
    ASIAN = "asian"
    MULATTO = "mulatto"
    SLAVIC = "slavic"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "asian": {Lang.UK: "Азіатки", Lang.RU: "Азиатки", Lang.EN: "Asians"},
            "mulatto": {Lang.UK: "Мулатки", Lang.RU: "Мулатки", Lang.EN: "Mulatto"},
            "slavic": {Lang.UK: "Слов'янки", Lang.RU: "Славянки", Lang.EN: "Slavic"},
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
            "slim": {Lang.UK: "Худі", Lang.RU: "Худые", Lang.EN: "Slim"},
            "fit": {Lang.UK: "Стрункі", Lang.RU: "Стройные", Lang.EN: "Fit"},
            "sport": {Lang.UK: "Спортивні", Lang.RU: "Спортивные", Lang.EN: "Sporty"},
            "dense": {Lang.UK: "Щільні", Lang.RU: "Плотные", Lang.EN: "Dense"},
            "fat": {Lang.UK: "Товсті", Lang.RU: "Полные", Lang.EN: "Fat"},
        }
        return translations[self.value].get(lang, self.value)


class BreastType(str, PyEnum):
    NATURAL = "natural"
    SILICONE = "silicone"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "natural": {
                Lang.UK: "Натуральна грудь",
                Lang.RU: "Натуральная грудь",
                Lang.EN: "Natural breast",
            },
            "silicone": {
                Lang.UK: "Силіконова грудь",
                Lang.RU: "Силиконовая грудь",
                Lang.EN: "Silicone breast",
            },
        }
        return translations[self.value].get(lang, self.value)


class City(str, PyEnum):
    KYIV = "kyiv"

    def get_translation(self, lang: Lang) -> str:
        translations = {
            "kyiv": {Lang.UK: "Київ", Lang.RU: "Киев", Lang.EN: "Kyiv"},
        }
        return translations[self.value].get(lang, self.value)


class Girl(Base):
    __tablename__ = "girls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False)
    birth_date = Column(Date, nullable=False)
    city = Column(Enum(City), nullable=False)
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
    services = relationship("Service", secondary="girl_services", back_populates="girls")

    def get_description(self, lang: Lang) -> str | None:
        if lang == Lang.UK:
            return self.description_ua or None
        elif lang == Lang.RU:
            return self.description_ru or None
        elif lang == Lang.EN:
            return self.description_en or None
        return None

    def get_min_price(self) -> int | None:
        if self.prices:
            return min(price.current_cost for price in self.prices)
        return None


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


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name_ua = Column(String(32), nullable=False)
    name_ru = Column(String(32), nullable=False)
    name_en = Column(String(32), nullable=False)
    order = Column(Integer, nullable=False)

    girls = relationship("Girl", secondary="girl_services", back_populates="services")

    def get_name(self, lang: Lang) -> str:
        if lang == Lang.UK:
            return self.name_ua
        elif lang == Lang.RU:
            return self.name_ru
        elif lang == Lang.EN:
            return self.name_en
        return self.name_ua

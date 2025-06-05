from datetime import date
from typing import Optional, List

from pydantic import BaseModel, computed_field, Field

from .models import HairColor, Ethnicity, BodyType, BreastType, Lang


def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


class GirlBase(BaseModel):
    name: str
    birth_date: date
    phone: str
    height: int
    weight: int
    breast_size: float
    hair_color: HairColor
    ethnicity: Ethnicity
    body_type: BodyType
    breast_type: BreastType
    has_tattoo: bool = False
    has_piercing: bool = False
    is_verified: bool = False
    description_ua: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None


class GirlCreate(GirlBase):
    pass


class PhotoBase(BaseModel):
    file_path: str
    order: int


class PhotoCreate(PhotoBase):
    girl_id: int


class Photo(PhotoBase):
    id: int = Field(exclude=True)
    girl_id: int = Field(exclude=True)

    class Config:
        from_attributes = True


class PriceBase(BaseModel):
    hours: int
    current_cost: int
    old_cost: Optional[int] = None


class PriceCreate(PriceBase):
    girl_id: int


class Price(PriceBase):
    id: int = Field(exclude=True)
    girl_id: int = Field(exclude=True)

    class Config:
        from_attributes = True


class ServiceBase(BaseModel):
    name_ua: str
    name_ru: str
    name_en: str
    order: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int
    lang: Lang = Field(default=Lang.UK, exclude=True)

    name_ua: str = Field(exclude=True)
    name_ru: str = Field(exclude=True)
    name_en: str = Field(exclude=True)

    @computed_field
    def name_localized(self) -> str:
        if self.lang == Lang.UK:
            return self.name_ua
        elif self.lang == Lang.RU:
            return self.name_ru
        elif self.lang == Lang.EN:
            return self.name_en
        return self.name_ua

    class Config:
        from_attributes = True


class GirlServiceBase(BaseModel):
    girl_id: int
    service_id: int
    additional_cost: Optional[int] = None


class GirlService(GirlServiceBase):
    service: Service = Field(exclude=True)
    lang: Lang = Field(default=Lang.UK, exclude=True)
    girl_id: int = Field(exclude=True)
    service_id: int = Field(exclude=True)

    @computed_field
    def name_localized(self) -> str:
        self.service.lang = self.lang
        return self.service.name_localized

    class Config:
        from_attributes = True


class GirlServiceCreate(GirlServiceBase):
    pass


class Girl(GirlBase):
    id: int
    birth_date: date = Field(exclude=True)
    photos: List[Photo] = []
    prices: List[Price] = []
    services: List[GirlService] = []
    lang: Lang = Field(default=Lang.UK, exclude=True)

    hair_color: HairColor = Field(exclude=True)
    ethnicity: Ethnicity = Field(exclude=True)
    body_type: BodyType = Field(exclude=True)
    breast_type: BreastType = Field(exclude=True)

    @computed_field
    def hair_color_localized(self) -> str:
        return self.hair_color.get_translation(self.lang)

    @computed_field
    def ethnicity_localized(self) -> str:
        return self.ethnicity.get_translation(self.lang)

    @computed_field
    def body_type_localized(self) -> str:
        return self.body_type.get_translation(self.lang)

    @computed_field
    def breast_type_localized(self) -> str:
        return self.breast_type.get_translation(self.lang)

    @computed_field
    def age(self) -> int:
        return calculate_age(self.birth_date)

    description_ua: Optional[str] = Field(exclude=True)
    description_ru: Optional[str] = Field(exclude=True)
    description_en: Optional[str] = Field(exclude=True)

    @computed_field
    def description_localized(self) -> str | None:
        if self.lang == Lang.UK:
            return self.description_ua or None
        elif self.lang == Lang.RU:
            return self.description_ru or None
        elif self.lang == Lang.EN:
            return self.description_en or None
        return None

    class Config:
        from_attributes = True


class GirlShort(BaseModel):
    id: int
    name: str
    birth_date: date = Field(exclude=True)
    height: int
    weight: int
    is_verified: bool
    photos: Optional[List[Photo]] = Field(default_factory=list, exclude=True)
    prices: Optional[List[Price]] = Field(default_factory=list, exclude=True)

    @computed_field
    def age(self) -> int:
        return calculate_age(self.birth_date)

    @computed_field
    def main_photo(self) -> Optional[str]:
        if self.photos:
            return self.photos[0].file_path
        return None

    @computed_field
    def min_price(self) -> Optional[int]:
        if self.prices:
            return min(price.current_cost for price in self.prices)
        return None

    class Config:
        from_attributes = True

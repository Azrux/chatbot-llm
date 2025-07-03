""" Stock data model for car listings. """

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class StockData(BaseModel):
    """
    Stock data model for car listings.
    This model represents the data structure for a car stock item
    """
    stock_id: int = Field(..., alias="stock_id", description="Stock unique ID")
    km: int = Field(..., alias="km", description="Mileage in kilometers")
    price: float = Field(..., alias="price", description="Price in MXN")
    make: str = Field(..., alias="make", description="Car make")
    model: str = Field(..., alias="model", description="Car model")
    year: int = Field(..., alias="year", description="Year of manufacture")
    version: str = Field(..., alias="version", description="Car version")
    bluetooth: Optional[bool] = Field(
        None, alias="bluetooth", description="Bluetooth availability")
    length: Optional[float] = Field(
        None, alias="largo", description="Length in centimeters")
    width: Optional[float] = Field(
        None, alias="ancho", description="Width in centimeters")
    height: Optional[float] = Field(
        None, alias="altura", description="Height in centimeters")
    car_play: Optional[bool] = Field(
        None, alias="car_play", description="CarPlay availability")

    @field_validator('bluetooth', 'car_play')
    @classmethod
    def str_to_bool(cls, v):
        """ Convert string values to boolean for 'bluetooth' and 'car_play' fields."""
        if isinstance(v, str):
            return v.strip().lower() == "sí"
        return bool(v) if v is not None else None

    class Config:
        # pylint: disable=too-few-public-methods
        """ Pydantic configuration for the model. """
        populate_by_name = True

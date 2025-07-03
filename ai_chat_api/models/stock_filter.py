"""Stock data filter model for car listings."""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class StockDataFilter(BaseModel):
    """
    Stock data filter model for car listings.
    This model represents the data structure for filtering car stock items.
    """
    stock_id: Optional[int] = Field(
        None, alias="stock_id", description="Stock unique ID")
    km: Optional[int] = Field(
        None, alias="km", description="Mileage in kilometers")
    price: Optional[float] = Field(
        None, alias="price", description="Price in MXN")
    make: Optional[str] = Field(None, alias="make", description="Car make")
    model: Optional[str] = Field(None, alias="model", description="Car model")
    year: Optional[int] = Field(
        None, alias="year", description="Year of manufacture")
    version: Optional[str] = Field(
        None, alias="version", description="Car version")
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
        """Convert string values to boolean for 'bluetooth' and 'car_play' fields."""
        if isinstance(v, str):
            return v.strip().lower() == "sí"
        return bool(v) if v is not None else None

    class Config:
        """Pydantic configuration for the model."""
        populate_by_name = True
        # pylint: disable=too-few-public-methods
        allow_population_by_field_name = True

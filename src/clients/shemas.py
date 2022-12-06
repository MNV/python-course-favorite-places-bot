"""
Описание моделей данных (DTO).
"""
from typing import Optional

from pydantic import BaseModel, Field


class PlaceDTO(BaseModel):
    """
    Модель для представления данных о месте.
    """

    id: int = Field(title="Идентификатор")
    latitude: float = Field(title="Широта")
    longitude: float = Field(title="Долгота")
    description: str = Field(title="Описание", min_length=2, max_length=255)
    city: Optional[str] = Field(
        None, title="Название города", min_length=2, max_length=50
    )
    locality: Optional[str] = Field(
        None, title="Местонахождение", min_length=2, max_length=255
    )

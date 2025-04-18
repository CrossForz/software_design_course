import uuid

from pydantic import BaseModel
from typing import Optional

from utils.bas_utils.transaction import TransactionType


class CategoryBase(BaseModel):
    type: TransactionType
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    type: Optional[TransactionType]
    name: Optional[str]


class CategoryRead(CategoryBase):
    id: uuid.UUID


    class Config:
        from_attributes = True

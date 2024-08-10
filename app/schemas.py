from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # class Config:
    #     from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# class VoteOut(BaseModel):
#     recipe_id: int
#     user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = Field(coerce_numbers_to_str=True)


class RecipeBase(BaseModel):
    name: str
    servings: int
    frequency: int
    instructions: list[str]
    time: list[int]
    is_prep_required: bool = False


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    # class Config:
    #     from_attributes = True


class RecipeOut(BaseModel):
    Recipe: Recipe
    votes: int


class ShoppingListItemBase(BaseModel):
    name: str
    amount: int
    recipe: Optional[list[int]] = None


class ShoppingListItemCreate(ShoppingListItemBase):
    pass


class ShoppingListItemOut(ShoppingListItemBase):
    id: int
    created_at: datetime

    # class Config:
    #     from_attributes = True


class Vote(BaseModel):
    recipe_id: int
    dir: bool

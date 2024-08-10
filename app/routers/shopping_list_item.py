from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status

from .. import models, schemas
from ..database import engine, get_db

router = APIRouter(prefix="/shopping_list_items", tags=["Shopping List Items"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShoppingListItemOut,
)
def create_shopping_list_item(
    shopping_list_item: schemas.ShoppingListItemCreate, db: Session = Depends(get_db)
):
    new_shopping_list_item = models.ShoppingListItem(**shopping_list_item.model_dump())

    db.add(new_shopping_list_item)
    db.commit()
    db.refresh(new_shopping_list_item)

    return new_shopping_list_item

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=List[schemas.RecipeOut])
def get_recipes(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cur.execute("SELECT * FROM recipes")
    # recipes = cur.fetchall()
    # for only showing current user's recipes: .filter(models.Recipe.user_id == current_user.id)

    # #before adding vote join
    # recipes = (
    #     db.query(models.Recipe)
    # .filter(models.Recipe.name.contains(search))
    # .limit(limit)
    # .offset(skip)
    # .all()
    # )

    results = (
        db.query(models.Recipe, func.count(models.Vote.recipe_id).label("votes"))
        .join(models.Vote, models.Vote.recipe_id == models.Recipe.id, isouter=True)
        .group_by(models.Recipe.id)
        .filter(models.Recipe.name.contains(search))
        .limit(limit)
        .offset(skip)
    ).all()

    return results


@router.get("/{id}", response_model=schemas.RecipeOut)
def get_recipe(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cur.execute("SELECT * FROM recipes WHERE id = %s", [str(id)])
    # recipe = cur.fetchone()
    # recipe = db.query(models.Recipe).filter(models.Recipe.id == id).first()

    recipe = (
        db.query(models.Recipe, func.count(models.Vote.recipe_id).label("votes"))
        .join(models.Vote, models.Vote.recipe_id == models.Recipe.id, isouter=True)
        .group_by(models.Recipe.id)
        .filter(models.Recipe.id == id)
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    # # for only showing current user's recipes
    # if recipe.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"Not authorized to perform requested action",
    #     )
    return recipe


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Recipe)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cur.execute(
    #     "INSERT INTO recipes (name, servings, frequency, instructions, time, is_prep_required) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
    #     (
    #         recipe.name,
    #         recipe.servings,
    #         recipe.frequency,
    #         recipe.instructions,
    #         recipe.time,
    #         recipe.is_prep_required,
    #     ),
    # )
    # conn.commit()
    # new_recipe = cur.fetchone()

    # new_recipe = models.Recipe(
    #     name=recipe.name,
    #     servings=recipe.servings,
    #     frequency=recipe.frequency,
    #     instructions=recipe.instructions,
    #     time=recipe.time,
    #     is_prep_required=recipe.is_prep_required,
    # )
    new_recipe = models.Recipe(user_id=current_user.id, **recipe.model_dump())

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cur.execute("DELETE FROM recipes WHERE id = %s RETURNING *", [str(id)])
    # deleted_recipe = cur.fetchone()
    # conn.commit()

    deleted_recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id)
    deleted_recipe = deleted_recipe_query.first()

    if deleted_recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if deleted_recipe.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    deleted_recipe_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Recipe)
def update_recipe(
    id: int,
    updated_recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cur.execute(
    #     "UPDATE recipes SET name = %s, servings = %s, frequency = %s, instructions = %s, time = %s, is_prep_required = %s WHERE id = %s RETURNING *",
    #     (
    #         recipe.name,
    #         recipe.servings,
    #         recipe.frequency,
    #         recipe.instructions,
    #         recipe.time,
    #         recipe.is_prep_required,
    #         str(id),
    #     ),
    # )
    # conn.commit()
    # updated_recipe = cur.fetchone()

    recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id)
    recipe = recipe_query.first()

    if recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if recipe.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    recipe_query.update(updated_recipe.model_dump(), synchronize_session=False)
    db.commit()

    return recipe_query.first()

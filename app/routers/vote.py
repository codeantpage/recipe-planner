from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    recipe = db.query(models.Recipe).filter(models.Recipe.id == vote.recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote.id} does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == True:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.recipe_id}",
            )
        new_vote = models.Vote(recipe_id=vote.recipe_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

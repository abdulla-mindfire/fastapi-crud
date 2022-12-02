from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import Vote
from ..oauth2 import get_current_user
from .. import models

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post does not exists!')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User has already voted on post')
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted"}

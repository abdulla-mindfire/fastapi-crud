from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models
from ..schemas import Post, PostResponse, UserCreate, UserOut, PostOut
from ..database import get_db
from .. import oauth2

router = APIRouter(prefix='/posts', tags=['Post'])


@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorised to delete")
    post.delete(synchronize_session=False)
    db.commit()
    return {"details": "Deleted Successfully"}


@router.put("/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorised to delete")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": "success"}

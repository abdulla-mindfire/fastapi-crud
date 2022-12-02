from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, utils
from ..schemas import Post, PostResponse, UserCreate, UserOut
from ..database import get_db

router = APIRouter(prefix='/user', tags=['User'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user.email)
    if user_exists.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists!")
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist!")
    return user
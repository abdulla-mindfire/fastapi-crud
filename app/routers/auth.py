from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserLogin, Token
from ..models import User
from ..utils import verify
from .. import oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=Token)
def login(user_creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_creds.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='Invalid Credentials')

    if not verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='Invalid Credentials')
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
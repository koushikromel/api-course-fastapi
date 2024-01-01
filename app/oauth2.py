from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, database, models

SECRET_KEY = "f91ddda468f26afafee7af8851d735ad137ec41447a0b56824ede759e570a24f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        # print(f"{id=} and {type(id)=}")
        token_data = schemas.TokenData(id=id)
        # print(f"{token_data=}")

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

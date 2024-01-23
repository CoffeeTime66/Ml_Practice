from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

import bcrypt

from models.users import Bill, User
from utils.database import session_commit, get_session


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def get_user_by_username(username, session=get_session()):
    return session.query(User).filter_by(username=username).first()


def get_user_by_email(email, session=get_session()):
    return session.query(User).filter_by(email=email).first()


def get_bill_by_user_id(user_id, session=get_session()):
    return session.query(Bill).filter_by(User_id=user_id).first()


def authenticate_user(username: str, password: str, session=get_session()):
    user = session.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    if token is None:
        token = Depends(oauth2_scheme)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return username


def create_user(
    email,
    username,
    password,
    name,
    surname,
    session=get_session(),
):
    new_user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
        name=name,
        surname=surname,
    )

    session.add(new_user)
    session_commit(session)
    new_bill = create_bill(user_id=new_user.id, money=200)
    session.add(new_bill)
    session_commit(session)
    return new_user


def create_bill(
    user_id,
    money,
):
    new_bill = Bill(
        User_id=user_id,
        money=money,
    )

    return new_bill


def update_bill(bill_id, new_money_value, session=get_session()):
    try:
        bill = session.query(Bill).get(bill_id)
        if bill:
            bill.money = new_money_value
            session_commit(session)
            return 1
    except:
        return 0


def delete_user(
    user_id,
    session=get_session(),
):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session_commit(session)

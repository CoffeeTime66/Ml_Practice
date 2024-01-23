from datetime import timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request, status

from schemas.users import User
from utils.users import create_user, get_user_by_email, authenticate_user, create_access_token, \
    get_current_user, get_user_by_username, get_bill_by_user_id

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/sign-up")
def register_user(pd: User):
    db_user = get_user_by_email(pd.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(
        email=pd.email,
        username=pd.username,
        password=pd.password,
        name=pd.name,
        surname=pd.surname,
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "name": user.name,
        "surname": user.surname,
    }


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"username": user.username, "password": user.hashed_password}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/billing")
def get_user_bill(request: Request):
    headers = request.headers
    current_user = get_current_user(headers["Authorization"])
    user = get_user_by_username(current_user)
    if user:
        bill = get_bill_by_user_id(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "bill": bill.money if bill.money > 0 else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

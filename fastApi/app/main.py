from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers import users
from routers import predictions


app = FastAPI()
app.include_router(users.router)
app.include_router(predictions.router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


from fastapi import FastAPI
from piza_api.auth_routes import auth_router
from piza_api.order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from piza_api.schemas import Settings

app=FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)




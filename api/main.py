from fastapi import FastAPI
from api.utils.db_utils import database
from api.auth import router as auth_router
from api.user import controller as user_router
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
@app.get("/")
def hello():
    return("Hello ALAM")

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router.router, tags=["Users"])
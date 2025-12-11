from app.db.database import engine
from app.api.routes import auth_route, user_route , llm_route
from contextlib import asynccontextmanager
from app.db.database import Base
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(llm_route.router, prefix="/chat_with_llm" , tags=["chat_with_llm"])

@app.get("/")
def root():
    return {"message": "FastAPI Auth API running!"}

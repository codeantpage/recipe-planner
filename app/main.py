from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from . import models
from .config import settings
from .database import engine
from .routers import auth, recipe, shopping_list_item, user, vote

# no longer needed. alembic handles all table creation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# change later
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe.router)
app.include_router(shopping_list_item.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

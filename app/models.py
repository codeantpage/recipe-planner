from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    servings = Column(SmallInteger)
    frequency = Column(SmallInteger)
    instructions = Column(ARRAY(String))
    time = Column(ARRAY(SmallInteger))
    is_prep_required = Column(Boolean, nullable=False, server_default="FALSE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("User")
    # vote = relationship("Vote")


class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False, server_default="1")
    recipe = Column(ARRAY(Integer))  # needs to be FK of recipes
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )


class Vote(Base):
    __tablename__ = "votes"
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

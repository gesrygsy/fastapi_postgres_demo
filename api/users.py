from os import stat
from typing import Optional, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from pydantic_schemas.user import UserCreate, User
from api.utils.users import get_user, get_user_by_email, get_users, create_user
from api.utils.courses import get_user_courses

router = fastapi.APIRouter()


@router.get("/users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users", status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(db=db, user=user)


@router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{user_id}/courses")
async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_courses(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="UserCourses not found")
    return db_user
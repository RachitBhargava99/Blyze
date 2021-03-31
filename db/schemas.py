from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional


# ===================================
# Group Models start here
# ===================================
class GroupBase(BaseModel):
    name: str
    default_duration: int


class GroupID(BaseModel):
    id: int


class Group(GroupBase, GroupID):
    is_active: bool
    owner_id: int

    class Config:
        orm_mode = True


class GroupList(BaseModel):
    groups: List[Group]


# ===================================
# User Models start here
# ===================================
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserAuthenticated(UserBase):
    auth_token: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: List[User]


# ===================================
# Chat Models start here
# ===================================
class Chat(BaseModel):
    id: int
    user_list: int
    messages: List[str] #Messages should probably be a different model, but I'm tired rn -\_(")_/-

class ChatList(BaseModel):
    chats: List[Chat]





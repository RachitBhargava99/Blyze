from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional


# ===================================
# Organization Models start here
# ===================================
class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationID(BaseModel):
    id: int


class Organization(OrganizationBase, OrganizationID):
    owner_id: int

    class Config:
        orm_mode = True


class OrganizationList(BaseModel):
    orgs: List[Organization]


# ===================================
# Project Models start here
# ===================================
class ProjectBase(BaseModel):
    name: str
    base_location: str


class ProjectCreate(ProjectBase):
    pass


class ProjectEdit(ProjectBase):
    pass


class ProjectID(BaseModel):
    id: int


class Project(ProjectBase, ProjectID):
    class Config:
        orm_mode = True


class ProjectList(BaseModel):
    projects: List[Project]


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
    messages: List[str]  # Messages should probably be a different model, but I'm tired rn -\_(")_/-


class ChatList(BaseModel):
    chats: List[Chat]

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
import bcrypt

from .db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)

    def __init__(self, username: str, password: str, org_id: int = None):
        self.username = username
        self.password = self.get_hash(password)
        self.organization_id = org_id

    @staticmethod
    def get_hash(text) -> str:
        return str(bcrypt.hashpw(bytes(text, encoding='utf8'), b'$2b$12$.Ez2TpYFdXhuIRWIavuklO'))


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))

    def __init__(self, name, creator_id):
        self.name = name
        self.owner_id = creator_id


class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(Integer, primary_key=True)
    chat_type = Column(Integer)


# Change Note: Changed project_id to id - project_id seems redundant in a class named 'Project', id should be sufficient
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), unique=True)
    name = Column(String(127), unique=True, nullable=False)
    base_location = Column(String(255), unique=True, nullable=False)

    def __init__(self, name, location):
        self.name = name
        self.base_location = location
        self.chat_id = None


class Chat_Individual_Pairs(Base):
    __tablename__ = 'chatpairs'

    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))


# Convention Note: Change naming from camel case
# General Note: Redundant class - check organizations
class Org_Membership(Base):
    __tablename__ = 'orgmemberships'

    user_id = Column(Integer, ForeignKey('users.id'))
    org_id = Column(Integer, ForeignKey('organizations.org_id'))


# Change Note: Changed user_id linking to organization_id linking
class Project_Membership(Base):
    __tablename__ = 'projectmemberships'

    org_id = Column(Integer, ForeignKey('organizations.id'))
    project_id = Column(Integer, ForeignKey('projects.project_id'))

    def __init__(self, org_id: int, project_id: int):
        self.org_id = org_id
        self.project_id = project_id


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    message = Column(String(255))
    time = Column(Integer,
                  nullable=True)  # Not sure how to to dates yet, so I'll fix this after initial mvp - Use DateTime

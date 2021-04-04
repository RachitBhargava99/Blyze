from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
import bcrypt

from .db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)

    def __init__(self, username: str, password: str, org_id: str = None):
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

    def __init__(self, name, creator_id):
        self.name = name
        self.owner_id = creator_id


class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(Integer, primary_key=True)
    chat_type = Column(Integer)


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))

class Organization(Base):
    __tablename__ = 'organizations'

    org_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))

class Chat_Individual_Pairs(Base):
    __tablename__ = 'chatpairs'

    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))

class Org_Membership(Base):
    __tablename__ = 'orgmemberships'

    user_id = Column(Integer, ForeignKey('users.id'))
    org_id = Column(Integer, ForeignKey('organizations.org_id'))

class Project_Membership(Base):
    __tablename__ = 'projectmemberships'

    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.project_id'))


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    message = Column(String(255))
    time = Column(Integer, nullable=True) #Not sure how to to dates yet, so I'll fix this after initial mvp






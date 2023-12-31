from datetime import date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    age = Column(Integer)
    vaccinated = Column(Boolean, default=False)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)

    owner = relationship("Owner", backref='cats')


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String, index=True)
    date_of_birth = Column(Date)
    description = Column(String, index=True, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)


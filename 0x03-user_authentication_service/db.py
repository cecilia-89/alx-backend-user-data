#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a user object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns user based on the argument"""
        user = self._session.query(User).filter_by(**kwargs).one_or_none()
        if user is None:
            raise NoResultFound
        for k in kwargs.keys():
            if hasattr(user, k):
                return user
        raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user based on keyword arguments"""
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if hasattr(user, k):
                user.k = v
                return
        raise ValueError

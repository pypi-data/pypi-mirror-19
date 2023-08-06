# -*- coding: utf-8 -*-

"""
Created on 2017-01-03
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from datetime import datetime
from kotti import Base, DBSession
from kotti.interfaces import IDefaultWorkflow
from sqlalchemy import (
    Column, ForeignKey, Integer, Unicode,
    Float, Boolean, Date, DateTime, String
)
from zope.interface import implements

from kotti_history import _


class SearchHistory(Base):

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(ForeignKey('principals.name',
                                onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    term = Column(String, nullable=False)
    date_last_viewed = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    @classmethod
    def create(cls, username, term):
        sh = cls(username=username, term=term)
        DBSession.add(sh)

    @classmethod
    def find_by_username(cls, username, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.username == username
        )

    @classmethod
    def find_by_term(cls, term, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.term == term
        )


class ViewHistory(Base):
    """ A custom content type. """

    implements(IDefaultWorkflow)

    id = Column(ForeignKey('contents.id',
                           onupdate="CASCADE",
                           ondelete="CASCADE"),
                primary_key=True)
    username = Column(ForeignKey('principals.name',
                                onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    content_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    num_views = Column(Integer, default=1)
    date_last_viewed = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    @classmethod
    def create(cls, content, user):
        history = cls(
            username=user.name,
            content_type=cls.__class__.__name__,
            id=content.id,
            title=content.title,
            url=content.path,
            num_views=1
        )
        return history

    @classmethod
    def find_by_content_id(cls, id, query=None):
        if not query:
            query = cls.query
        return query.filter(
                cls.id == id
            )

    @classmethod
    def find_by_username(cls, username, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.username == username
        )

    @classmethod
    def find(cls, content_id=None, username=None):
        query = cls.query
        if content_id:
            query = cls.find_by_content_id(content_id)
        if username:
            query = cls.find_by_username(username)
        return query


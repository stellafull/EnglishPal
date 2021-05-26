# Software Architecture and Design Patterns -- Lab 2 starter code
# Copyright (C) 2021 Hui Lan

from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# ADDITION: just for convenience
engine = create_engine(
    r'sqlite:///D:\newDesktop\大三下courses\SADP\lab2\test\EnglishPalDatabase.db')
get_session = sessionmaker(bind=engine)
session = get_session()

@dataclass
class Article:
    article_id: int
    text: str
    source: str
    date: str
    level: int
    question: str


class NewWord:
    def __init__(self, username, word='', date='yyyy-mm-dd'):
        self.username = username
        self.word = word
        self.date = date


class User:
    def __init__(self, username, password='12345', start_date='2021-05-19', expiry_date='2031-05-19'):
        self.username = username
        self.password = password
        self.start_date = start_date
        self.expiry_date = expiry_date
        self._read = []

    def read_article(self, article):
        # ADDITION: implement the action
        session.add(article)
        reading = Reading(self.username, article.article_id)
        session.add(reading)
        session.commit()
        # pass

    # ADDITION: use property to achieve list(user.newwords)
    @property
    def newwords(self):
        words = session.query(NewWord).filter(NewWord.username == self.username).all()
        # test code
        # for w in words:
        #     print(w.word)
        return words


# ADDITION: implement the Reading class
class Reading:
    def __init__(self, username, article_id):
        self.username = username
        self.article_id = article_id

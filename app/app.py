# Software Architecture and Design Patterns -- Lab 2 starter code
# Copyright (C) 2021 Hui Lan

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
import orm

orm.start_mappers()
engine = create_engine(
    r'sqlite:///D:\newDesktop\大三下courses\SADP\lab2\test\EnglishPalDatabase.db') # modify the path
orm.metadata.drop_all(engine)
orm.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)

# add two users

session = get_session()

try:
    session.add(model.User(username='mrlan', password='12345', start_date='2021-05-14'))
    session.add(model.User(username='lanhui', password='Hard2Guess!', start_date='2021-05-15'))
    session.commit()
except:
    print('Duplicate insertions.')

print(session.query(model.User).count())

for u in session.query(model.User).all():
    print(u.username)

session.close()

# add a few new words

session = get_session()
session.add(model.NewWord(username='lanhui', word='starbucks', date='2021-05-15'))
session.add(model.NewWord(username='lanhui', word='luckin', date='2021-05-15'))
session.add(model.NewWord(username='lanhui', word='secondcup', date='2021-05-15'))
session.add(model.NewWord(username='mrlan', word='costa', date='2021-05-15'))
session.add(model.NewWord(username='mrlan', word='timhortons', date='2021-05-15'))
session.commit()
session.close()

# add a few articles

session = get_session()
article = model.Article(article_id=1,
                        text='THE ORIGIN OF SPECIES BY MEANS OF NATURAL SELECTION, OR THE PRESERVATION OF FAVOURED RACES IN THE STRUGGLE FOR LIFE',
                        source='CHARLES DARWIN, M.A.', date='1859-01-01', level=5,
                        question='Are humans descended from monkeys?')
session.add(article)
session.commit()
session.close()

# query user and let him read something

session = get_session()
user = session.query(model.User).filter_by(username='lanhui').one()

for item in list(user.newwords):
    print(item.word)

user.read_article(article)  # this method call will add a row to table readings

print('-----')

user = session.query(model.User).filter_by(username='mrlan').one()
for item in list(user.newwords):
    print(item.word)

user.read_article(article)  # this method call will add a row to table readings

session.commit()
session.close()
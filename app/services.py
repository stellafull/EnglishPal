# Software Architecture and Design Patterns -- Lab 3 starter code
# An implementation of the Service Layer
# Copyright (C) 2021 Hui Lan

import repository
import model

# word and its difficulty level
WORD_DIFFICULTY_LEVEL = {'starbucks':5, 'luckin':4, 'secondcup':4, 'costa':3, 'timhortons':3, 'frappuccino':6}


class UnknownUser(Exception):
    pass


class NoArticleMatched(Exception):
    pass


def read(user, user_repo, article_repo, session):

    dbuser = user_repo.get(user.username)
    if dbuser is None or dbuser.password != user.password:
        raise UnknownUser(user)

    wordList = session.query(model.NewWord).filter(model.NewWord.username == user.username).all()
    difficulty_list = []
    for w in wordList:
        difficulty_list.append(WORD_DIFFICULTY_LEVEL.get(w.word))
    difficulty_list.sort(reverse=True)
    lu = 0
    count = 0
    for i in difficulty_list:
        if count>=3:
            break
        lu += i
        count+=1
    lu /= count

    qualified_articles = session.query(model.Article).filter(model.Article.level > lu).order_by(model.Article.level).all()
    if not qualified_articles:
        raise NoArticleMatched
    else:
        wanted_article = qualified_articles[0]
        ar = article_repo.get(wanted_article.article_id)
        session.add(ar)
        dbuser.read_article(ar)
        session.commit()
        # print(user._read)
        return wanted_article.article_id



# "Database code" for the DB news.

import psycopg2

DBNAME = "news"


def get_article_report():
    """What are the most popular three articles of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = "select title, count(*) as views \
             from log, articles \
             where path = '/article/' || articles.slug \
             group by title order by views desc limit 3;"
    c.execute(query)
    return c.fetchall()
    db.close()


def get_author_report():
    """Who are the most popular article authors of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = "select name, count(articles.title) as views \
             from log, articles, authors \
             where path = '/article/' || articles.slug \
             and authors.id = articles.author\
             group by name order by views desc;"
    c.execute(query)
    return c.fetchall()
    db.close()


def get_error_report():
    """On which days did more than 1% of site requests lead to errors?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = "with error_log as \
             ( \
              select time::date, \
              round(100 * ( \
              sum(case when status != '200 OK' \
              then 1 else 0 end)::numeric / count(time)::numeric), 2) \
              as percent_error \
              from log \
              group by time::date \
             ) \
             select to_char(time, 'Month DD, YYYY') as date, percent_error \
             from error_log \
             where percent_error > 1.0;"
    c.execute(query)
    return c.fetchall()
    db.close()

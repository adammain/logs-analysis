# Logs Analysis Project


## How to install
```
# Clone this git repo:
git clone git@github.com:amtruenorth/logs-analysis.git

cd logs-analysis/
```

### Requirements
- Tested with Python3
- Environtment cabable of running PostgreSQL server
- `"news"` database generated by the `newsdata.sql` file

## Usage

1) Open a terminal / shell / command line / command prompt window
2) Navigate to project directory ```logs-analysis/```
3) To run the log-analysis program, enter the command:
```
python3 news.py
```

### Expected Results

The following output should be displayed in your terminal shell window:

1. What are the most popular three articles of all time?

    "Candidate is jerk, alleges rival" — 338647 views
    
    "Bears love berries, alleges bear" — 253801 views
    
    "Bad things gone, say good people" — 170098 views


2. Who are the most popular article authors of all time?

    Ursula La Multa — 507594 views
    
    Rudolf von Treppenwitz — 423457 views
    
    Anonymous Contributor — 170098 views
    
    Markoff Chaney — 84557 views


3. On which days did more than 1% of requests lead to errors?

    July      17, 2016 — 2.26% errors

---

### Design Notes

Project is split into two files, `news.py` and `newsdb.py`.

- `news.py` is responsible the programs initiation, calling the functions that contain the SQL queries, and organizing the SQL query's return output into plain text format.
- `newsdb.py` contains our database connection and the functions to execute each SQL query:

  -- `get_article_report()` - Queries the DB to answer the question: **_What are the most popular three articles of all time?_**
    - _Matches each articles slug with the log's url records to determine how many time each article was viewed.  Returns the the top 3 viewed article titles and their viewcount._
  ```
  select title, count(*) as views
  from log, articles
  where path = '/article/' || articles.slug
  group by title order by views desc limit 3;
  ```
  ---
  -- `get_author_report()` - Queries the DB to answer the question: **_Who are the most popular article authors of all time?_**
    - _Joins 3 tables, counts each article's views that was written by each author, and displays each author's total number of views for all articles they have written._
  ```
  select name, count(articles.title) as views
  from log, articles, authors
  where path = '/article/' || articles.slug
  and authors.id = articles.author
  group by name order by views desc;
  ```
  ---
  -- `get_error_report()` - Queries the DB to answer the question: **_On which days did more than 1% of site requests lead to errors?_**
    - _Uses a subquery named `error_log` to find each days percent error (named `percent_error`) from the log table. Another query then tests each day's error percentage, returning only those with an error rate over 1%._
  ```
  with error_log as 
  ( 
    select time::date, 
    round(100 * ( sum( case when status != '200 OK' 
          then 1 else 0 end)::numeric / count(time)::numeric), 2) 
    as percent_error 
    from log 
    group by time::date 
  ) 
  select to_char(time, 'Month DD, YYYY') as date, percent_error 
  from error_log 
  where percent_error > 1.0;
  ```

---
### License
MIT © Adam Main

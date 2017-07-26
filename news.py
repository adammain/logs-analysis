#!/usr/bin/env python3
#
# An internal log reporting service for a news website..


from newsdb import get_article_report, get_author_report, get_error_report


# Template for the log reports plain text output
TEXT_WRAP = '''\
1. What are the most popular three articles of all time?

%s

2. Who are the most popular article authors of all time?

%s

3. On which days did more than 1%% of requests lead to errors?

%s
'''

# Template for individual report
REPORT = '''\
    %s — %s%s
'''


def main():
    article_report = "".join(REPORT % ('"'+article+'"', result, ' views')
                             for article, result in get_article_report())
    author_report = "".join(REPORT % (author, result, ' views')
                            for author, result in get_author_report())
    error_report = "".join(REPORT % (date, result, '% errors')
                           for date, result in get_error_report())
    reports = TEXT_WRAP % (article_report, author_report, error_report)
    print(reports)
    return reports


main()

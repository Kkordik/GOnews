from apscheduler.schedulers.background import BackgroundScheduler
from config import config_data

# from database.run_db import urls_tb
# from database.Tables.UrlsTable import UrlsDb
# import newspaper

from newspaper import Article
from gnews import GNews
from pprint import pprint
from datetime import datetime


# Define a function to parse the publish date
def parse_date(date_str):
    # Define the date format
    date_format = '%a, %d %b %Y %H:%M:%S GMT'
    # Convert the date string to a datetime object
    return datetime.strptime(date_str, date_format)


def parse_gnews():
    google_news = GNews(language='ru', country='RU')
    topic_news = google_news.get_news_by_topic('TECHNOLOGY')

    # Now sort the list by the 'published date'
    sorted_topic_news = sorted(topic_news, key=lambda d: parse_date(d['published date']), reverse=True)
    # pprint(sorted_topic_news)
    for news in sorted_topic_news:
        print(f"{news['published date']} {news['title']} {news['url']}")
        # article = Article(news['url'])
        # article.download()
        # article.parse()


def job():
    print("I'm working...")

# def parse_urls():
#     urls_db = UrlsDb(table=urls_tb)
#     urls_db.add_url("https://abcnews.go.com")
#     all_news_sources = urls_db.get_all_urls()
#     print(all_news_sources)
#     for news_source in all_news_sources:
#         news_paper = newspaper.build(news_source['url'])
#         print(f"{news_source['url']}:{len(news_paper.articles)}")
#         for article in news_paper.articles[:10]:
#             article: newspaper.Article
#             article.download()
#             article.parse()
#             print(f"{article.tags}, {article.publish_date}, {article.title}, {article.url}")
#         for category in news_paper.categories:
#             print(category.url)


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=config_data['additional']['NEWS_INTERVAL_S'])
scheduler.start()





from bs4 import BeautifulSoup
from lxml import etree
import requests
from dataclasses import dataclass


@dataclass
class Article:
    href: str
    title: str


def get_articles():
    newsletter_url = "https://newsletterhunt.com/newsletters/money-stuff-by-matt-levine"

    r = requests.get(newsletter_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    raw_article = soup.find_all("article")

    articles = []
    for raw_article in raw_article:
        link = raw_article.find_all(lambda t: t.name == "a" and t.h2)[0]
        href = link['href']
        title = link.h2.string.strip().replace("Money Stuff: ", "")
        article = Article(href, title)
        articles.append(article)

    return articles


def get_article_html(url) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    html = soup.iframe['srcdoc']
    return html


if __name__ == '__main__':
    articles = get_articles()

    for article in articles:
        html = get_article_html(article.href)
        file_path = f"{article.title}.html"

        with open(file_path, 'w') as f:
            f.write(html)

import feedparser


def get_articles():
    url = "https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine.rss"
    feed = feedparser.parse(url)
    return feed.entries

if __name__ == "__main__":
    print(get_articles())
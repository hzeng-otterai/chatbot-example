from duckduckgo_search import DDGS
from itertools import islice

def search_news(keywords, num_results=10):
    result = []
    with DDGS() as ddgs:
        ddgs_news_gen = ddgs.news(
          keywords,
          region="us-en",
          safesearch="Off",
          timelimit="m",
        )
        for r in islice(ddgs_news_gen, num_results):
            result.append(r)

    return result


def search_text(keywords, num_results=10):
    result = []
    with DDGS() as ddgs:
        ddgs_text_gen = ddgs.text(
            keywords, 
            region='cn-zh', 
            safesearch='Off', 
            timelimit='y'
        )

        for r in islice(ddgs_text_gen, num_results):
            result.append(r)

    return result
# Udacity - UD1110

# Author : Tejasvi Nuthalapati

"""
Pseudo Code:
page = a random starting page
article_chain = []
while title of page isn't 'Philosophy' and we have not discovered a cycle:
    append page to article_chain
    download the page content
    find the first link in the content
    page = that link
    pause for a second

"""

""" 
decides if it's a go for the crawler to go crawl further
@Params:
    search_history : search history the crawler tracked
    target_url : What's the target URL we are aiming to land at
@Return:
    True/False
@Implementation:
> if the most recent article in the search_history is the target article the search should stop and the function should return False
> If the list is more than 25 urls long, the function should return False
> If the list has a cycle in it, the function should return False
> otherwise the search should continue and the function should return True.
"""

from bs4 import BeautifulSoup
import requests
import time
import urllib


def find_first_link(url):
    # download html of the article
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    """
    If you only want Beautiful Soup to consider direct children, you can pass in recursive=False.
    As of today April,18 body is nested in the below tags
    """

    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # if nothing is found just return None
    article_link = None
    # find all direct p tags of content_div without recursion inward
    for element in content_div.find_all("p", recursive=False):
        # if the does direct p has a direct a tag in it ?
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    """
    This is very interesting point that I learnt:
        Wikipedia Urls sometimes are marked relatively in their hrefs so we need to return an absolute url for this to function appropriately
        To reconstruct the URL we do the below
    """

    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    return first_link

def continue_crawl(search_history, target_url, max_steps=25):

    # check is target is initial
    if search_history[-1] == target_url:
        print("Target URL found")
        return False
    elif len(search_history) > max_steps:
        print("Web Crawler Aborting... took suspiciously longer")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("Target URL reached !")
        return False
    return True

# HTML page we would like to Crawl, here it's a Wikipedia link
initial_url = "https://en.wikipedia.org/wiki/Japanese_battleship_Aki"


# Tracking the visited pages
article_chain = [initial_url]

# HTML page we are aiming to reach
target_url = "https://en.wikipedia.org/wiki/Philosophy"


while continue_crawl(article_chain, target_url):

    print("Visiting URl - " + article_chain[-1])

    # find the first link in that html
    first_link = find_first_link(article_chain[-1])

    if not first_link:
        print("Target URL Reached, abort crawler !")
        break

    # add the first link to article chain to continue crawling
    article_chain.append(first_link)
    # delay for about two seconds, see Wiki Bot Rules:
    time.sleep(2)

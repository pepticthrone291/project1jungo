import requests
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

bsc = "https://reddit.com"
sorting_posts = {}


def extract_post(i):
    top = f"{bsc}/r/{subreddits[i]}/top/?t=month"
    res = requests.get(top, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    postbox = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
    posts = postbox.find_all("div", {"data-testid": "post-container"})

    arts = []

    for post in posts:
        try:
            title = post.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).text
            print(title)
            linkbox = post.find(
                "a", {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
            link = bsc + linkbox['href']
            print(link)
            upvotes_box = post.find(
                "div", {"class": "_1E9mcoVn4MYnuBQSVDt1gC"})
            upvotes_str = upvotes_box.find(
                "div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"}).text
            if 'k' in upvotes_str:
                upvotes = int(float(upvotes_str.replace('k', ''))*1000)
            else:
                upvotes = int(upvotes_str)
            art = {'title': title, 'link': link,
                   'upvotes_str': upvotes_str, 'category': subreddits[i]}
            arts.append(art)
            global sorting_posts
            sorting_posts[upvotes] = art
        except:
            continue
    return arts


extract_post(0)

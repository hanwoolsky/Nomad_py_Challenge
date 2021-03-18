import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def extract(html, subreddit):
  votes = html.find("div", {"class":"_1rZYMD_4xY3gRcSS3p8ODO"})
  if votes:
    votes = votes.text
  title = html.find("h3", {"class":"_eYtD2XCVieq6emjKBH3m"})
  if title:
    title = title.text
  link = html.find("a", {"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
  if link:
    link = link['href']

  if votes and title and link:
    return {
      'votes':int(votes),
      'titles':title,
      'link':link,
      'subreddit':subreddit
    }

def content(subreddit):
  posts = []
  try:
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    container = soup.find("div", {"class":"rpBJOHq2PR60pnwJlUyP0"})
    if container:
      post = container.find_all("div", {"class": None})
      for i in range(len(post)):
        final = extract(post[2*i], subreddit)
        if final:
          posts.append(final)
  except:
    pass

  return posts


def summation(subreddits):
  sums = []
  for subreddit in subreddits:
    posts = content(subreddit)
    sums += posts
  return sums
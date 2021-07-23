import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def home():
  order = request.args.get("order_by")
  if not order:
    order = "popular"
  if order == "popular":
    result = requests.get(popular)
  elif order == "new":
    result = requests.get(new)
  data = result.json()["hits"]
  db[order] = data
  show = db[order]
  return render_template("index.html", order_by = order, results = show)

@app.route("/<id>")
def detail(id):
  detail_url = requests.get(make_detail_url(id))
  show = detail_url.json()
  return render_template("detail.html", results = show, detail = show["children"])

app.run(host="0.0.0.0")
"""
These are the URLs that will give you remote jobs for the term 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from stack_scrapper import get_jobs
from remote_scrapper import get_rejobs
from wework_scrapper import get_wejobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  term = request.args.get("term")
  if term:
    term = term.lower()
    existingJobs = db.get(term)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(term)
      jobs += get_rejobs(term)
      jobs += get_wejobs(term)
      db[term] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy=term,
    resultsNumber=len(jobs),
    jobs=jobs
  )


@app.route("/export")
def export():
  try:
    term = request.args.get('term')
    if not term:
      raise Exception()
    term = term.lower()
    jobs = db.get(term)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")
  

app.run(host="0.0.0.0")
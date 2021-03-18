import requests
from bs4 import BeautifulSoup

def extract_job(html):
    title = html.find("h2", {"itemprop": "title"}).text
    company = html.find("h2", {"itemprop": "hiringOrganization"}).text
    job_id = html.find("a", {"itemprop": "url"})["href"]
    return {
        'title': title,
        'company': company,
        "apply_link": f"https://remoteok.io/{job_id}"
    }


def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("table", {"id": "jobsboard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    return jobs


def get_rejobs(word):
    url = f"https://remoteok.io/remote-dev+{word}-jobs"
    jobs = extract_jobs(url)
    return jobs

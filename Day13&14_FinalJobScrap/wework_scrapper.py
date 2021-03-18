import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("li", {"class": "view-all"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("span", {"class": "title"}).text
    company = html.find("span", {"class": "company"}).text
    job_id = html.find("a")['href']
    return {
        'title': title,
        'company': company,
        "apply_link": f"https://weworkremotely.com/{job_id}"
    }

def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    return jobs


def get_wejobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("li", {"class": "view-all"}).find("a")
    url2 = pages["href"]
    jobs = extract_jobs(f"https://weworkremotely.com/{url2}")
    return jobs

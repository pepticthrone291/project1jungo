import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, send_file
from exporter import save_to_file

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

# so extraction


def so_ext(term):
    so_bsc = "https://stackoverflow.com"
    so = f"{so_bsc}/jobs?q={term}&r=true"
    jobs = []
    res = requests.get(so)
    soup = BeautifulSoup(res.text, "html.parser")
    page_box = soup.find("div", {"class": "s-pagination"})
    pages = page_box.find_all("a", {"class": "s-pagination--item"})
    max_page = int(pages[-2].text)
    for i in range(max_page):
        resa = requests.get(f"{so}&pg=f{i}")
        soupa = BeautifulSoup(resa.text, "html.parser")
        jobs_list_box = soupa.find("div", {"class": "listResults"})
        jobs_list = jobs_list_box.find_all("div", {"class": "flex--item fl1"})
        for job in jobs_list:
            linkntitle = job.find("h2", {"class": "mb4 fc-black-800 fs-body3"})
            linkp = linkntitle.find("a")["href"]
            link = f"{so_bsc}{linkp}"
            title = linkntitle.find("a").text.strip()
            company_loc = job.find(
                "h3", {"class": "fc-black-700 fs-body1 mb4"})
            company = company_loc.find("span").text.strip()
            job_info = {'title': title, 'company': company, 'link': link}
            jobs.append(job_info)
    return jobs

# wwr extraction


def wwr_ext(term):
    wwr_bsc = "https://weworkremotely.com"
    wwr = f"{wwr_bsc}/remote-jobs/search?term={term}"
    jobs = []
    resb = requests.get(wwr)
    soupb = BeautifulSoup(resb.text, "html.parser")
    jobs_list_box_b = soupb.find_all("article")
    for jobsb in jobs_list_box_b:
        jobs_list_b = jobsb.find_all("li", {"class": "feature"})
        for jobb in jobs_list_b:
            linkp = jobb.find("a")["href"]
            link = f"{wwr_bsc}{linkp}"
            company = jobb.find("span", {"class": "company"}).text
            title = jobb.find("span", {"class": "title"}).text
            job_info_b = {'title': title, 'company': company, 'link': link}
            jobs.append(job_info_b)
    return jobs

# ok extraction


def ok_ext(term):
    ok_bsc = "https://remoteok.io"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    ok = f"{ok_bsc}/remote-dev+{term}-jobs"
    jobs = []
    resc = requests.get(ok, headers=headers)
    soupc = BeautifulSoup(resc.text, "html.parser")
    jobs_list = soupc.find_all(
        "td", {"class": "company position company_and_position"})
    for job in jobs_list:
        try:
            company = job.find("h3", {"itemprop": "name"}).text
            titlenlink = job.find("a", {"itemprop": "url"})
            linkp = titlenlink["href"]
            link = f"{ok_bsc}{linkp}"
            title = titlenlink.find("h2", {"itemprop": "title"}).text
            job_info = {'title': title, 'company': company, 'link': link}
            jobs.append(job_info)
        except:
            continue
    return jobs


app = Flask("theLast")

db = {}


@app.route("/")
def home():
    return render_template("index13.html")


@app.route("/search")
def search():
    term = request.args.get("term")
    if term:
        term = term.lower()
        existingWords = db.get(term)
        if existingWords:
            jobs = existingWords
        else:
            jobs = wwr_ext(term) + ok_ext(term) + so_ext(term)
            db[term] = jobs
    else:
        return redirect("/")
    return render_template("search13.html", resultsNumber=len(jobs), searchingBy=term, jobs=jobs)


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
        save_to_file(jobs, term)
        return send_file(f"{term}.csv")
    except:
        return redirect("/")


app.run(host="0.0.0.0")

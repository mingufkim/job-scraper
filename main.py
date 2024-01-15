import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=python&tab=position")

for i in range(5):
    time.sleep(3)
    page.keyboard.down("End")

content = page.content()

browser.close()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__FqChn")

jobs_db = []

for job in jobs:
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company = job.find("span", class_="JobCard_companyName__vZMqJ").text
    location = job.find("span", class_="JobCard_location__2EOr5").text
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"

    job = {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }

    jobs_db.append(job)

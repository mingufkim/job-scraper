import csv
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class JobScraper:
    def __init__(self, query):
        self.query = query
        self.jobs_db = []

    def scrape_jobs(self):
        p = sync_playwright().start()

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(f"https://www.wanted.co.kr/search?query={self.query}&tab=position")

        for i in range(5):
            time.sleep(2.5)
            page.keyboard.down("End")

        content = page.content()

        browser.close()

        p.stop()

        soup = BeautifulSoup(content, "html.parser")

        jobs = soup.find_all("div", class_="JobCard_container__FqChn")

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

            self.jobs_db.append(job)

    def save_to_file(self):
        filename = self.query.replace(" ", "_").lower() + ".csv"
        file = open(filename, mode="w", encoding="utf-8-sig", newline="")
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Link"])

        for job in self.jobs_db:
            writer.writerow(job.values())

        file.close()


if __name__ == "__main__":
    queries = ["python", "java", "flutter"]

    for query in queries:
        job_scraper = JobScraper(query)
        job_scraper.scrape_jobs()
        job_scraper.save_to_file()

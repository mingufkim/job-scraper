from flask import Flask, render_template, request, redirect, send_file

from main import JobScraper
from file import save_to_file

app = Flask("Job Scraper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    if query == "":
        return redirect("/")
    if query in db:
        jobs = db[query]
    else:
        jobs = JobScraper(query).scrape_jobs()
        db[query] = jobs
    return render_template("search.html", query=query, jobs=jobs)


@app.route("/export")
def export():
    query = request.args.get("query")
    if query == "":
        return redirect("/")
    if query not in db:
        return redirect(f"/search?query={query}")
    save_to_file(query, db[query])
    return send_file(f"{query}.csv", as_attachment=True)


app.run(debug=True)

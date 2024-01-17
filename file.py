import csv


def save_to_file(query, jobs):
    filename = query.replace(" ", "_").lower() + ".csv"
    file = open(filename, mode="w", encoding="utf-8-sig", newline="")
    writer = csv.writer(file)
    writer.writerow(["포지션", "회사", "위치", "상세보기"])

    for job in jobs:
        writer.writerow(job.values())

    file.close()

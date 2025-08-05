import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Your search parameters ---
JOB_TITLE = "data analyst"
LOCATION = "Kenya"
KEYWORD = "python"
NUM_JOBS = 20

def scrape_jobs(title, location, keyword, num_jobs):
    jobs_found = 0
    page = 0
    all_descriptions = []

    while jobs_found < num_jobs:
        url = f"https://www.indeed.com/jobs?q={title}&l={location}&start={page * 10}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='job_seen_beacon')

        if not cards:
            break

        for card in cards:
            if jobs_found >= num_jobs:
                break
            description = card.text.lower()
            all_descriptions.append(description)
            jobs_found += 1
        page += 1

    keyword = keyword.lower()
    count = sum(desc.count(keyword) for desc in all_descriptions)
    report = f"[{datetime.now()}] Analyzed {jobs_found} jobs.\nKeyword '{keyword}' found {count} times.\n"

    # Save to text file
    with open("job_report.txt", "a") as file:
        file.write(report + "\n")

    print(report)

# --- Run the function ---
scrape_jobs(JOB_TITLE, LOCATION, KEYWORD, NUM_JOBS)

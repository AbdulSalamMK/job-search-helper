from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

app = Flask(__name__)

# Ensure static folder exists for storing CSV
if not os.path.exists('static'):
    os.makedirs('static')

# Function to get job data
def get_job_data(search_term, pages):
    jobs = []

    # Set up headless Chrome for cloud environments
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    for page in range(1, pages + 1):
        url = f"https://www.mycareersfuture.gov.sg/search?search={search_term}&sortBy=new_posting_date&page={page}"

        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "JobCard__card___22xP3")))
        except Exception as e:
            print(f"Error waiting for job cards: {e}")
            driver.quit()
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # Find all job cards
        cards = soup.find_all("a", attrs={"data-testid": "job-card-link"})

        # Extract job data
        for card in cards:
            title = card.find("span", {"data-testid": "job-card__job-title"})
            company = card.find("p", {"data-testid": "company-hire-info"})
            location = card.find("p", {"data-testid": "job-card__location"})
            link = card["href"]
            salary = card.find("span", {"data-testid": "salary-range"})
            salary = salary.text.strip() if salary else "Not Available"

            jobs.append({
                "title": title.text.strip() if title else None,
                "company": company.text.strip() if company else None,
                "location": location.text.strip() if location else None,
                "salary": salary,
                "link": "https://www.mycareersfuture.gov.sg" + link
            })

    return jobs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        pages = int(request.form['pages'])

        jobs = get_job_data(search_term, pages)

        # Save to CSV
        df = pd.DataFrame(jobs)
        file_path = 'static/job_listings.csv'
        df.to_csv(file_path, index=False)

        return render_template('index.html', jobs=jobs, file_path=file_path)

    return render_template('index.html')

@app.route('/download')
def download_file():
    file_path = 'static/job_listings.csv'
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

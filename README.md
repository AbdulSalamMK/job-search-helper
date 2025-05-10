
# Job Search Helper

A web application built using Flask and Selenium that scrapes job listings from MyCareersFuture.sg and allows users to download the results in CSV format.

## Features
- Search for job listings based on a keyword (e.g., "Python", "Marketing", etc.).
- Scrape multiple pages of job listings from MyCareersFuture.sg.
- View job details like title, company, location, salary, and a link to the job posting.
- Download the scraped job listings as a CSV file.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) based on your Chrome version and add it to your system's PATH.

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000/` to access the app.

## Usage

- Enter a search term (e.g., "Python", "Java") and the number of pages you want to scrape.
- Click "Search" to get the job listings.
- You can download the CSV file containing the job details after the search results are displayed.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Created by

AbdulSalamMK

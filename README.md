# REDDIT DAILY DIGEST

A clean, modular Python project that scrapes informative subreddits, produces CSV + HTML daily reports, and (optionally) commits those reports back to the repository using GitHub Actions.
Built to be reproducible, testable, and presentable, thus making it perfect for demos, portfolio projects, or lightweight research tooling.

Repository: [here](https://github.com/Ani-404/Reddit-Daily-Digest)

---

## Table of contents

- [Why this project](#why-this-project)
- [Features](#features)
- [Sample output](#sample-output)
- [Repo layout](#repo-layout)
- [Getting started (Windows)](#getting-started)
- [Run locally](#run-locally)
- [Github Actions (Automated runs)](#github-actions)
- [Design & Implementation notes](#design--implementation-notes)
- [Improvements & production ideas](#improvements--production-ideas)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgement](#acknowledgement)

---

## Why this project

This project collects posts from selected subreddits, extracts title, URL, score & content, and generates human-friendly HTML reports plus CSVs for downstream analysis. It demonstrates:

- robust scraping via Selenium + webdriver-manager,
- automated scheduling via GitHub Actions,
- clear project structure and reproducible dependencies,
- a minimal reporting layer for sharing insights.

It’s intentionally small but production-minded, good for showing real engineering practices.

---

## Features

- Scrapes multiple subreddit URLs configured in src/config.json
- Extracts: title, url, score, content, and source
- Outputs: daily data/YYYY-MM-DD.csv and data/YYYY-MM-DD.html
- Automated daily runs with GitHub Actions (.github/workflows/daily-digest.yml)
- Simple, dependency-free HTML report generator (safe HTML escaping)
- Pushes generated reports back to repo (via Actions)

---

## Sample output

![sample-output](https://github.com/Ani-404/Reddit-Daily-Digest/blob/main/images/Screenshot%202025-09-30%20204504.png)

---

## Repo layout

![repo-layout](https://github.com/Ani-404/Reddit-Daily-Digest/blob/main/images/Screenshot%202025-09-30%20204936.png)

---

## Getting started

1. Clone the repo
```Powershell
git clone https://github.com/Ani-404/Reddit-Daily-Digest.git
cd Reddit-Daily-Digest
```
2. Create & activate a virtual environment
```Powershell
python -m venv scraper-env
.\scraper-env\Scripts\activate
```
3. Install dependencies
```Powershell
pip install --upgrade pip
pip install -r requirements.txt
```
4. Ensure Google Chrome is installed (or change settings to use a different browser). webdriver-manager will download the appropriate ChromeDriver automatically.

---

## Configuration 

Example config used by main.py:
```json
{
  "output_dir": "data",
  "sites": [
    {
      "name": "MachineLearning",
      "url": "https://old.reddit.com/r/MachineLearning/",
      "posts_to_scrape": 10
    },
    {
      "name": "DataScience",
      "url": "https://old.reddit.com/r/datascience/",
      "posts_to_scrape": 10
    }
  ]
}
```
Notes
- Using old.reddit.com provides a stable, simpler DOM for scraping.
- output_dir should match the folder your main.py expects (default: data).

---

## Run locally

From repo root (with venv active):
```Powershell
python main.py
```

---

## Run with Docker (optional)

A simple Dockerfile makes the environment reproducible. Example:
```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## GitHub Actions

The repo contains .github/workflows/daily-digest.yml. It:
- runs daily at the configured cron (configured in the workflow file)
- sets up Python, installs requirements.txt
- runs python main.py
- commits data/ back to the repository using the built-in GITHUB_TOKEN.

Manual runs are available under Actions → Daily Digest → Run workflow.

---

## Design & implementation notes

- Selenium + webdriver-manager: webdriver-manager removes the need to manually download ChromeDriver; Selenium controls Chrome in headless mode.
- Old Reddit: using old.reddit.com simplifies selectors (e.g., div.thing, a.title, div.score) — much more stable for scraping.
- Report generation: the HTML generator is dependency-free (uses Python's html module for safe escaping, simple CSS).
- Separation of concerns: scraper.py collects data, report_generator.py renders it, main.py orchestrates and handles config + saving.

---

## Improvements & production ideas

These are realistic, meaningful upgrades that can be implemented to strengthen the project:
- Use Reddit API (PRAW) — more robust and respectful than scraping.
- Rate limiting & retries — polite scraping with exponential backoff.
- Unit tests — tests for parsing logic and output formats (use sample HTML files).
- Static analysis/linting — add ruff or flake8 in CI.
- Containerization — documented Docker image for reproducible runs.
- Data pipeline — push results to a database (SQLite / Postgres) and add visualization notebooks.
- Dashboard — a small static dashboard (or GitHub Pages) to host daily reports.
- Secrets management — store any API keys in GitHub Secrets (never commit them).

---

## Contributing

Contributions are welcome, and small, focused PRs are best. Suggested workflow:
- Fork the repo
- Create a topic branch: git checkout -b feat/add-tests
- Run tests (if added) and make changes
- Open a PR with an explanation and screenshots if appropriate

---

## License
This project is released under the MIT License — see LICENSE for details.

---

## Acknowledgement
- Selenium and webdriver-manager for making browser automation straightforward.
- Inspiration from many small scraping/reporting projects; assembled here to be clear, reproducible, and presentable.




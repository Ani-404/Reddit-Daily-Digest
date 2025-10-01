# REDDIT DAILY DIGEST

A clean, modular Python project that scrapes informative subreddits, produces CSV + HTML daily reports, and (optionally) commits those reports back to the repository using GitHub Actions.
Built to be reproducible, testable, and presentable, thus making it perfect for demos, portfolio projects, or lightweight research tooling.

Repository: [here](https://github.com/Ani-404/Reddit-Daily-Digest)

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








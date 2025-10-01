# src/scraper.py
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def _safe_parse_score(score_text: str) -> int:
    score_text = (score_text or "").strip()
    # extract first integer (handles "1,234" and plain numbers)
    m = re.search(r'(\d[\d,]*)', score_text)
    if not m:
        return 0
    return int(m.group(1).replace(',', ''))

def scrape_site(site_config):
    """
    Scrapes a single site (e.g., a subreddit) based on site_config:
      - name
      - url
      - posts_to_scrape
    """
    print(f"Scraping site: {site_config['name']}")

    # --- setup driver as before ---
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # TOP-LEVEL guarded block for navigation + debug
        try:
            driver.get(site_config['url'])
        except Exception as e:
            print(f"ERROR: failed to load URL {site_config['url']}: {e}")
            # try to salvage page_source if available, then return empty df
            try:
                print("DEBUG: partial page_source length =", len(driver.page_source or ""))
            except Exception:
                pass
            return pd.DataFrame()  # safe empty result on failure

        # --- DEBUG BLOCK (safe) ---
        try:
            ua = driver.execute_script("return navigator.userAgent")
        except Exception:
            ua = "unknown"

        print("DEBUG: current_url =", driver.current_url)
        print("DEBUG: page title  =", driver.title)
        print("DEBUG: userAgent   =", ua)

        # quick counts for the selectors we attempt
        try:
            count_old = len(driver.find_elements(By.CSS_SELECTOR, "div.thing"))
        except Exception:
            count_old = 0
        try:
            count_new = len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='post-container']"))
        except Exception:
            count_new = 0

        print(f"DEBUG: found elements - old_reddit(div.thing)={count_old}, new_reddit(post-container)={count_new}")

        # Dump a snippet in CI to help debugging
        if os.environ.get("GITHUB_ACTIONS") or os.environ.get("CI"):
            src = driver.page_source or ""
            print("DEBUG: page_source length =", len(src))
            print("DEBUG: page snippet (first 2000 chars):")
            print(src[:2000])
        # --- END DEBUG BLOCK ---

        # proceed with the normal waiting/parsing logic here...
        wait = WebDriverWait(driver, 10)
        # (example) try old reddit then new reddit
        try:
            posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.thing")))
        except Exception:
            try:
                posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='post-container']")))
            except Exception:
                posts = []

        posts_data = []
        for post in posts[: site_config.get("posts_to_scrape", 10)]:
            try:
                # parsing logic (same as earlier)
                # ... obtain title, url, score, content safely ...
                pass  # replace with your parsing block
            except Exception as e:
                print(f"Error parsing a post: {e}")
                continue

        print(f"Found {len(posts_data)} posts from {site_config['name']}.")
        return pd.DataFrame(posts_data)

    finally:
        # ALWAYS quit the driver
        try:
            driver.quit()
        except Exception:
            pass
        # --- END DEBUG BLOCK ---

# def scrape_site(site_config):
#     """
#     Scrapes a single site (e.g., a subreddit) based on site_config:
#       - name
#       - url
#       - posts_to_scrape
#     """
#     print(f"Scraping site: {site_config['name']}")

#     # Setup Chrome options (CI-friendly)
#     chrome_options = Options()
#     # Use new headless mode for recent Chrome + Selenium
#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--window-size=1920,1080")
#     # Make it look like a normal browser
#     chrome_options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#     )
#     # Reduce automation flags
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option("useAutomationExtension", False)

#     service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     try:
#         driver.get(site_config['url'])
#         # Wait up to 10s for posts to appear (old.reddit uses div.thing)
#         wait = WebDriverWait(driver, 10)

#         try:
#             posts = wait.until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.thing"))
#             )
#         except Exception:
#             # Fallback: try new reddit structure
#             try:
#                 posts = wait.until(
#                     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='post-container']"))
#                 )
#             except Exception:
#                 posts = []

#         posts_data = []
#         for post in posts[: site_config.get("posts_to_scrape", 10)]:
#             try:
#                 # Try old-reddit title first
#                 try:
#                     title_element = post.find_element(By.CSS_SELECTOR, "a.title")
#                     title = title_element.text.strip()
#                     url = title_element.get_attribute("href")
#                 except Exception:
#                     # Try new Reddit clickable body link as title
#                     try:
#                         title_element = post.find_element(By.CSS_SELECTOR, "a[data-click-id='body']")
#                         title = title_element.text.strip()
#                         url = title_element.get_attribute("href")
#                     except Exception:
#                         # If no title found, skip
#                         raise RuntimeError("no title element found")

#                 # Score: try common selectors (old reddit then new reddit)
#                 score_text = ""
#                 try:
#                     score_text = post.find_element(By.CSS_SELECTOR, "div.score").text
#                 except Exception:
#                     try:
#                         score_text = post.find_element(By.CSS_SELECTOR, "div[data-click-id='score']").text
#                     except Exception:
#                         score_text = ""

#                 score = _safe_parse_score(score_text)

#                 # Try to get content/body text if present
#                 content = ""
#                 try:
#                     # old reddit
#                     content = post.find_element(By.CSS_SELECTOR, "div.expando, div.md, div.usertext-body").text
#                 except Exception:
#                     try:
#                         # new reddit
#                         content = post.find_element(By.CSS_SELECTOR, "div[data-click-id='text']").text
#                     except Exception:
#                         content = ""

#                 posts_data.append(
#                     {
#                         "title": title,
#                         "url": url,
#                         "score": score,
#                         "content": content,
#                         "source": site_config.get("name"),
#                     }
#                 )
#             except Exception as e:
#                 print(f"Error parsing a post: {e}")
#                 continue

#         print(f"Found {len(posts_data)} posts from {site_config['name']}.")
#         return pd.DataFrame(posts_data)

#     finally:
#         driver.quit()


def scrape_all_sites(configs):
    """Iterate site configs and collect results."""
    all_dataframes = []
    for site_config in configs:
        df = scrape_site(site_config)
        if df is not None and not df.empty:
            all_dataframes.append(df)

    if not all_dataframes:
        return pd.DataFrame()

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    if "score" in combined_df.columns:
        combined_df.sort_values(by="score", ascending=False, inplace=True)
    return combined_df

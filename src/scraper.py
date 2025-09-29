import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_site(site_config):
    """
    Scrapes a single site (e.g., a subreddit) based on the provided configuration.
    Each site_config should have: 
    - 'name': site name (string)
    - 'url': subreddit URL
    - 'posts_to_scrape': number of posts to fetch
    """
    print(f"Scraping site: {site_config['name']}")

    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(site_config['url'])
    time.sleep(2)  # Wait for the page to load

    posts_data = []
    posts = driver.find_elements(By.CSS_SELECTOR, 'div.Post')

    for post in posts[:site_config['posts_to_scrape']]:
        try:
            title = post.find_element(By.CSS_SELECTOR, "h3").text
            url = post.find_element(By.CSS_SELECTOR, "a[data-click-id='body']").get_attribute("href")

            # Get score if present
            try:
                score_text = post.find_element(By.CSS_SELECTOR, "div[data-click-id='score']").text
            except:
                score_text = "0"
            score = 0
            if "k" in score_text.lower():
                score = int(float(score_text.lower().replace("k", "")) * 1000)
            elif score_text.isdigit():
                score = int(score_text)

            # Get content if available
            try:
                content = post.find_element(By.CSS_SELECTOR, "div[data-click-id='text']").text
            except:
                content = ""

            posts_data.append({
                "title": title,
                "url": url,
                "score": score,
                "content": content,
                "source": site_config['name']
            })

        except Exception as e:
            print(f"Error parsing post: {e}")
            continue

    driver.quit()
    print(f"Found {len(posts_data)} posts from {site_config['name']}.")
    return pd.DataFrame(posts_data)

def scrape_all_sites(configs):
    """Iterates through site configurations and scrapes each one."""
    all_dataframes = []
    for site_config in configs:
        df = scrape_site(site_config)
        if not df.empty:
            all_dataframes.append(df)

    if not all_dataframes:
        return pd.DataFrame()

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df.sort_values(by="score", ascending=False, inplace=True)
    return combined_df
            
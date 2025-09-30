import json
import os
import sys
import traceback

from src.scraper import scrape_all_sites
from src.report_generator import generate_html_report
from src.utils import get_today_date_str, ensure_dir_exists

def main(config_path="src/config.json"):
    """Main function to run the daily digest generation."""
    print("Starting Daily Digest generation...")

    # Load configuration
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to parse config file: {e}")
            sys.exit(1)

    sites = config.get("sites", [])
    if not sites:
        print("No sites configured in config['sites']. Exiting.")
        return

    output_dir = config.get("output_dir", "data")
    ensure_dir_exists(output_dir)

    try:
        # Scrape data from all configured sites
        scraped_data = scrape_all_sites(sites)

        if scraped_data.empty:
            print("No data was scraped. Exiting.")
            return

        # Ensure consistent ordering (most popular first)
        if "score" in scraped_data.columns:
            scraped_data.sort_values(by="score", ascending=False, inplace=True)

        # Prepare file paths
        today_str = get_today_date_str()
        csv_path = os.path.join(output_dir, f"{today_str}.csv")
        html_path = os.path.join(output_dir, f"{today_str}.html")

        # Save data to CSV
        print(f"Saving data to CSV at: {csv_path}")
        scraped_data.to_csv(csv_path, index=False)
        print("CSV file saved successfully.")

        # Generate HTML report
        generate_html_report(scraped_data, today_str, html_path)
        print(f"HTML report saved to: {html_path}")

        print("Daily Digest generation finished successfully.")

    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(1)
    except Exception:
        print("An unexpected error occurred:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Accept optional config path: `python main.py path/to/config.json`
    config_arg = sys.argv[1] if len(sys.argv) > 1 else "src/config.json"
    main(config_arg)

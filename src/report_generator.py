# src/report_generator.py
import os
import html
from pathlib import Path
from typing import Optional

def _escape(s: Optional[str]) -> str:
    """Safe HTML escape, handling None values."""
    if s is None:
        return ""
    return html.escape(str(s))

def generate_html_report(df, date_str: str, output_path: str) -> None:
    """
    Generate a simple HTML report from a pandas DataFrame and save it to output_path.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame expected to have columns like: ['title','url','score','content','source']
    date_str : str
        A date string used in the report header (e.g., '2025-09-30')
    output_path : str
        Path where the HTML file will be written.
    """
    # Ensure output directory exists
    out_dir = Path(output_path).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Basic info
    total_posts = 0
    unique_sources = []
    if df is not None and not df.empty:
        total_posts = len(df)
        unique_sources = sorted(df.get("source", []).unique()) if "source" in df.columns else []
        # Ensure we present top posts first if score exists
        if "score" in df.columns:
            df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    else:
        df = None

    # Build HTML
    header = f"Daily Digest — {_escape(date_str)}"
    summary_html = f"<p>Total posts: <strong>{total_posts}</strong></p>"
    if unique_sources:
        summary_html += "<p>Sources: " + ", ".join(f"<strong>{_escape(s)}</strong>" for s in unique_sources) + "</p>"

    styles = """
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; margin: 24px; color: #111;}
      .container { max-width: 1100px; margin: 0 auto; }
      h1 { font-size: 24px; margin-bottom: 6px; }
      .meta { color: #444; margin-bottom: 18px; }
      .post { border-radius: 8px; padding: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); background: #fff; }
      .post .title { font-weight: 600; font-size: 16px; margin-bottom: 6px; }
      .post .meta { color: #666; font-size: 13px; margin-bottom: 8px; }
      .post .content { white-space: pre-wrap; color: #222; }
      .link { color: #1a0dab; text-decoration: none; }
      .small { font-size: 13px; color: #666; }
      .no-data { padding: 24px; background:#fff3cd; border-radius:8px; }
      table.summary { border-collapse: collapse; margin-top: 12px; }
      table.summary td { padding: 4px 8px; }
    </style>
    """

    if df is None or df.empty:
        body = f"""
        <div class="container">
          <h1>{header}</h1>
          <div class="no-data">
            <p>No posts were scraped for this date.</p>
          </div>
        </div>
        """
    else:
        # Build posts HTML (one card per row)
        posts_html = []
        for idx, row in df.iterrows():
            title = _escape(row.get("title", "Untitled"))
            url = row.get("url", "")
            score = _escape(row.get("score", ""))
            source = _escape(row.get("source", ""))
            content = _escape(row.get("content", ""))

            # Make title hyperlink if url available
            if url:
                title_html = f'<a class="link" href="{_escape(url)}" target="_blank" rel="noopener noreferrer">{title}</a>'
            else:
                title_html = title

            post_block = f"""
            <div class="post">
              <div class="title">{title_html}</div>
              <div class="meta small">Score: <strong>{score}</strong> &nbsp;|&nbsp; Source: <strong>{source}</strong></div>
              <div class="content">{content}</div>
            </div>
            """
            posts_html.append(post_block)

        body = f"""
        <div class="container">
          <h1>{header}</h1>
          <div class="meta">{summary_html}</div>
          {"".join(posts_html)}
        </div>
        """

    html_doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{_escape(header)}</title>{styles}</head><body>{body}</body></html>"

    # Write file
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html_doc)

    # No return value — file is written to disk.

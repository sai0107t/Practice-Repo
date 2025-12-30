import re
import csv
import time
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit("Install packages:\npython3 -m pip install requests beautifulsoup4")

BASE_URL = "https://www.cs.stonybrook.edu"
FACULTY_URL = BASE_URL + "/people/faculty"


def fetch(url):
    try:
        r = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"❌ Fetch error {url}: {e}")
        return ""


def extract_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@(?:cs\.)?stonybrook\.edu", text)
    return m.group(0) if m else ""


def scrape_faculty_list():
    html = fetch(FACULTY_URL)
    soup = BeautifulSoup(html, "html.parser")

    # --- Get faculty cards ---
    people = soup.select("div.card")

    if not people:
        print("\n❌ No faculty cards found. Page structure may have changed.\n")
        sys.exit(1)

    print(f"\n✅ Found {len(people)} faculty entries\n")

    faculty = []

    for p in people:
        # Get the profile link
        link = p.find("a")
        if not link:
            continue
        
        rel = link.get("href") or ""
        profile_url = BASE_URL + rel
        
        # Parse the card structure: text nodes separated by newlines
        # Each card has: Name, Title, Research description
        text_parts = []
        for child in p.descendants:
            if isinstance(child, str):
                text = child.strip()
                if text and text != "more":
                    text_parts.append(text)
        
        # Reconstruct: usually first part is name, second is title, rest is research
        name = text_parts[0] if text_parts else ""
        title = text_parts[1] if len(text_parts) > 1 else ""
        research = " ".join(text_parts[2:]) if len(text_parts) > 2 else ""

        faculty.append({
            "name": name,
            "title": title,
            "research": research[:150],  # Truncate research for readability
            "profile_url": profile_url,
        })

    return faculty


def enrich_with_email(faculty):
    print("\n🔍 Fetching profile pages for emails...\n")

    for i, f in enumerate(faculty, start=1):
        print(f"[{i}/{len(faculty)}] {f['name']}")
        html = fetch(f["profile_url"])
        f["email"] = extract_email(html)
        time.sleep(1)

    return faculty


def save_csv(data):
    filename = "stonybrook_cs_faculty.csv"
    keys = ["name", "title", "research", "email", "profile_url"]

    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"\n💾 Saved → {filename}")


if __name__ == "__main__":
    faculty = scrape_faculty_list()
    faculty = enrich_with_email(faculty)
    save_csv(faculty)
    print("\n🎯 Done")

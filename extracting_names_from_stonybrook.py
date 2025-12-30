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


def extract_email(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    
    # Look for spamspan divs that contain the email
    spamspan = soup.find("span", class_="spamspan")
    if spamspan:
        # Extract username and domain from the split HTML
        u_span = spamspan.find("span", class_="u")
        d_span = spamspan.find("span", class_="d")
        
        if u_span and d_span:
            username = u_span.get_text(strip=True)
            domain = d_span.get_text(strip=True)
            return f"{username}@{domain}"
    
    # Fallback: try to find email pattern in plain text
    m = re.search(r"([A-Za-z0-9._-]+)\s*\[at\]\s*(?:cs\.)?stonybrook\.edu", html_text)
    if m:
        username = m.group(1)
        return f"{username}@cs.stonybrook.edu"
    
    # Last resort: look for plain email format
    m = re.search(r"[A-Za-z0-9._%+-]+@(?:cs\.)?stonybrook\.edu", html_text)
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
        
        # Extract text content and split into lines
        text_content = p.get_text()
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        
        # Remove "more" if present
        lines = [line for line in lines if line != "more"]
        
        # Parse: first line is name, second is title, rest is research
        name = lines[0] if len(lines) > 0 else ""
        title = lines[1] if len(lines) > 1 else ""
        research = " ".join(lines[2:]) if len(lines) > 2 else ""

        faculty.append({
            "name": name,
            "title": title,
            "research": research,
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

import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://pmksy.gov.in/mis/rptDIPDocAllStateDistricts.aspx?ccZapuVRQcxji/LEsGyo3vC9aemLktTrbZkbZKhYZf37KjC5K4eyfMnugU5H3ZtHN9v44S9wyU+8Xvp24OPgQXUrafxEOEznkrRSeZqwacZTLbTPZJYCj9twnO9p/DnwS9DVNGyJ32md6pueZ4bspuGp8cy84o6ZvDchs0L1M9c="

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
r = session.get(BASE_URL, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

# Find the table
table = soup.find("table", {"id": "ContentPlaceHolder1_GRD_DIPTargetEntry"})

rows = []
for tr in table.find_all("tr")[1:]:  # skip header
    cols = tr.find_all("td")
    if not cols:
        continue

    state = cols[0].get_text(strip=True)
    district = cols[1].get_text(strip=True)

    # Document code + link
    doc_link_tag = cols[2].find("a")
    doc_code = doc_link_tag.get_text(strip=True)
    doc_url = "https://pmksy.gov.in/mis/" + doc_link_tag["href"]

    date = cols[3].get_text(strip=True)
    title = cols[4].get_text(strip=True)
    description = cols[5].get_text(strip=True)

    rows.append([state, district, doc_code, doc_url, date, title, description])

# Save to CSV
with open("dip_reports.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["State", "District", "Document Code", "Document URL", "Date", "Title", "Description"])
    writer.writerows(rows)

print("Scraping done! Saved dip_reports.csv")

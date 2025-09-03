import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://pmksy.gov.in/mis/rptDIPDocConsolidate.aspx"

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "X-MicrosoftAjax": "Delta=true",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL,
    "Origin": "https://pmksy.gov.in"
}

# GET initial page to fetch hidden fields
resp = session.get(BASE_URL, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

viewstate = soup.find(id="__VIEWSTATE")["value"]
viewstategen = soup.find(id="__VIEWSTATEGENERATOR")["value"]
eventvalidation = soup.find(id="__EVENTVALIDATION")["value"]

# Check for HFToken, skip if not present
hf_token_elem = soup.find(id="ctl00_HFToken")
hf_token = hf_token_elem["value"] if hf_token_elem else None

# Prepare POST payload
payload = {
    "ctl00$ContentPlaceHolder1$ScriptManager1": "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$DDL_FinancialYear",
    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$DDL_FinancialYear",
    "__EVENTARGUMENT": "",
    "__LASTFOCUS": "",
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategen,
    "__EVENTVALIDATION": eventvalidation,
    "ctl00$ContentPlaceHolder1$DDL_FinancialYear": "1001",  # selected year
    "__ASYNCPOST": "true"
}

# Include HFToken only if it exists
if hf_token:
    payload["ctl00$HFToken"] = hf_token

# Send POST request
post_resp = session.post(BASE_URL, data=payload, headers=headers)
html_content = post_resp.text

# Extract table HTML from ASP.NET response
table_html = html_content.split("|")[-1]  # last part contains the table HTML
soup_table = BeautifulSoup(table_html, "html.parser")
table = soup_table.find("table", {"id": "ContentPlaceHolder1_GRD_RegisteredUser"})

html_content

from bs4 import BeautifulSoup
import pandas as pd

# Suppose your HTML content is stored in a variable called 'html_content'
 # replace with your actual HTML

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table
table = soup.find('table')

# Extract headers
headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())

# If there are no th tags, define your own headers
if not headers:
    headers = ['State', 'District_Count', 'SIP', 'Total_DIPD']

from urllib.parse import urljoin

BASE_PREFIX = "https://pmksy.gov.in/mis/"

rows = []
for tr in table.find_all('tr')[1:]:
    cols = tr.find_all('td')
    if len(cols) == 0:
        continue
    row = []
    for td in cols:
        a_tag = td.find('a')
        if a_tag:
            relative_href = a_tag['href']
            full_url = urljoin(BASE_PREFIX, relative_href)
            # Excel-style embedded hyperlink
            row.append(f'=HYPERLINK("{full_url}", "{a_tag.text.strip()}")')
        else:
            row.append(td.get_text(strip=True))
    rows.append(row)


# Create DataFrame
df = pd.DataFrame(rows, columns=headers)

# Save to CSV
df.to_csv('output.csv', index=False)
print("CSV file saved as 'output.csv'")


# # Parse headers
# headers = [th.text.strip() for th in table.find_all("th")]

# # Parse rows
# rows = []
# for tr in table.find_all("tr")[1:]:
#     cols = [td.get_text(strip=True) for td in tr.find_all("td")]
#     if cols:
#         rows.append(cols)

# # Save CSV
# with open("pmksy_dip_consolidated.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(headers)
#     writer.writerows(rows)

# print("CSV saved successfully as pmksy_dip_consolidated.csv")

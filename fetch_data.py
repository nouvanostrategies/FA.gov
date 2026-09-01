import json
import requests

# Set a browser User-Agent header so the API doesn't block the automated request
headers = {"User-Agent": "Mozilla/5.0"}
url = "https://foreignassistance.gov/api/v1/financials?fiscal_year=2024&limit=200"

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    raw_data = response.json().get("data", [])

    summary = {}
    for record in raw_data:
        account = record.get("account_name", "Other")
        disbursed = float(record.get("disbursements", 0) or 0)

        if account not in summary:
            summary[account] = 0
        summary[account] += disbursed

    # Save data.json locally
    with open("data.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Successfully created data.json!")

except Exception as e:
    print(f"Error fetching data: {e}")
    # Create fallback structure so the website doesn't crash completely
    fallback = {"Status": "API request failed, check workflow log"}
    with open("data.json", "w") as f:
        json.dump(fallback, f, indent=2)

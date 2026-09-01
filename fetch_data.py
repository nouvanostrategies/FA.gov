import json
import requests

# Fetch 2024 assistance data from the API
url = (
    "https://foreignassistance.gov/api/v1/financials?fiscal_year=2024&limit=1000"
)
response = requests.get(url)

if response.status_code == 200:
    raw_data = response.json().get("data", [])
    summary = {}

    for record in raw_data:
        account = record.get("account_name", "Other")
        disbursed = float(record.get("disbursements", 0) or 0)

        if account not in summary:
            summary[account] = 0
        summary[account] += disbursed

    # Save the processed data into data.json
    with open("data.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("Successfully created data.json")
else:
    print("Failed to fetch data from API")

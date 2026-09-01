import json
import requests

# ForeignAssistance.gov API endpoint
url = "https://foreignassistance.gov/api/v1/financials?fiscal_year=2024&limit=500"

# Strict headers to prevent ForeignAssistance.gov from blocking GitHub Actions
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://foreignassistance.gov/data",
}

try:
    response = requests.get(url, headers=headers, timeout=25)
    response.raise_for_status()
    payload = response.json()

    # Handle varying JSON array locations in the API response
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = (
            payload.get("data")
            or payload.get("results")
            or payload.get("items")
            or []
        )
    else:
        records = []

    summary = {}

    for item in records:
        # Flexible key lookup for Account Name
        account = (
            item.get("account_name")
            or item.get("treasury_account_name")
            or item.get("agency_name")
            or "Uncategorized Program"
        )

        # Flexible key lookup for Disbursements / Obligations
        disbursed = float(
            item.get("disbursements")
            or item.get("disbursement_amount")
            or item.get("obligations")
            or 0
        )

        summary[account] = summary.get(account, 0) + disbursed

    # If the API returned no matching records, populate with a clear indicator
    if not summary:
        summary = {"Notice": "API connected successfully but returned 0 records for FY2024"}

    # Write output to data.json
    with open("data.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Successfully wrote data.json from ForeignAssistance.gov API!")

except Exception as err:
    print(f"Fetch Error: {err}")
    # Write error state to data.json so the website displays the failure reason
    with open("data.json", "w") as f:
        json.dump({"API_Error_Log": str(err)}, f, indent=2)

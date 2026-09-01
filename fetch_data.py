import json
import requests

# Updated official ForeignAssistance.gov API endpoint hosted on USAID's open data platform
url = "https://api.usaid.gov/foreignassistance/v1/financials"

# Parameters for Fiscal Year 2024 data
params = {
    "fiscal_year": 2024,
    "page_size": 250
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

try:
    response = requests.get(url, params=params, headers=headers, timeout=25)
    response.raise_for_status()
    payload = response.json()

    # The API returns data wrapped inside a results or data array
    records = payload.get("results") or payload.get("data") or []

    summary = {}

    for item in records:
        # Get account name or agency name
        account = (
            item.get("account_name")
            or item.get("treasury_account_name")
            or item.get("agency_name")
            or "General Foreign Assistance"
        )

        # Get disbursement or obligation dollar amounts
        disbursed = float(
            item.get("disbursements")
            or item.get("disbursement_amount")
            or item.get("obligations")
            or 0
        )

        summary[account] = summary.get(account, 0) + disbursed

    # Fallback structure if the response array was empty
    if not summary:
        summary = {"Notice": "API connected but no financial records returned for FY2024"}

    # Save to data.json
    with open("data.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Successfully fetched ForeignAssistance.gov data!")

except Exception as err:
    print(f"Error fetching data: {err}")
    with open("data.json", "w") as f:
        json.dump({"API_Error_Log": str(err)}, f, indent=2)

import json
import os
import sys
from pathlib import Path

import requests

WEBEX_API_URL = "https://webexapis.com/v1/messages"

def load_counts(report_path: Path):
    if not report_path.exists():
        return None

    with report_path.open() as f:
        data = json.load(f)

    # Similar counting logic as in evaluate_trivy.py
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "UNKNOWN": 0,
    }

    results = data if isinstance(data, list) else data.get("Results", [])
    for result in results:
        vulns = result.get("Vulnerabilities") or []
        for v in vulns:
            sev = v.get("Severity", "").upper()
            if sev in counts:
                counts[sev] += 1
            else:
                counts["UNKNOWN"] += 1

    return counts

def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python send_webex_notification.py "
            "<room_id> <status> <build_number> <job_name> <build_url>"
        )
        sys.exit(1)

    room_id = sys.argv[1]
    status = sys.argv[2]
    build_number = sys.argv[3]
    job_name = sys.argv[4]
    build_url = sys.argv[5]

    bot_token = os.environ.get("WEBEX_BOT_TOKEN")
    if not bot_token:
        print("ERROR: WEBEX_BOT_TOKEN environment variable not set")
        sys.exit(1)

    report_path = Path("trivy-report.json")
    counts = load_counts(report_path)

    if counts:
        vuln_summary = (
            f"CRITICAL: {counts['CRITICAL']}, "
            f"HIGH: {counts['HIGH']}, "
            f"MEDIUM: {counts['MEDIUM']}, "
            f"LOW: {counts['LOW']}, "
            f"UNKNOWN: {counts['UNKNOWN']}"
        )
    else:
        vuln_summary = "No Trivy report found."

    text = (
        f"Jenkins build notification\n"
        f"Job: {job_name}\n"
        f"Build: #{build_number}\n"
        f"Status: {status}\n"
        f"Vulnerabilities: {vuln_summary}\n"
        f"Details: {build_url}"
    )

    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "roomId": room_id,
        "text": text,
    }

    response = requests.post(WEBEX_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Failed to send Webex message: {response.status_code} {response.text}")
        sys.exit(1)
    else:
        print("Webex notification sent successfully.")

if __name__ == "__main__":
    main()

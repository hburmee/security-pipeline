import json
import sys
from pathlib import Path

def count_vulnerabilities(report):
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "UNKNOWN": 0,
    }

    # Trivy JSON: list of results, each with Vulnerabilities list
    results = report if isinstance(report, list) else report.get("Results", [])

    for result in results:
        vulns = result.get("Vulnerabilities") or []
        for v in vulns:
            severity = v.get("Severity", "").upper()
            if severity in counts:
                counts[severity] += 1
            else:
                counts["UNKNOWN"] += 1

    return counts

def main():
    if len(sys.argv) != 2:
        print("Usage: python evaluate_trivy.py <trivy-report.json>")
        sys.exit(1)

    report_path = Path(sys.argv[1])
    if not report_path.exists():
        print(f"ERROR: Report file not found: {report_path}")
        sys.exit(1)

    with report_path.open() as f:
        data = json.load(f)

    counts = count_vulnerabilities(data)

    print("=== Trivy Vulnerability Summary ===")
    for sev, count in counts.items():
        print(f"{sev}: {count}")

    # Decide policy: fail if any CRITICAL or HIGH
    critical = counts["CRITICAL"]
    high = counts["HIGH"]

    if critical > 0 or high > 0:
        print("\nPolicy: FAIL (CRITICAL or HIGH vulnerabilities found)")
        sys.exit(1)
    else:
        print("\nPolicy: PASS (No HIGH/CRITICAL vulnerabilities)")
        sys.exit(0)

if __name__ == "__main__":
    main()

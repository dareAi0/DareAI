
import os
import re

def scan_file_for_vulns(file_path):
    vulns = []
    patterns = {
        "SQL Injection": r"(SELECT|INSERT|UPDATE|DELETE).*['\"]\s*\+\s*.*input\(",
        "XSS": r"(<script>|document\.write|innerHTML\s*=)",
        "Command Injection": r"(os\.system|subprocess\.Popen|eval\()",
        "Hardcoded Password": r"(password\s*=\s*['\"])"
    }

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        for vuln_type, pattern in patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                vulns.append((i, vuln_type, line.strip()))
    return vulns

def generate_report(vulns, file_path):
    report_path = "data/scans/vuln_report.txt"
    os.makedirs("data/scans", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Vulnerability Report for {file_path}\n")
        f.write("=" * 50 + "\n")
        if not vulns:
            f.write("No critical vulnerabilities found.\n")
        else:
            for line_num, vuln_type, content in vulns:
                f.write(f"[Line {line_num}] {vuln_type}: {content}\n")
    return report_path

def main():
    target_file = "test_target.py"
    if not os.path.exists(target_file):
        print("File not found: test_target.py")
        return
    vulns = scan_file_for_vulns(target_file)
    report = generate_report(vulns, target_file)
    print("Code scan complete. Report saved to:", report)

if __name__ == "__main__":
    main()

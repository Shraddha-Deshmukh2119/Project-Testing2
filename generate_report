import json

# Load metrics JSON
with open("sonar_metrics.json", "r") as f:
    metrics_data = json.load(f)

# Load issues JSON
with open("sonar_issues.json", "r") as f:
    issues_data = json.load(f)

report = "\n========== SONARQUBE REPORT ==========\n\n"

# Extract metrics
measures = metrics_data["component"]["measures"]

for measure in measures:
    metric_name = measure["metric"]
    metric_value = measure["value"]
    report += f"{metric_name.upper()} : {metric_value}\n"

report += "\n========== ISSUES ==========\n\n"

issues = issues_data["issues"]

if not issues:
    report += "No issues found.\n"
else:
    for issue in issues[:10]:  # show only first 10 issues
        report += f"File       : {issue.get('component')}\n"
        report += f"Type       : {issue.get('type')}\n"
        report += f"Severity   : {issue.get('severity')}\n"
        report += f"Message    : {issue.get('message')}\n"
        report += f"Line       : {issue.get('line')}\n"
        report += "-----------------------------------\n"

# Save report as text file
with open("sonar_readable_report.txt", "w") as f:
    f.write(report)

print(report)

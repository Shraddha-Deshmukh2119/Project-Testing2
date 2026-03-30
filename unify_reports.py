import xml.etree.ElementTree as ET
import json
import os

def get_raw_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "File not found"

def get_java_metrics(path):
    if not os.path.exists(path): return {"line_coverage": "0%", "stats": {"lines_covered": 0, "lines_total": 0}}
    root = ET.parse(path).getroot()
    line = root.find("./counter[@type='LINE']")
    branch = root.find("./counter[@type='BRANCH']")
    c = int(line.get('covered', 0)); m = int(line.get('missed', 0))
    bc = int(branch.get('covered', 0)) if branch is not None else 0
    bm = int(branch.get('missed', 0)) if branch is not None else 0
    return {
        "line_coverage": f"{round((c/(c+m))*100, 2)}%" if (c+m) > 0 else "0%",
        "branch_coverage": f"{round((bc/(bc+bm))*100, 2)}%" if (bc+bm) > 0 else "0%",
        "stats": {"lines_covered": c, "lines_total": c+m, "branches_covered": bc, "branches_total": bc+bm},
        "raw_xml": get_raw_content(path)
    }

def get_cpp_metrics(path):
    if not os.path.exists(path): return {"line_coverage": "0%", "stats": {"lines_covered": 0, "lines_total": 0}}
    root = ET.parse(path).getroot()
    lc = int(root.get('lines-covered', 0)); lv = int(root.get('lines-valid', 0))
    bc = int(root.get('branches-covered', 0)); bv = int(root.get('branches-valid', 0))
    return {
        "line_coverage": f"{round((lc/lv)*100, 2)}%" if lv > 0 else "0%",
        "branch_coverage": f"{round((bc/bv)*100, 2)}%" if bv > 0 else "0%",
        "stats": {"lines_covered": lc, "lines_total": lv, "branches_covered": bc, "branches_total": bv},
        "raw_xml": get_raw_content(path)
    }

def main():
    java_xml = "java-project/target/site/jacoco/jacoco.xml"
    cpp_xml = "cpp-project/sonar-cpp-coverage.xml"
    
    java_data = get_java_metrics(java_xml)
    cpp_data = get_cpp_metrics(cpp_xml)
    
    # Combined Average Calculation
    total_cov = java_data['stats']['lines_covered'] + cpp_data['stats']['lines_covered']
    total_all = java_data['stats']['lines_total'] + cpp_data['stats']['lines_total']
    weighted_avg = round((total_cov / total_all) * 100, 2) if total_all > 0 else 0

    # Initialize separate issue buckets
    java_issues = []; cpp_issues = []
    
    if os.path.exists("sonar_detailed_issues.json"):
        with open("sonar_detailed_issues.json", "r") as f:
            all_issues = json.load(f).get("issues", [])
            for issue in all_issues:
                # Sort issues based on file path
                component = issue.get("component", "")
                if "java-project" in component: java_issues.append(issue)
                elif "cpp-project" in component: cpp_issues.append(issue)

    report = {
        "metadata": {
            "project": "Unified Multi-Language Analysis",
            "overall_weighted_coverage": f"{weighted_avg}%",
            "quality_status": "PASS" if weighted_avg > 80 else "FAIL"
        },
        "languages": {
            "java_analysis": {
                "local_metrics": {
                    "line_pct": java_data["line_coverage"],
                    "branch_pct": java_data["branch_coverage"],
                    "raw_stats": java_data["stats"]
                },
                "sonarcloud_issues": java_issues,
                "xml_source": java_data["raw_xml"]
            },
            "cpp_analysis": {
                "local_metrics": {
                    "line_pct": cpp_data["line_coverage"],
                    "branch_pct": cpp_data["branch_coverage"],
                    "raw_stats": cpp_data["stats"]
                },
                "sonarcloud_issues": cpp_issues,
                "xml_source": cpp_data["raw_xml"]
            }
        },
        "full_sonarcloud_api_dump": {}
    }

    if os.path.exists("sonar_metrics.json"):
        with open("sonar_metrics.json", "r") as f:
            report["full_sonarcloud_api_dump"] = json.load(f)

    with open("unified_master_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"Full Report Generated. Average: {weighted_avg}%")

if __name__ == "__main__":
    main()

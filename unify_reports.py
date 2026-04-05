import xml.etree.ElementTree as ET
import json
import os

def get_java_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0, "branches_covered": 0, "branches_total": 0}
    root = ET.parse(path).getroot()
    line = root.find("./counter[@type='LINE']")
    branch = root.find("./counter[@type='BRANCH']")
    
    c = int(line.get('covered', 0))
    m = int(line.get('missed', 0))
    bc = int(branch.get('covered', 0)) if branch is not None else 0
    bm = int(branch.get('missed', 0)) if branch is not None else 0
    
    return {
        "line_coverage": f"{round((c/(c+m))*100, 2)}%" if (c+m) > 0 else "0%",
        "branch_coverage": f"{round((bc/(bc+bm))*100, 2)}%" if (bc+bm) > 0 else "0%",
        "stats": {"lines_covered": c, "lines_total": c+m, "branches_covered": bc, "branches_total": bc+bm}
    }

def get_cpp_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0}
    root = ET.parse(path).getroot()
    lc = int(root.get('lines-covered', 0))
    lv = int(root.get('lines-valid', 0))
    bc = int(root.get('branches-covered', 0))
    bv = int(root.get('branches-valid', 0))
    
    return {
        "line_coverage": f"{round((lc/lv)*100, 2)}%" if lv > 0 else "0%",
        "branch_coverage": f"{round((bc/bv)*100, 2)}%" if bv > 0 else "0%",
        "stats": {"lines_covered": lc, "lines_total": lv, "branches_covered": bc, "branches_total": bv}
    }

def main():
    java = get_java_metrics("java-project/target/site/jacoco/jacoco.xml")
    cpp = get_cpp_metrics("cpp-project/sonar-cpp-coverage.xml")
    
    # Calculate TRUE Combined Weighted Average
    total_covered = java['stats']['lines_covered'] + cpp['stats']['lines_covered']
    total_lines = java['stats']['lines_total'] + cpp['stats']['lines_total']
    weighted_avg = round((total_covered / total_lines) * 100, 2) if total_lines > 0 else 0

    report = {
        "project_summary": {
            "final_score": f"{weighted_avg}%",
            "quality_gate": "PASSED" if weighted_avg > 80 else "FAILED",
            "languages": ["Java", "C++"]
        },
        "detailed_analysis": { "java": java, "cpp": cpp },
        "sonar_cloud_full_sync": {},
        "active_issues": []
    }

    # Load the metric data
    if os.path.exists("sonar_metrics.json"):
        with open("sonar_metrics.json", "r") as f:
            report["sonar_cloud_full_sync"] = json.load(f)

    # Load the DETAILED issues (The "Full" part)
    if os.path.exists("sonar_detailed_issues.json"):
        with open("sonar_detailed_issues.json", "r") as f:
            issues_data = json.load(f)
            report["active_issues"] = issues_data.get("issues", [])

    with open("unified_master_report.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()

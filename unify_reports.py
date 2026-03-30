import xml.etree.ElementTree as ET
import json
import os

def get_java_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0, "pct": 0}
    root = ET.parse(path).getroot()
    line_counter = root.find("./counter[@type='LINE']")
    if line_counter is not None:
        c = int(line_counter.get('covered'))
        m = int(line_counter.get('missed'))
        return {"covered": c, "total": c + m, "pct": round((c/(c+m))*100, 2)}
    return {"covered": 0, "total": 0, "pct": 0}

def get_cpp_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0, "pct": 0}
    root = ET.parse(path).getroot()
    c = int(root.get('lines-covered', 0))
    v = int(root.get('lines-valid', 0))
    return {"covered": c, "total": v, "pct": round((c/v)*100, 2) if v > 0 else 0}

def main():
    java_xml = "java-project/target/site/jacoco/jacoco.xml"
    cpp_xml = "cpp-project/sonar-cpp-coverage.xml"
    
    java = get_java_metrics(java_xml)
    cpp = get_cpp_metrics(cpp_xml)
    
    # Calculate TRUE Weighted Average
    total_cov = java['covered'] + cpp['covered']
    total_lines = java['total'] + cpp['total']
    weighted_avg = round((total_cov / total_lines) * 100, 2) if total_lines > 0 else 0

    # Build the Neat JSON Structure
    report = {
        "report_metadata": {
            "project_name": "Unified Multi-Language System",
            "final_weighted_coverage": f"{weighted_avg}%",
            "status": "PASS" if weighted_avg > 80 else "FAIL"
        },
        "language_stats": {
            "java": java,
            "cpp": cpp
        },
        "sonar_cloud_sync": {}
    }

    # Load API data if available
    if os.path.exists("sonar_metrics.json"):
        with open("sonar_metrics.json", "r") as f:
            report["sonar_cloud_sync"] = json.load(f)

    # Save with 2-space indentation for neatness
    with open("unified_master_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Success! Final Weighted Average: {weighted_avg}%")

if __name__ == "__main__":
    main()

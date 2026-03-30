import xml.etree.ElementTree as ET
import json
import os

def get_xml_raw(path):
    return open(path, 'r', encoding='utf-8').read() if os.path.exists(path) else "Missing"

def get_java_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0, "pct": 0}
    root = ET.parse(path).getroot()
    line_counter = root.find("./counter[@type='LINE']")
    if line_counter is not None:
        c, m = int(line_counter.get('covered')), int(line_counter.get('missed'))
        return {"covered": c, "total": c + m, "pct": round((c/(c+m))*100, 2)}
    return {"covered": 0, "total": 0, "pct": 0}

def get_cpp_metrics(path):
    if not os.path.exists(path): return {"covered": 0, "total": 0, "pct": 0}
    root = ET.parse(path).getroot()
    c, v = int(root.get('lines-covered', 0)), int(root.get('lines-valid', 0))
    return {"covered": c, "total": v, "pct": round((c/v)*100, 2) if v > 0 else 0}

def main():
    j_path, c_path = "java-project/target/site/jacoco/jacoco.xml", "cpp-project/sonar-cpp-coverage.xml"
    java, cpp = get_java_metrics(j_path), get_cpp_metrics(c_path)
    
    # Calculate the TRUE Weighted Average
    total_cov = java['covered'] + cpp['covered']
    total_lines = java['total'] + cpp['total']
    project_avg = round((total_cov / total_lines) * 100, 2) if total_lines > 0 else 0

    report = {
        "report_metadata": {
            "project_name": "Unified Multi-Language System",
            "status": "SUCCESS" if project_avg > 80 else "WARNING",
            "final_weighted_coverage": f"{project_avg}%"
        },
        "language_breakdown": {
            "java": java,
            "cpp": cpp
        },
        "cloud_sync": {},
        "raw_data_blobs": {
            "jacoco_xml": get_xml_raw(j_path),
            "gcovr_xml": get_xml_raw(c_path)
        }
    }

    if os.path.exists("sonar_metrics.json"):
        with open("sonar_metrics.json", "r") as f:
            report["cloud_sync"] = json.load(f)

    with open("unified_master_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"Done! Final Weighted Coverage: {project_avg}%")

if __name__ == "__main__":
    main()

import xml.etree.ElementTree as ET
import json
import os

def get_xml_raw(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "File Not Found"

def get_java_metrics(path):
    if not os.path.exists(path): return {"error": "Missing Java XML"}
    tree = ET.parse(path)
    root = tree.getroot()
    # Find the 'LINE' counter for the whole project
    line_counter = root.find("./counter[@type='LINE']")
    if line_counter is not None:
        missed = int(line_counter.get('missed'))
        covered = int(line_counter.get('covered'))
        percentage = (covered / (covered + missed)) * 100 if (covered + missed) > 0 else 0
        return {"covered": covered, "missed": missed, "percentage": round(percentage, 2)}
    return {"percentage": 0}

def get_cpp_metrics(path):
    if not os.path.exists(path): return {"error": "Missing C++ XML"}
    tree = ET.parse(path)
    root = tree.getroot()
    # Gcovr/Cobertura format uses 'line-rate' attribute (0.0 to 1.0)
    line_rate = float(root.get('line-rate', 0))
    return {
        "percentage": round(line_rate * 100, 2),
        "lines_covered": root.get('lines-covered'),
        "lines_valid": root.get('lines-valid')
    }

def main():
    java_xml_path = "java-project/target/site/jacoco/jacoco.xml"
    cpp_xml_path = "cpp-project/sonar-cpp-coverage.xml"

    unified_report = {
        "summary": {
            "java_coverage": get_java_metrics(java_xml_path),
            "cpp_coverage": get_cpp_metrics(cpp_xml_path)
        },
        "sonar_cloud_data": {},
        "raw_xml_content": {
            "java_jacoco": get_xml_raw(java_xml_path),
            "cpp_gcovr": get_xml_raw(cpp_xml_path)
        }
    }

    # Load the SonarCloud API JSONs if they exist
    if os.path.exists("sonar_metrics.json"):
        with open("sonar_metrics.json", "r") as f:
            unified_report["sonar_cloud_data"] = json.load(f)

    with open("unified_master_report.json", "w") as f:
        json.dump(unified_report, f, indent=4)
    print("Success: unified_master_report.json generated.")

if __name__ == "__main__":
    main()

import xml.etree.ElementTree as ET
import json
import requests
import os

# --- CONFIGURATION ---
SONAR_PROJECT_KEY = "Shraddha-Deshmukh2119_Project-Testing2"
SONAR_ORG = "shraddha-deshmukh2119"
# The token is usually passed as an environment variable in Jenkins
SONAR_TOKEN = os.getenv('SONAR_TOKEN') 

JAVA_XML_PATH = "java-project/target/site/jacoco/jacoco.xml"
CPP_XML_PATH = "cpp-project/sonar-cpp-coverage.xml"

def get_java_details(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        data = {"classes": [], "totals": {}}
        
        for package in root.findall('package'):
            for sourcefile in package.findall('sourcefile'):
                data["classes"].append({
                    "name": f"{package.get('name')}/{sourcefile.get('name').replace('.java', '')}",
                    "lines_missed": next(c.get('missed') for c in sourcefile.findall('counter') if c.get('type') == 'LINE')
                })
        
        for counter in root.findall('counter'):
            data["totals"][counter.get('type')] = {
                "missed": counter.get('missed'),
                "covered": counter.get('covered')
            }
        return data
    except Exception: return {}

def get_cpp_details(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return {
            "line_rate": root.get("line-rate"),
            "branch_rate": root.get("branch-rate"),
            "lines_covered": root.get("lines-covered"),
            "lines_valid": root.get("lines-valid")
        }
    except Exception: return {}

def fetch_sonar_data():
    headers = {'Authorization': f'Bearer {SONAR_TOKEN}'}
    
    # 1. Fetch Measures (Coverage, Bugs, etc.)
    measures_url = f"https://sonarcloud.io/api/measures/component?component={SONAR_PROJECT_KEY}&metricKeys=coverage,bugs,code_smells,uncovered_lines,vulnerabilities"
    
    # 2. Fetch Issues (The actual bug list)
    issues_url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT_KEY}&ps=100"
    
    try:
        m_resp = requests.get(measures_url, headers=headers).json()
        i_resp = requests.get(issues_url, headers=headers).json()
        return m_resp.get('component', {}), i_resp
    except Exception as e:
        print(f"Error fetching Sonar data: {e}")
        return {}, {}

def main():
    java_data = get_java_details(JAVA_XML_PATH)
    cpp_data = get_cpp_details(CPP_XML_PATH)
    sonar_measures, sonar_issues = fetch_sonar_data()

    unified_report = {
        "metadata": {"status": "Success", "version": "2.0"},
        "java_detailed": java_data,
        "cpp_detailed": cpp_data,
        "sonar_cloud_analysis": {"component": sonar_measures},
        "issues_and_bugs": sonar_issues
    }

    with open("unified_master_report.json", "w") as f:
        json.dump(unified_report, f, indent=4)
    
    print("Unified Report Generated: unified_master_report.json")

if __name__ == "__main__":
    main()

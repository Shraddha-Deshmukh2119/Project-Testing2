import xml.etree.ElementTree as ET
import json
import urllib.request
import urllib.error
import base64
import os

# --- CONFIGURATION ---
SONAR_PROJECT_KEY = "Shraddha-Deshmukh2119_Project-Testing2"
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

def fetch_from_sonar(url):
    # SonarCloud uses Basic Auth (Token + empty password)
    auth_str = f"{SONAR_TOKEN}:"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_auth}"}
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching from Sonar: {e}")
        return {}

def main():
    # 1. Parse Local XMLs
    java_data = get_java_details(JAVA_XML_PATH)
    cpp_data = get_cpp_details(CPP_XML_PATH)

    # 2. Fetch from SonarCloud API using urllib
    measures_url = f"https://sonarcloud.io/api/measures/component?component={SONAR_PROJECT_KEY}&metricKeys=coverage,bugs,code_smells,uncovered_lines,vulnerabilities"
    issues_url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT_KEY}&ps=100"
    
    sonar_measures = fetch_from_sonar(measures_url).get('component', {})
    sonar_issues = fetch_from_sonar(issues_url)

    # 3. Create Unified JSON
    unified_report = {
        "metadata": {"status": "Success", "version": "2.0"},
        "java_detailed": java_data,
        "cpp_detailed": cpp_data,
        "sonar_cloud_analysis": {"component": sonar_measures},
        "issues_and_bugs": sonar_issues
    }

    # 4. Save to file
    with open("unified_master_report.json", "w") as f:
        json.dump(unified_report, f, indent=4)
    
    print("Unified Report Generated successfully without external libraries!")

if __name__ == "__main__":
    main()

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
    """
    Parses SonarQube Generic Coverage XML to match the Java detailed format.
    """
    try:
        if not os.path.exists(xml_path):
            return {}
            
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        data = {"classes": [], "totals": {}}
        
        # Initialize totals
        total_l_miss, total_l_cov = 0, 0
        total_b_miss, total_b_cov = 0, 0

        for file_node in root.findall('file'):
            # Extract clean filename from path
            full_path = file_node.get('path')
            file_name = full_path.split('/')[-1] if '/' in full_path else full_path.split('\\')[-1]
            
            file_l_miss = 0
            
            for line in file_node.findall('lineToCover'):
                is_covered = line.get('covered') == 'true'
                
                # Line Counting
                if is_covered:
                    total_l_cov += 1
                else:
                    total_l_miss += 1
                    file_l_miss += 1
                
                # Branch Counting (if exists)
                branches = line.get('branchesToCover')
                if branches:
                    b_to_cover = int(branches)
                    b_covered = int(line.get('coveredBranches', 0))
                    total_b_cov += b_covered
                    total_b_miss += (b_to_cover - b_covered)

            data["classes"].append({
                "name": file_name,
                "lines_missed": str(file_l_miss)
            })

        # Structure totals exactly like Java section
        data["totals"] = {
            "LINE": {"missed": str(total_l_miss), "covered": str(total_l_cov)},
            "BRANCH": {"missed": str(total_b_miss), "covered": str(total_b_cov)}
        }
        return data
    except Exception as e:
        print(f"Error parsing C++ XML: {e}")
        return {}

def fetch_from_sonar(url):
    if not SONAR_TOKEN:
        print("Error: SONAR_TOKEN environment variable is not set.")
        return {}
    
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

    # 2. Fetch from SonarCloud API
    measures_url = f"https://sonarcloud.io/api/measures/component?component={SONAR_PROJECT_KEY}&metricKeys=coverage,bugs,code_smells,uncovered_lines,vulnerabilities"
    issues_url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT_KEY}&ps=100"
    
    measures_resp = fetch_from_sonar(measures_url)
    sonar_measures = measures_resp.get('component', {})
    sonar_issues = fetch_from_sonar(issues_url)

    # 3. Create Unified JSON
    unified_report = {
        "metadata": {"status": "Success", "version": "2.0"},
        "java_detailed": java_data,
        "cpp_detailed": cpp_data, # Now matches Java structure
        "sonar_cloud_analysis": {"component": sonar_measures},
        "issues_and_bugs": sonar_issues
    }

    # 4. Save to file
    with open("unified_master_report.json", "w") as f:
        json.dump(unified_report, f, indent=4)
    
    print("Unified Report Generated successfully with detailed C++ and Java metrics!")

if __name__ == "__main__":
    main()

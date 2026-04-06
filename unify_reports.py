import xml.etree.ElementTree as ET
import json
import os

def parse_jacoco(file_path):
    if not os.path.exists(file_path): return None
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {"classes": [], "totals": {}}
    for package in root.findall('package'):
        for cls in package.findall('class'):
            line_counter = next((c for c in cls.findall('counter') if c.get('type') == 'LINE'), None)
            missed = line_counter.get('missed') if line_counter is not None else "0"
            data["classes"].append({"name": cls.get('name'), "lines_missed": missed})
    for counter in root.findall('counter'):
        data["totals"][counter.get('type')] = {"missed": counter.get('missed'), "covered": counter.get('covered')}
    return data

def parse_cpp_sonar_detailed(file_path):
    if not os.path.exists(file_path): return None
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cpp_detailed = {"classes": [], "totals": {}}
    total_l_cov, total_l_miss = 0, 0
    total_b_cov, total_b_miss = 0, 0

    for file_node in root.findall('file'):
        file_name = file_node.get('path').split('/')[-1] # Get bank.cpp instead of full path
        file_l_miss = 0
        
        for line in file_node.findall('lineToCover'):
            is_covered = line.get('covered') == 'true'
            # Line tracking
            if is_covered: total_l_cov += 1
            else: 
                total_l_miss += 1
                file_l_miss += 1
            
            # Branch tracking (if available in the XML)
            branches = line.get('branchesToCover')
            if branches:
                b_to_cover = int(branches)
                b_covered = int(line.get('coveredBranches', 0))
                total_b_cov += b_covered
                total_b_miss += (b_to_cover - b_covered)

        cpp_detailed["classes"].append({"name": file_name, "lines_missed": str(file_l_miss)})

    cpp_detailed["totals"] = {
        "LINE": {"missed": str(total_l_miss), "covered": str(total_l_cov)},
        "BRANCH": {"missed": str(total_b_miss), "covered": str(total_b_cov)}
    }
    return cpp_detailed

# Main Execution
java_info = parse_jacoco('java-project/target/site/jacoco/jacoco.xml')
cpp_info = parse_cpp_sonar_detailed('cpp-project/sonar-cpp-coverage.xml')

sonar_json = {}
if os.path.exists('sonar_metrics.json'):
    with open('sonar_metrics.json', 'r') as f:
        sonar_json = json.load(f)

final_report = {
    "metadata": {"status": "Success", "version": "2.2"},
    "java_detailed": java_info,
    "cpp_detailed": cpp_info, # Now follows the Java format!
    "sonar_cloud_analysis": sonar_json
}

with open('unified_master_report.json', 'w') as f:
    json.dump(final_report, f, indent=2)

print("Report generated with detailed C++ metrics.")

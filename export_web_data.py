import csv
import json
import os

BASE_DIR = r"C:\Users\Himabala\.gemini\antigravity-ide\scratch\hr_analytics_powerbi"
DATA_DIR = os.path.join(BASE_DIR, "data")

def read_csv(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

departments = read_csv("Dim_Department.csv")
job_roles = read_csv("Dim_JobRole.csv")
employees = read_csv("Dim_Employee.csv")
attrition = read_csv("Fact_Attrition.csv")
performance = read_csv("Fact_Performance.csv")
payroll = read_csv("Fact_Payroll.csv")

# Create lookup maps
dept_map = {d["DepartmentID"]: d["DepartmentName"] for d in departments}
role_map = {r["JobRoleID"]: r for r in job_roles}

# Enrich employees with DeptName and JobTitle
for emp in employees:
    emp["DepartmentName"] = dept_map.get(emp["DepartmentID"], "Unknown")
    r = role_map.get(emp["JobRoleID"], {})
    emp["JobTitle"] = r.get("JobTitle", "Unknown")
    emp["JobLevel"] = r.get("JobLevel", "Unknown")

app_payload = {
    "departments": departments,
    "job_roles": job_roles,
    "employees": employees,
    "attrition": attrition,
    "performance": performance,
    "payroll": payroll
}

# Write app_data.js
js_content = f"window.HR_DATA = {json.dumps(app_payload)};"

with open(os.path.join(BASE_DIR, "app_data.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"app_data.js created successfully with {len(employees)} employees and complete relational facts.")

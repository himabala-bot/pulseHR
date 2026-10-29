import json
import os

BASE_DIR = r"C:\Users\Himabala\.gemini\antigravity-ide\scratch\hr_analytics_powerbi"
REPORT_DIR = os.path.join(BASE_DIR, "HR_Analytics.Report")
MODEL_DIR = os.path.join(BASE_DIR, "HR_Analytics.SemanticModel")
DATA_DIR = os.path.join(BASE_DIR, "data").replace("\\", "/")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# 1. HR_Analytics.pbip
pbip_content = {
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": "HR_Analytics.Report"
            }
        }
    ],
    "settings": {
        "enableAutoAuth": True
    }
}
with open(os.path.join(BASE_DIR, "HR_Analytics.pbip"), "w", encoding="utf-8") as f:
    json.dump(pbip_content, f, indent=2)

# 2. HR_Analytics.Report/definition.pbir
pbir_content = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": "../HR_Analytics.SemanticModel"
        },
        "byConnection": None
    }
}
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir_content, f, indent=2)

# 3. HR_Analytics.SemanticModel/definition.pbism
pbism_content = {
    "version": "1.0"
}
with open(os.path.join(MODEL_DIR, "definition.pbism"), "w", encoding="utf-8") as f:
    json.dump(pbism_content, f, indent=2)

# 4. HR_Analytics.SemanticModel/model.bim
def make_csv_partition(filename):
    csv_path = f"{DATA_DIR}/{filename}"
    m_expr = [
        "let",
        f'    Source = Csv.Document(File.Contents("{csv_path}"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])',
        "in",
        '    #"Promoted Headers"'
    ]
    return {
        "name": "Partition",
        "dataView": "full",
        "source": {
            "type": "m",
            "expression": m_expr
        }
    }

# Build tables
tables = [
    {
        "name": "Dim_Department",
        "columns": [
            {"name": "DepartmentID", "dataType": "int64", "sourceColumn": "DepartmentID"},
            {"name": "DepartmentName", "dataType": "string", "sourceColumn": "DepartmentName"},
            {"name": "Division", "dataType": "string", "sourceColumn": "Division"},
            {"name": "CostCenter", "dataType": "string", "sourceColumn": "CostCenter"},
            {"name": "DepartmentHead", "dataType": "string", "sourceColumn": "DepartmentHead"}
        ],
        "partitions": [make_csv_partition("Dim_Department.csv")]
    },
    {
        "name": "Dim_JobRole",
        "columns": [
            {"name": "JobRoleID", "dataType": "int64", "sourceColumn": "JobRoleID"},
            {"name": "DepartmentID", "dataType": "int64", "sourceColumn": "DepartmentID"},
            {"name": "JobTitle", "dataType": "string", "sourceColumn": "JobTitle"},
            {"name": "JobLevel", "dataType": "string", "sourceColumn": "JobLevel"},
            {"name": "PayGrade", "dataType": "string", "sourceColumn": "PayGrade"},
            {"name": "MinSalary", "dataType": "double", "sourceColumn": "MinSalary"},
            {"name": "MaxSalary", "dataType": "double", "sourceColumn": "MaxSalary"}
        ],
        "partitions": [make_csv_partition("Dim_JobRole.csv")]
    },
    {
        "name": "Dim_Date",
        "dataCategory": "Time",
        "columns": [
            {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
            {"name": "Date", "dataType": "dateTime", "isKey": True, "sourceColumn": "Date"},
            {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
            {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
            {"name": "YearQuarter", "dataType": "string", "sourceColumn": "YearQuarter"},
            {"name": "MonthNumber", "dataType": "int64", "sourceColumn": "MonthNumber"},
            {"name": "MonthName", "dataType": "string", "sortByColumn": "MonthNumber", "sourceColumn": "MonthName"},
            {"name": "MonthShort", "dataType": "string", "sortByColumn": "MonthNumber", "sourceColumn": "MonthShort"},
            {"name": "YearMonth", "dataType": "string", "sourceColumn": "YearMonth"},
            {"name": "Day", "dataType": "int64", "sourceColumn": "Day"},
            {"name": "DayOfWeek", "dataType": "string", "sourceColumn": "DayOfWeek"},
            {"name": "DayOfWeekNumber", "dataType": "int64", "sourceColumn": "DayOfWeekNumber"},
            {"name": "IsWeekend", "dataType": "int64", "sourceColumn": "IsWeekend"},
            {"name": "FiscalYear", "dataType": "string", "sourceColumn": "FiscalYear"},
            {"name": "FiscalQuarter", "dataType": "string", "sourceColumn": "FiscalQuarter"}
        ],
        "partitions": [make_csv_partition("Dim_Date.csv")]
    },
    {
        "name": "Dim_Employee",
        "columns": [
            {"name": "EmployeeID", "dataType": "string", "sourceColumn": "EmployeeID"},
            {"name": "FirstName", "dataType": "string", "sourceColumn": "FirstName"},
            {"name": "LastName", "dataType": "string", "sourceColumn": "LastName"},
            {"name": "Gender", "dataType": "string", "sourceColumn": "Gender"},
            {"name": "Age", "dataType": "int64", "sourceColumn": "Age"},
            {"name": "Generation", "dataType": "string", "sourceColumn": "Generation"},
            {"name": "Ethnicity", "dataType": "string", "sourceColumn": "Ethnicity"},
            {"name": "MaritalStatus", "dataType": "string", "sourceColumn": "MaritalStatus"},
            {"name": "EducationLevel", "dataType": "string", "sourceColumn": "EducationLevel"},
            {"name": "DepartmentID", "dataType": "int64", "sourceColumn": "DepartmentID"},
            {"name": "JobRoleID", "dataType": "int64", "sourceColumn": "JobRoleID"},
            {"name": "WorkLocation", "dataType": "string", "sourceColumn": "WorkLocation"},
            {"name": "OfficeCity", "dataType": "string", "sourceColumn": "OfficeCity"},
            {"name": "HireDate", "dataType": "dateTime", "sourceColumn": "HireDate"},
            {"name": "CurrentStatus", "dataType": "string", "sourceColumn": "CurrentStatus"},
            {"name": "ExitDate", "dataType": "dateTime", "sourceColumn": "ExitDate"},
            {"name": "ExitType", "dataType": "string", "sourceColumn": "ExitType"},
            {"name": "ExitReason", "dataType": "string", "sourceColumn": "ExitReason"},
            {"name": "CurrentBaseSalary", "dataType": "double", "sourceColumn": "CurrentBaseSalary"},
            {"name": "TenureMonths", "dataType": "double", "sourceColumn": "TenureMonths"},
            {"name": "TenureYears", "dataType": "double", "sourceColumn": "TenureYears"}
        ],
        "partitions": [make_csv_partition("Dim_Employee.csv")]
    },
    {
        "name": "Fact_Attrition",
        "columns": [
            {"name": "AttritionID", "dataType": "string", "sourceColumn": "AttritionID"},
            {"name": "EmployeeID", "dataType": "string", "sourceColumn": "EmployeeID"},
            {"name": "ExitDate", "dataType": "dateTime", "sourceColumn": "ExitDate"},
            {"name": "ExitDateKey", "dataType": "int64", "sourceColumn": "ExitDateKey"},
            {"name": "DepartmentID", "dataType": "int64", "sourceColumn": "DepartmentID"},
            {"name": "JobRoleID", "dataType": "int64", "sourceColumn": "JobRoleID"},
            {"name": "TenureMonths", "dataType": "double", "sourceColumn": "TenureMonths"},
            {"name": "TenureBand", "dataType": "string", "sourceColumn": "TenureBand"},
            {"name": "AttritionType", "dataType": "string", "sourceColumn": "AttritionType"},
            {"name": "PrimaryReason", "dataType": "string", "sourceColumn": "PrimaryReason"},
            {"name": "LastPerformanceRating", "dataType": "int64", "sourceColumn": "LastPerformanceRating"},
            {"name": "LastSatisfactionScore", "dataType": "int64", "sourceColumn": "LastSatisfactionScore"},
            {"name": "EstimatedCostOfTurnover", "dataType": "double", "sourceColumn": "EstimatedCostOfTurnover"}
        ],
        "partitions": [make_csv_partition("Fact_Attrition.csv")]
    },
    {
        "name": "Fact_Performance",
        "columns": [
            {"name": "ReviewID", "dataType": "string", "sourceColumn": "ReviewID"},
            {"name": "EmployeeID", "dataType": "string", "sourceColumn": "EmployeeID"},
            {"name": "ReviewDate", "dataType": "dateTime", "sourceColumn": "ReviewDate"},
            {"name": "ReviewDateKey", "dataType": "int64", "sourceColumn": "ReviewDateKey"},
            {"name": "ReviewYear", "dataType": "int64", "sourceColumn": "ReviewYear"},
            {"name": "PerformanceRating", "dataType": "int64", "sourceColumn": "PerformanceRating"},
            {"name": "PotentialRating", "dataType": "int64", "sourceColumn": "PotentialRating"},
            {"name": "NineBoxGrid", "dataType": "string", "sourceColumn": "NineBoxGrid"},
            {"name": "TrainingHoursCompleted", "dataType": "int64", "sourceColumn": "TrainingHoursCompleted"},
            {"name": "SatisfactionScore", "dataType": "int64", "sourceColumn": "SatisfactionScore"},
            {"name": "WorkLifeBalanceScore", "dataType": "int64", "sourceColumn": "WorkLifeBalanceScore"},
            {"name": "Promoted", "dataType": "string", "sourceColumn": "Promoted"},
            {"name": "FlightRisk", "dataType": "string", "sourceColumn": "FlightRisk"}
        ],
        "partitions": [make_csv_partition("Fact_Performance.csv")]
    },
    {
        "name": "Fact_Payroll",
        "columns": [
            {"name": "PayrollID", "dataType": "string", "sourceColumn": "PayrollID"},
            {"name": "EmployeeID", "dataType": "string", "sourceColumn": "EmployeeID"},
            {"name": "PayDate", "dataType": "dateTime", "sourceColumn": "PayDate"},
            {"name": "PayDateKey", "dataType": "int64", "sourceColumn": "PayDateKey"},
            {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
            {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
            {"name": "AnnualizedBaseSalary", "dataType": "double", "sourceColumn": "AnnualizedBaseSalary"},
            {"name": "QuarterlyBasePay", "dataType": "double", "sourceColumn": "QuarterlyBasePay"},
            {"name": "BonusPay", "dataType": "double", "sourceColumn": "BonusPay"},
            {"name": "OvertimeHours", "dataType": "int64", "sourceColumn": "OvertimeHours"},
            {"name": "OvertimePay", "dataType": "double", "sourceColumn": "OvertimePay"},
            {"name": "BenefitsCost", "dataType": "double", "sourceColumn": "BenefitsCost"},
            {"name": "TotalCompensation", "dataType": "double", "sourceColumn": "TotalCompensation"}
        ],
        "partitions": [make_csv_partition("Fact_Payroll.csv")]
    },
    {
        "name": "_DAX Measures",
        "columns": [
            {"name": "MeasureHolder", "dataType": "string", "isHidden": True, "sourceColumn": "MeasureHolder"}
        ],
        "partitions": [
            {
                "name": "Partition",
                "dataView": "full",
                "source": {
                    "type": "m",
                    "expression": [
                        'let Source = #table(type table[MeasureHolder = text], {{"Measures"}}) in Source'
                    ]
                }
            }
        ],
        "measures": [
            {
                "name": "Total Employees",
                "expression": "COUNTROWS('Dim_Employee')",
                "formatString": "#,##0",
                "displayFolder": "01 - Workforce & Headcount"
            },
            {
                "name": "Active Headcount",
                "expression": "CALCULATE(COUNTROWS('Dim_Employee'), 'Dim_Employee'[CurrentStatus] = \"Active\")",
                "formatString": "#,##0",
                "displayFolder": "01 - Workforce & Headcount"
            },
            {
                "name": "Female Representation %",
                "expression": "DIVIDE(CALCULATE([Active Headcount], 'Dim_Employee'[Gender] = \"Female\"), [Active Headcount], 0)",
                "formatString": "0.0%",
                "displayFolder": "01 - Workforce & Headcount"
            },
            {
                "name": "Average Employee Age",
                "expression": "CALCULATE(AVERAGE('Dim_Employee'[Age]), 'Dim_Employee'[CurrentStatus] = \"Active\")",
                "formatString": "0.0",
                "displayFolder": "01 - Workforce & Headcount"
            },
            {
                "name": "Total Separations",
                "expression": "COUNTROWS('Fact_Attrition')",
                "formatString": "#,##0",
                "displayFolder": "02 - Attrition & Retention"
            },
            {
                "name": "Attrition Rate %",
                "expression": "DIVIDE([Total Separations], [Total Employees], 0)",
                "formatString": "0.0%",
                "displayFolder": "02 - Attrition & Retention"
            },
            {
                "name": "Voluntary Attrition %",
                "expression": "DIVIDE(CALCULATE(COUNTROWS('Fact_Attrition'), 'Fact_Attrition'[AttritionType] = \"Voluntary\"), [Total Separations], 0)",
                "formatString": "0.0%",
                "displayFolder": "02 - Attrition & Retention"
            },
            {
                "name": "Total Cost of Turnover",
                "expression": "SUM('Fact_Attrition'[EstimatedCostOfTurnover])",
                "formatString": "$#,##0",
                "displayFolder": "02 - Attrition & Retention"
            },
            {
                "name": "Total Payroll Cost",
                "expression": "SUM('Fact_Payroll'[TotalCompensation])",
                "formatString": "$#,##0",
                "displayFolder": "03 - Compensation & Payroll"
            },
            {
                "name": "Average Annual Base Salary",
                "expression": "CALCULATE(AVERAGE('Dim_Employee'[CurrentBaseSalary]), 'Dim_Employee'[CurrentStatus] = \"Active\")",
                "formatString": "$#,##0",
                "displayFolder": "03 - Compensation & Payroll"
            },
            {
                "name": "Median Annual Base Salary",
                "expression": "CALCULATE(MEDIAN('Dim_Employee'[CurrentBaseSalary]), 'Dim_Employee'[CurrentStatus] = \"Active\")",
                "formatString": "$#,##0",
                "displayFolder": "03 - Compensation & Payroll"
            },
            {
                "name": "Gender Pay Equity Ratio",
                "expression": "DIVIDE(CALCULATE([Average Annual Base Salary], 'Dim_Employee'[Gender] = \"Female\"), CALCULATE([Average Annual Base Salary], 'Dim_Employee'[Gender] = \"Male\"), 1.0)",
                "formatString": "0.00",
                "displayFolder": "03 - Compensation & Payroll"
            },
            {
                "name": "Average Performance Rating",
                "expression": "AVERAGE('Fact_Performance'[PerformanceRating])",
                "formatString": "0.00",
                "displayFolder": "04 - Performance & Talent Matrix"
            },
            {
                "name": "High Performer %",
                "expression": "DIVIDE(CALCULATE(COUNTROWS('Fact_Performance'), 'Fact_Performance'[PerformanceRating] >= 4), COUNTROWS('Fact_Performance'), 0)",
                "formatString": "0.0%",
                "displayFolder": "04 - Performance & Talent Matrix"
            },
            {
                "name": "Promotion Rate %",
                "expression": "DIVIDE(CALCULATE(COUNTROWS('Fact_Performance'), 'Fact_Performance'[Promoted] = \"Yes\"), COUNTROWS('Fact_Performance'), 0)",
                "formatString": "0.0%",
                "displayFolder": "04 - Performance & Talent Matrix"
            },
            {
                "name": "Average Satisfaction Score",
                "expression": "AVERAGE('Fact_Performance'[SatisfactionScore])",
                "formatString": "0.00",
                "displayFolder": "04 - Performance & Talent Matrix"
            }
        ]
    }
]

# Build relationships
relationships = [
    {
        "name": "Rel_Dept_JobRole",
        "fromTable": "Dim_JobRole",
        "fromColumn": "DepartmentID",
        "toTable": "Dim_Department",
        "toColumn": "DepartmentID"
    },
    {
        "name": "Rel_Dept_Employee",
        "fromTable": "Dim_Employee",
        "fromColumn": "DepartmentID",
        "toTable": "Dim_Department",
        "toColumn": "DepartmentID"
    },
    {
        "name": "Rel_JobRole_Employee",
        "fromTable": "Dim_Employee",
        "fromColumn": "JobRoleID",
        "toTable": "Dim_JobRole",
        "toColumn": "JobRoleID"
    },
    {
        "name": "Rel_Employee_Payroll",
        "fromTable": "Fact_Payroll",
        "fromColumn": "EmployeeID",
        "toTable": "Dim_Employee",
        "toColumn": "EmployeeID"
    },
    {
        "name": "Rel_Employee_Performance",
        "fromTable": "Fact_Performance",
        "fromColumn": "EmployeeID",
        "toTable": "Dim_Employee",
        "toColumn": "EmployeeID"
    },
    {
        "name": "Rel_Employee_Attrition",
        "fromTable": "Fact_Attrition",
        "fromColumn": "EmployeeID",
        "toTable": "Dim_Employee",
        "toColumn": "EmployeeID"
    },
    {
        "name": "Rel_Date_Payroll",
        "fromTable": "Fact_Payroll",
        "fromColumn": "PayDate",
        "toTable": "Dim_Date",
        "toColumn": "Date"
    },
    {
        "name": "Rel_Date_Performance",
        "fromTable": "Fact_Performance",
        "fromColumn": "ReviewDate",
        "toTable": "Dim_Date",
        "toColumn": "Date"
    },
    {
        "name": "Rel_Date_Attrition",
        "fromTable": "Fact_Attrition",
        "fromColumn": "ExitDate",
        "toTable": "Dim_Date",
        "toColumn": "Date"
    },
    {
        "name": "Rel_Date_Employee_HireDate",
        "fromTable": "Dim_Employee",
        "fromColumn": "HireDate",
        "toTable": "Dim_Date",
        "toColumn": "Date",
        "isActive": False
    },
    {
        "name": "Rel_Date_Employee_ExitDate",
        "fromTable": "Dim_Employee",
        "fromColumn": "ExitDate",
        "toTable": "Dim_Date",
        "toColumn": "Date",
        "isActive": False
    }
]

model_bim = {
    "name": "HR_Analytics_SemanticModel",
    "compatibilityLevel": 1550,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "fastCombine": False
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "tables": tables,
        "relationships": relationships
    }
}

with open(os.path.join(MODEL_DIR, "model.bim"), "w", encoding="utf-8") as f:
    json.dump(model_bim, f, indent=2)

print("PBIP Project Structure and model.bim generated successfully!")

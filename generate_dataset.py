import os
import csv
import random
import datetime

# Seed for reproducibility
random.seed(42)

OUT_DIR = r"C:\Users\Himabala\.gemini\antigravity-ide\scratch\hr_analytics_powerbi\data"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Dim_Department
departments = [
    {"DepartmentID": 1, "DepartmentName": "Engineering", "Division": "Technology", "CostCenter": "CC-ENG-100", "DepartmentHead": "Dr. Sarah Chen"},
    {"DepartmentID": 2, "DepartmentName": "Sales", "Division": "Commercial", "CostCenter": "CC-SLS-200", "DepartmentHead": "Marcus Vance"},
    {"DepartmentID": 3, "DepartmentName": "Marketing", "Division": "Commercial", "CostCenter": "CC-MKT-300", "DepartmentHead": "Elena Rostova"},
    {"DepartmentID": 4, "DepartmentName": "Human Resources", "Division": "Corporate Services", "CostCenter": "CC-HR-400", "DepartmentHead": "Patricia Gomez"},
    {"DepartmentID": 5, "DepartmentName": "Finance & Accounting", "Division": "Corporate Services", "CostCenter": "CC-FIN-500", "DepartmentHead": "David Kim"},
    {"DepartmentID": 6, "DepartmentName": "Product & Design", "Division": "Technology", "CostCenter": "CC-PRD-600", "DepartmentHead": "Amina Al-Mansoor"},
    {"DepartmentID": 7, "DepartmentName": "Customer Support", "Division": "Operations", "CostCenter": "CC-SUP-700", "DepartmentHead": "Brian O'Connor"},
]

with open(os.path.join(OUT_DIR, "Dim_Department.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(departments[0].keys()))
    writer.writeheader()
    writer.writerows(departments)

# 2. Dim_JobRole
job_roles = [
    # Engineering
    {"JobRoleID": 101, "DepartmentID": 1, "JobTitle": "Junior Software Engineer", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 68000, "MaxSalary": 85000},
    {"JobRoleID": 102, "DepartmentID": 1, "JobTitle": "Software Engineer", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 90000, "MaxSalary": 120000},
    {"JobRoleID": 103, "DepartmentID": 1, "JobTitle": "Senior Software Engineer", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 130000, "MaxSalary": 165000},
    {"JobRoleID": 104, "DepartmentID": 1, "JobTitle": "Staff Software Architect", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 170000, "MaxSalary": 210000},
    {"JobRoleID": 105, "DepartmentID": 1, "JobTitle": "Engineering Director", "JobLevel": "Executive", "PayGrade": "Grade 5", "MinSalary": 220000, "MaxSalary": 280000},
    # Sales
    {"JobRoleID": 201, "DepartmentID": 2, "JobTitle": "Sales Development Rep", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 52000, "MaxSalary": 68000},
    {"JobRoleID": 202, "DepartmentID": 2, "JobTitle": "Account Executive", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 75000, "MaxSalary": 105000},
    {"JobRoleID": 203, "DepartmentID": 2, "JobTitle": "Senior Enterprise AE", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 115000, "MaxSalary": 150000},
    {"JobRoleID": 204, "DepartmentID": 2, "JobTitle": "Regional Sales Manager", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 155000, "MaxSalary": 195000},
    {"JobRoleID": 205, "DepartmentID": 2, "JobTitle": "VP of Commercial Sales", "JobLevel": "Executive", "PayGrade": "Grade 5", "MinSalary": 210000, "MaxSalary": 270000},
    # Marketing
    {"JobRoleID": 301, "DepartmentID": 3, "JobTitle": "Marketing Coordinator", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 50000, "MaxSalary": 65000},
    {"JobRoleID": 302, "DepartmentID": 3, "JobTitle": "Content Marketing Specialist", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 70000, "MaxSalary": 92000},
    {"JobRoleID": 303, "DepartmentID": 3, "JobTitle": "Growth Marketing Manager", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 105000, "MaxSalary": 138000},
    {"JobRoleID": 304, "DepartmentID": 3, "JobTitle": "Director of Demand Gen", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 150000, "MaxSalary": 190000},
    # Human Resources
    {"JobRoleID": 401, "DepartmentID": 4, "JobTitle": "HR Coordinator", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 52000, "MaxSalary": 66000},
    {"JobRoleID": 402, "DepartmentID": 4, "JobTitle": "People Operations Specialist", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 72000, "MaxSalary": 95000},
    {"JobRoleID": 403, "DepartmentID": 4, "JobTitle": "Senior Talent Acquisition Partner", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 100000, "MaxSalary": 135000},
    {"JobRoleID": 404, "DepartmentID": 4, "JobTitle": "Head of People & Culture", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 155000, "MaxSalary": 195000},
    # Finance
    {"JobRoleID": 501, "DepartmentID": 5, "JobTitle": "Junior Accountant", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 55000, "MaxSalary": 70000},
    {"JobRoleID": 502, "DepartmentID": 5, "JobTitle": "Financial Analyst", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 80000, "MaxSalary": 105000},
    {"JobRoleID": 503, "DepartmentID": 5, "JobTitle": "Senior FP&A Manager", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 125000, "MaxSalary": 160000},
    {"JobRoleID": 504, "DepartmentID": 5, "JobTitle": "VP of Finance & Controller", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 180000, "MaxSalary": 230000},
    # Product & Design
    {"JobRoleID": 601, "DepartmentID": 6, "JobTitle": "Associate Product Designer", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 62000, "MaxSalary": 78000},
    {"JobRoleID": 602, "DepartmentID": 6, "JobTitle": "Product Manager", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 95000, "MaxSalary": 128000},
    {"JobRoleID": 603, "DepartmentID": 6, "JobTitle": "Lead Product Designer", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 130000, "MaxSalary": 165000},
    {"JobRoleID": 604, "DepartmentID": 6, "JobTitle": "Group Product Manager", "JobLevel": "Lead/Manager", "PayGrade": "Grade 4", "MinSalary": 170000, "MaxSalary": 215000},
    # Support
    {"JobRoleID": 701, "DepartmentID": 7, "JobTitle": "Customer Success Associate", "JobLevel": "Entry", "PayGrade": "Grade 1", "MinSalary": 48000, "MaxSalary": 62000},
    {"JobRoleID": 702, "DepartmentID": 7, "JobTitle": "Tier 2 Technical Support Specialist", "JobLevel": "Mid", "PayGrade": "Grade 2", "MinSalary": 65000, "MaxSalary": 82000},
    {"JobRoleID": 703, "DepartmentID": 7, "JobTitle": "Customer Support Lead", "JobLevel": "Senior", "PayGrade": "Grade 3", "MinSalary": 88000, "MaxSalary": 115000},
]

with open(os.path.join(OUT_DIR, "Dim_JobRole.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(job_roles[0].keys()))
    writer.writeheader()
    writer.writerows(job_roles)

# 3. Dim_Date (2020-01-01 to 2026-12-31)
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2026, 12, 31)
curr = start_date

date_rows = []
while curr <= end_date:
    q = (curr.month - 1) // 3 + 1
    fy = curr.year if curr.month < 10 else curr.year + 1
    fq = ((curr.month + 2) % 12) // 3 + 1
    date_rows.append({
        "DateKey": int(curr.strftime("%Y%m%d")),
        "Date": curr.strftime("%Y-%m-%d"),
        "Year": curr.year,
        "Quarter": f"Q{q}",
        "YearQuarter": f"{curr.year}-Q{q}",
        "MonthNumber": curr.month,
        "MonthName": curr.strftime("%B"),
        "MonthShort": curr.strftime("%b"),
        "YearMonth": curr.strftime("%Y-%m"),
        "Day": curr.day,
        "DayOfWeek": curr.strftime("%A"),
        "DayOfWeekNumber": curr.isoweekday(),
        "IsWeekend": 1 if curr.isoweekday() in [6, 7] else 0,
        "FiscalYear": f"FY{fy}",
        "FiscalQuarter": f"FQ{fq}"
    })
    curr += datetime.timedelta(days=1)

with open(os.path.join(OUT_DIR, "Dim_Date.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(date_rows[0].keys()))
    writer.writeheader()
    writer.writerows(date_rows)

# 4. Generate Dim_Employee (~1,250 employees)
first_names_male = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Charles", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Frank", "Raymond", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Douglas", "Zachary", "Peter", "Kyle", "Noah", "Ethan", "Jeremy", "Christian", "Walter", "Keith", "Austin", "Roger", "Terry", "Sean", "Gerald", "Carl", "Dylan", "Harold", "Jordan", "Jesse", "Bryan", "Lawrence", "Arthur", "Gabriel", "Bruce", "Logan", "Billy", "Joe", "Alan", "Juan", "Elijah", "Willie", "Albert", "Wayne", "Randy", "Mason", "Vincent", "Liam", "Roy", "Bobby", "Caleb", "Bradley", "Russell", "Lucas", "Eugene"]
first_names_female = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda", "Dorothy", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra", "Rachel", "Carolyn", "Janet", "Maria", "Catherine", "Heather", "Diane", "Olivia", "Julie", "Joyce", "Victoria", "Ruth", "Virginia", "Lauren", "Kelly", "Christina", "Joan", "Evelyn", "Judith", "Andrea", "Hannah", "Megan", "Cheryl", "Jacqueline", "Martha", "Madison", "Teresa", "Gloria", "Sara", "Janice", "Ann", "Kathryn", "Abigail", "Sophia", "Frances", "Jean", "Alice", "Judy", "Isabella", "Julia", "Grace", "Amber", "Denise", "Danielle", "Marilyn", "Beverly", "Charlotte", "Natalie", "Theresa", "Diana", "Brittany", "Doris", "Kayla", "Alexis", "Lori", "Marie"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Mendoza", "Gray", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman"]

ethnicities = ["White", "Asian", "Hispanic/Latino", "Black/African American", "Two or More Races"]
ethnicity_weights = [0.45, 0.22, 0.16, 0.12, 0.05]

education_levels = ["Bachelor's", "Master's", "Doctorate", "Associate's", "High School Diploma"]
edu_weights = [0.55, 0.30, 0.05, 0.08, 0.02]

cities = ["New York, NY", "San Francisco, CA", "Austin, TX", "Chicago, IL", "London, UK", "Seattle, WA"]
city_weights = [0.28, 0.25, 0.18, 0.14, 0.08, 0.07]

work_models = ["Hybrid", "Remote", "On-site"]
work_weights = [0.55, 0.30, 0.15]

exit_reasons_voluntary = [
    "Better Compensation & Benefits",
    "Career Advancement / Growth",
    "Relocation / Personal Reasons",
    "Work-Life Balance / Burnout",
    "Company Culture / Leadership",
    "Pursuing Higher Education"
]
exit_reasons_involuntary = [
    "Performance Standards Not Met",
    "Organizational Restructuring / Layoff",
    "Violation of Company Policy"
]

roles_by_dept = {}
for r in job_roles:
    roles_by_dept.setdefault(r["DepartmentID"], []).append(r)

employees = []
payroll_records = []
performance_reviews = []
attrition_records = []

payroll_id_seq = 1
review_id_seq = 1
attrition_id_seq = 1

TOTAL_EMPLOYEES = 1250

for emp_i in range(1, TOTAL_EMPLOYEES + 1):
    emp_id = f"EMP-{1000 + emp_i}"
    
    g_rnd = random.random()
    if g_rnd < 0.48:
        gender = "Female"
        first_name = random.choice(first_names_female)
    elif g_rnd < 0.96:
        gender = "Male"
        first_name = random.choice(first_names_male)
    else:
        gender = "Non-Binary"
        first_name = random.choice(first_names_female if random.random() < 0.5 else first_names_male)
        
    last_name = random.choice(last_names)
    
    dept_weights = [0.28, 0.24, 0.12, 0.08, 0.08, 0.10, 0.10]
    dept = random.choices(departments, weights=dept_weights)[0]
    dept_id = dept["DepartmentID"]
    
    role_choices = roles_by_dept[dept_id]
    level_weights = [0.35, 0.35, 0.20, 0.08] if len(role_choices) == 4 else [0.35, 0.30, 0.20, 0.10, 0.05]
    role = random.choices(role_choices, weights=level_weights[:len(role_choices)])[0]
    role_id = role["JobRoleID"]
    
    if role["JobLevel"] == "Entry":
        age = random.randint(22, 29)
    elif role["JobLevel"] == "Mid":
        age = random.randint(26, 40)
    elif role["JobLevel"] == "Senior":
        age = random.randint(31, 52)
    else:
        age = random.randint(38, 62)
        
    if age <= 28:
        generation = "Gen Z (1997-2012)"
    elif age <= 43:
        generation = "Millennials (1981-1996)"
    elif age <= 59:
        generation = "Gen X (1965-1980)"
    else:
        generation = "Boomers (1946-1964)"
        
    ethnicity = random.choices(ethnicities, weights=ethnicity_weights)[0]
    education = random.choices(education_levels, weights=edu_weights)[0]
    location = random.choices(cities, weights=city_weights)[0]
    work_model = random.choices(work_models, weights=work_weights)[0]
    marital_status = random.choice(["Single", "Married", "Divorced"]) if age > 25 else random.choices(["Single", "Married"], weights=[0.8, 0.2])[0]
    
    hire_year = random.choices([2020, 2021, 2022, 2023, 2024, 2025, 2026], weights=[0.12, 0.15, 0.18, 0.20, 0.18, 0.12, 0.05])[0]
    hire_month = random.randint(1, 12 if hire_year < 2026 else 4)
    hire_day = random.randint(1, 28)
    hire_date = datetime.date(hire_year, hire_month, hire_day)
    
    salary_range = role["MaxSalary"] - role["MinSalary"]
    ratio = random.betavariate(2.2, 2.0)
    base_salary = int(round(role["MinSalary"] + ratio * salary_range, -2))
    
    base_attrition_chance = 0.17
    if dept["DepartmentName"] in ["Customer Support", "Sales"]:
        base_attrition_chance = 0.24
    elif dept["DepartmentName"] in ["Engineering", "Finance & Accounting"]:
        base_attrition_chance = 0.12
    if role["JobLevel"] == "Executive":
        base_attrition_chance = 0.06
        
    is_terminated = random.random() < base_attrition_chance
    
    if is_terminated:
        min_tenure_days = random.randint(90, 1100)
        exit_date = hire_date + datetime.timedelta(days=min_tenure_days)
        if exit_date > datetime.date(2026, 10, 15):
            if random.random() < 0.6:
                exit_date = datetime.date(2026, random.randint(1, 9), random.randint(1, 28))
                if exit_date <= hire_date:
                    is_terminated = False
            else:
                is_terminated = False
                
    if is_terminated:
        current_status = "Terminated"
        if age >= 60 and random.random() < 0.4:
            exit_type = "Retirement"
            exit_reason = "Retirement"
        elif random.random() < 0.82:
            exit_type = "Voluntary"
            exit_reason = random.choice(exit_reasons_voluntary)
        else:
            exit_type = "Involuntary"
            exit_reason = random.choice(exit_reasons_involuntary)
        exit_date_str = exit_date.strftime("%Y-%m-%d")
        tenure_days = (exit_date - hire_date).days
        tenure_months = round(tenure_days / 30.4375, 1)
        tenure_years = round(tenure_days / 365.25, 2)
    else:
        current_status = "Active"
        exit_type = ""
        exit_reason = ""
        exit_date_str = ""
        tenure_days = (datetime.date(2026, 10, 29) - hire_date).days
        tenure_months = round(tenure_days / 30.4375, 1)
        tenure_years = round(tenure_days / 365.25, 2)
        
    employees.append({
        "EmployeeID": emp_id,
        "FirstName": first_name,
        "LastName": last_name,
        "Gender": gender,
        "Age": age,
        "Generation": generation,
        "Ethnicity": ethnicity,
        "MaritalStatus": marital_status,
        "EducationLevel": education,
        "DepartmentID": dept_id,
        "JobRoleID": role_id,
        "WorkLocation": work_model,
        "OfficeCity": location,
        "HireDate": hire_date.strftime("%Y-%m-%d"),
        "CurrentStatus": current_status,
        "ExitDate": exit_date_str,
        "ExitType": exit_type,
        "ExitReason": exit_reason,
        "CurrentBaseSalary": base_salary,
        "TenureMonths": tenure_months,
        "TenureYears": tenure_years
    })
    
    if is_terminated:
        if tenure_months < 6:
            tenure_band = "< 6 Months"
        elif tenure_months <= 12:
            tenure_band = "6-12 Months"
        elif tenure_months <= 24:
            tenure_band = "1-2 Years"
        elif tenure_months <= 48:
            tenure_band = "2-4 Years"
        else:
            tenure_band = "4+ Years"
            
        last_sat = random.choices([1, 2, 3, 4, 5], weights=[0.40, 0.30, 0.18, 0.08, 0.04])[0]
        last_perf = random.choices([1, 2, 3, 4, 5], weights=[0.20, 0.25, 0.35, 0.15, 0.05])[0]
        cost_of_turnover = round(base_salary * random.uniform(0.6, 1.2), 0)
        
        attrition_records.append({
            "AttritionID": f"ATT-{attrition_id_seq:04d}",
            "EmployeeID": emp_id,
            "ExitDate": exit_date_str,
            "ExitDateKey": int(exit_date.strftime("%Y%m%d")),
            "DepartmentID": dept_id,
            "JobRoleID": role_id,
            "TenureMonths": tenure_months,
            "TenureBand": tenure_band,
            "AttritionType": exit_type,
            "PrimaryReason": exit_reason,
            "LastPerformanceRating": last_perf,
            "LastSatisfactionScore": last_sat,
            "EstimatedCostOfTurnover": int(cost_of_turnover)
        })
        attrition_id_seq += 1

    review_years = [y for y in [2021, 2022, 2023, 2024, 2025] if y >= hire_year]
    for r_year in review_years:
        rev_date = datetime.date(r_year, 12, 15)
        if is_terminated and exit_date < rev_date:
            continue
            
        perf_rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.15, 0.52, 0.21, 0.07])[0]
        potential_rating = random.choices([1, 2, 3], weights=[0.25, 0.55, 0.20])[0]
        
        training_hrs = random.randint(10, 65)
        sat_score = random.choices([1, 2, 3, 4, 5], weights=[0.06, 0.14, 0.32, 0.33, 0.15])[0]
        wlb_score = random.choices([1, 2, 3, 4, 5], weights=[0.08, 0.16, 0.35, 0.28, 0.13])[0]
        
        if sat_score <= 2 or wlb_score <= 2:
            flight_risk = random.choices(["High", "Medium", "Low"], weights=[0.60, 0.30, 0.10])[0]
        elif perf_rating >= 4:
            flight_risk = random.choices(["High", "Medium", "Low"], weights=[0.25, 0.45, 0.30])[0]
        else:
            flight_risk = "Low"
            
        promoted = "Yes" if perf_rating >= 4 and potential_rating >= 2 and random.random() < 0.35 else "No"
        
        performance_reviews.append({
            "ReviewID": f"REV-{review_id_seq:05d}",
            "EmployeeID": emp_id,
            "ReviewDate": rev_date.strftime("%Y-%m-%d"),
            "ReviewDateKey": int(rev_date.strftime("%Y%m%d")),
            "ReviewYear": r_year,
            "PerformanceRating": perf_rating,
            "PotentialRating": potential_rating,
            "NineBoxGrid": f"P{perf_rating}-Pot{potential_rating}",
            "TrainingHoursCompleted": training_hrs,
            "SatisfactionScore": sat_score,
            "WorkLifeBalanceScore": wlb_score,
            "Promoted": promoted,
            "FlightRisk": flight_risk
        })
        review_id_seq += 1

    payroll_quarters = [
        datetime.date(2023, 3, 31), datetime.date(2023, 6, 30), datetime.date(2023, 9, 30), datetime.date(2023, 12, 31),
        datetime.date(2024, 3, 31), datetime.date(2024, 6, 30), datetime.date(2024, 9, 30), datetime.date(2024, 12, 31),
        datetime.date(2025, 3, 31), datetime.date(2025, 6, 30), datetime.date(2025, 9, 30), datetime.date(2025, 12, 31),
        datetime.date(2026, 3, 31), datetime.date(2026, 6, 30), datetime.date(2026, 9, 30)
    ]
    
    salary_tracker = base_salary
    for pq in payroll_quarters:
        if hire_date > pq:
            continue
        if is_terminated and exit_date < pq:
            continue
            
        if pq.month == 3 and pq.year > hire_year:
            merit_pct = random.uniform(0.025, 0.065)
            salary_tracker = int(round(salary_tracker * (1 + merit_pct), -2))
            
        quarterly_base = round(salary_tracker / 4.0, 2)
        if pq.month == 12:
            bonus = round(quarterly_base * random.uniform(0.08, 0.25), 2)
        else:
            bonus = round(quarterly_base * random.uniform(0.0, 0.05), 2)
            
        if role["JobLevel"] in ["Entry", "Mid"] and dept["DepartmentName"] in ["Customer Support", "Engineering"]:
            ot_hours = random.randint(0, 35)
            ot_rate = (salary_tracker / 2080.0) * 1.5
            ot_pay = round(ot_hours * ot_rate, 2)
        else:
            ot_hours = 0
            ot_pay = 0.0
            
        benefits = round(quarterly_base * 0.18, 2)
        total_comp = round(quarterly_base + bonus + ot_pay + benefits, 2)
        
        payroll_records.append({
            "PayrollID": f"PAY-{payroll_id_seq:06d}",
            "EmployeeID": emp_id,
            "PayDate": pq.strftime("%Y-%m-%d"),
            "PayDateKey": int(pq.strftime("%Y%m%d")),
            "Year": pq.year,
            "Quarter": f"Q{(pq.month - 1) // 3 + 1}",
            "AnnualizedBaseSalary": salary_tracker,
            "QuarterlyBasePay": quarterly_base,
            "BonusPay": bonus,
            "OvertimeHours": ot_hours,
            "OvertimePay": ot_pay,
            "BenefitsCost": benefits,
            "TotalCompensation": total_comp
        })
        payroll_id_seq += 1

with open(os.path.join(OUT_DIR, "Dim_Employee.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(employees[0].keys()))
    writer.writeheader()
    writer.writerows(employees)

with open(os.path.join(OUT_DIR, "Fact_Attrition.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(attrition_records[0].keys()))
    writer.writeheader()
    writer.writerows(attrition_records)

with open(os.path.join(OUT_DIR, "Fact_Performance.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(performance_reviews[0].keys()))
    writer.writeheader()
    writer.writerows(performance_reviews)

with open(os.path.join(OUT_DIR, "Fact_Payroll.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(payroll_records[0].keys()))
    writer.writeheader()
    writer.writerows(payroll_records)

print("Data Generation Completed Successfully:")
print(f" - Dim_Department: {len(departments)} rows")
print(f" - Dim_JobRole: {len(job_roles)} rows")
print(f" - Dim_Date: {len(date_rows)} rows")
print(f" - Dim_Employee: {len(employees)} rows")
print(f" - Fact_Attrition: {len(attrition_records)} rows")
print(f" - Fact_Performance: {len(performance_reviews)} rows")
print(f" - Fact_Payroll: {len(payroll_records)} rows")

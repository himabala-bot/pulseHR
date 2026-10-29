# Power BI Report Design Specifications & Visual Layout Blueprint

This blueprint outlines the visual layout, chart types, data fields, color theme, and user interaction design for the 4-page **Enterprise HR & People Analytics Solution**.

---

## Global Design System & Palette

- **Theme Style**: Modern Executive Glassmorphic / Clean Professional
- **Primary Navy**: `#0F172A` (Header, Text, Dark Elements)
- **Primary Blue Accent**: `#2563EB` (Primary trends, bars, selections)
- **Vibrant Teal Accent**: `#0D9488` (Active metrics, positive growth)
- **Warning Coral/Rose**: `#F43F5E` (Attrition, risks, negative variance)
- **Purple Accent**: `#8B5CF6` (Potential & talent indicators)
- **Neutral Background**: `#F8FAFC` (Canvas background)
- **Card Background**: `#FFFFFF` with soft drop-shadow (`rgba(0, 0, 0, 0.05)`) and subtle border (`#E2E8F0`)
- **Typography**: Segoe UI / Inter, 10pt (Visual labels), 12pt (Headers), 24pt bold (KPI values)

---

## Global Filter Header (Consistent Across All Pages)
Located horizontally across the top (`Y: 10px`, `Height: 65px`):
1. **Department Slicer**: Dropdown multi-select (`Dim_Department[DepartmentName]`)
2. **Job Level Slicer**: Tile / Pill buttons (`Dim_JobRole[JobLevel]`)
3. **Gender Slicer**: Dropdown (`Dim_Employee[Gender]`)
4. **Work Location**: Dropdown (`Dim_Employee[WorkLocation]`: Remote, Hybrid, On-site)
5. **Year Slicer**: Dropdown / Single-select slider (`Dim_Date[Year]`)
6. **Reset Filters Button**: Power BI bookmark action to clear all slicers

---

## PAGE 1: Executive Workforce & Headcount Overview

### Top KPI Banner (4 Cards across `Width: 100%`)
1. **Active Headcount Card**:
   - Value: `[Active Headcount]` (e.g., `1,046`)
   - Subtext: `+38 MoM (+3.8%)` vs prior period
   - Trend Sparkline: 12-month rolling headcount
2. **Attrition Rate Card**:
   - Value: `[Attrition Rate %]` (e.g., `16.3%`)
   - Subtext: Target `< 15.0%` (Conditional formatting: Red if > 15%, Green if <= 15%)
3. **Total Annual Payroll Cost**:
   - Value: `[Total Payroll Cost]` (e.g., `$112.4M`)
   - Subtext: `+5.2% YoY`
4. **Employee Engagement / Satisfaction**:
   - Value: `[Average Satisfaction Score]` (e.g., `3.42 / 5.00`)
   - Subtext: Rating scale from annual employee surveys

### Main Visual Layout
- **Visual 1: Headcount by Department & Gender (100% Stacked Bar Chart)**
  - *Position*: Top Left (`Width: 50%`)
  - *Y-Axis*: `Dim_Department[DepartmentName]`
  - *X-Axis*: `[Active Headcount]`
  - *Legend*: `Dim_Employee[Gender]` (Colors: Teal `#0D9488` for Female, Indigo `#4338CA` for Male, Orange `#F97316` for Non-Binary)
  - *Tooltip*: Headcount, `[Female Representation %]`
- **Visual 2: Headcount Growth Trend & New Hires (Area & Clustered Column Chart)**
  - *Position*: Top Right (`Width: 50%`)
  - *X-Axis*: `Dim_Date[YearQuarter]`
  - *Column Y-Axis*: `[New Hires]`
  - *Line Y-Axis*: `[Active Headcount]`
- **Visual 3: Age & Generation Distribution (Donut Chart)**
  - *Position*: Bottom Left (`Width: 33%`)
  - *Legend*: `Dim_Employee[Generation]` (Gen Z, Millennials, Gen X, Boomers)
  - *Values*: `[Active Headcount]`
- **Visual 4: Office City & Work Location Spread (Treemap)**
  - *Position*: Bottom Center (`Width: 33%`)
  - *Category*: `Dim_Employee[OfficeCity]`
  - *Sub-category*: `Dim_Employee[WorkLocation]`
  - *Values*: `[Active Headcount]`
- **Visual 5: Education Level by Department (Matrix)**
  - *Position*: Bottom Right (`Width: 34%`)
  - *Rows*: `Dim_Department[DepartmentName]`
  - *Columns*: `Dim_Employee[EducationLevel]`
  - *Values*: `[Active Headcount]` with background color data bars

---

## PAGE 2: Attrition & Retention Deep Dive

### Top KPI Banner
1. **Total Separations**: `[Total Separations]` (e.g., `204`)
2. **Voluntary Attrition %**: `[Voluntary Attrition %]` (e.g., `78.4%`)
3. **Early Attrition Rate (< 1 Year)**: `[Early Attrition Rate %]` (e.g., `24.1%`)
4. **Estimated Cost of Turnover**: `[Total Cost of Turnover]` (e.g., `$18.6M`)

### Main Visual Layout
- **Visual 1: Primary Reasons for Separation (Horizontal Bar Chart)**
  - *Y-Axis*: `Fact_Attrition[PrimaryReason]`
  - *X-Axis*: `[Total Separations]`
  - *Color*: Coral `#F43F5E`
  - *Data Labels*: On with percentage of total
- **Visual 2: Attrition Rate by Department vs Company Benchmark (Clustered Column Chart)**
  - *X-Axis*: `Dim_Department[DepartmentName]`
  - *Y-Axis*: `[Attrition Rate %]`
  - *Constant Line*: Company benchmark target `15.0%`
- **Visual 3: Attrition by Tenure Band & Job Level (Heatmap / Matrix)**
  - *Rows*: `Fact_Attrition[TenureBand]` (`< 6 Months`, `6-12 Months`, `1-2 Years`, `2-4 Years`, `4+ Years`)
  - *Columns*: `Dim_JobRole[JobLevel]`
  - *Values*: `[Total Separations]` with conditional gradient background (Low: Light Pink, High: Dark Crimson)
- **Visual 4: Satisfaction Prior to Exit vs Tenure (Scatter Plot)**
  - *X-Axis*: `Fact_Attrition[TenureMonths]`
  - *Y-Axis*: `Fact_Attrition[LastSatisfactionScore]`
  - *Size*: `Fact_Attrition[EstimatedCostOfTurnover]`
  - *Details*: `Fact_Attrition[EmployeeID]`

---

## PAGE 3: Compensation, Payroll & Pay Equity

### Top KPI Banner
1. **Average Annual Base Salary**: `[Average Annual Base Salary]` (e.g., `$108,450`)
2. **Median Annual Base Salary**: `[Median Annual Base Salary]` (e.g., `$102,000`)
3. **Gender Pay Equity Ratio**: `[Gender Pay Equity Ratio]` (e.g., `0.98` / 1.00)
4. **Total Overtime Paid**: `[Total Overtime Paid]` (with `[Overtime Cost Ratio %]`)

### Main Visual Layout
- **Visual 1: Salary Distribution by Job Level & Gender (Clustered Bar Chart)**
  - *Y-Axis*: `Dim_JobRole[JobLevel]` (Sorted Entry to Executive)
  - *X-Axis*: `[Female Average Salary]` and `[Male Average Salary]`
  - *Legend*: Gender
- **Visual 2: Total Compensation Breakdown over Time (Stacked Area Chart)**
  - *X-Axis*: `Dim_Date[YearQuarter]`
  - *Values*: `[Total Base Salary Paid]`, `[Total Bonus Paid]`, `[Total Overtime Paid]`
- **Visual 3: Salary vs Performance Rating (Scatter Plot)**
  - *X-Axis*: `Fact_Performance[PerformanceRating]` (1 to 5)
  - *Y-Axis*: `Dim_Employee[CurrentBaseSalary]`
  - *Legend*: `Dim_Department[DepartmentName]`
  - *Trend Line*: Linear regression line to audit pay-for-performance fairness
- **Visual 4: Overtime Hours & Cost by Department (Decomposition Tree or Table)**
  - Breakdown by Division -> Department -> Job Title

---

## PAGE 4: Talent Development & 9-Box Performance Grid

### Top KPI Banner
1. **Average Performance Rating**: `[Average Performance Rating]` (e.g., `3.32 / 5.00`)
2. **High Performers %**: `[High Performer %]` (Rating 4-5)
3. **Promotion Rate %**: `[Promotion Rate %]`
4. **High Flight Risk Count**: `[High Flight Risk Count]` (Employees needing retention action)

### Main Visual Layout
- **Visual 1: The 9-Box Grid Matrix (Custom Visual / Matrix)**
  - *Rows*: `Fact_Performance[PotentialRating]` (High = 3, Medium = 2, Low = 1)
  - *Columns*: `Fact_Performance[PerformanceRating]` (1-2 = Needs Attention, 3 = Core, 4-5 = Star)
  - *Values*: Count of Employees
  - *Quadrants Color Coding*:
    - Top-Right (High Perf + High Pot): **"Future Leaders / Stars"** (Emerald Green `#10B981`)
    - Center (Mid Perf + Mid Pot): **"Core Contributors"** (Sky Blue `#0EA5E9`)
    - Bottom-Left (Low Perf + Low Pot): **"Risk / Underperformers"** (Rose Red `#F43F5E`)
- **Visual 2: Training Hours Completed vs Performance Rating (Clustered Column Chart)**
  - *X-Axis*: `Fact_Performance[PerformanceLabel]`
  - *Y-Axis*: `[Avg Training Hours Per Employee]`
- **Visual 3: Flight Risk by Department & Performance Level (Stacked Column Chart)**
  - *X-Axis*: `Dim_Department[DepartmentName]`
  - *Y-Axis*: Count of Employees
  - *Legend*: `Fact_Performance[FlightRisk]` (High, Medium, Low)
- **Visual 4: Detailed Employee Talent Drill-Through (Interactive Table)**
  - *Columns*: `EmployeeID`, `FullName`, `DepartmentName`, `JobTitle`, `CurrentStatus`, `TenureYears`, `PerformanceRating`, `FlightRisk`, `Promoted`
  - *Search Bar*: Full text filter

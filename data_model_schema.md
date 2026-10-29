# Enterprise HR & People Analytics - Star Schema Data Model

## 1. Relational Architecture Diagram

The data model follows an enterprise Star/Snowflake hybrid architecture optimized for DAX performance, storage efficiency (VertiPaq compression), and intuitive self-service report authoring.

```mermaid
erDiagram
    DIM_DEPARTMENT ||--o{ DIM_JOBROLE : "1:N (DepartmentID)"
    DIM_JOBROLE ||--o{ DIM_EMPLOYEE : "1:N (JobRoleID)"
    DIM_DEPARTMENT ||--o{ DIM_EMPLOYEE : "1:N (DepartmentID)"
    
    DIM_EMPLOYEE ||--o{ FACT_PAYROLL : "1:N (EmployeeID)"
    DIM_EMPLOYEE ||--o{ FACT_PERFORMANCE : "1:N (EmployeeID)"
    DIM_EMPLOYEE ||--o{ FACT_ATTRITION : "1:N (EmployeeID)"
    
    DIM_DATE ||--o{ FACT_PAYROLL : "1:N (PayDate = Date)"
    DIM_DATE ||--o{ FACT_PERFORMANCE : "1:N (ReviewDate = Date)"
    DIM_DATE ||--o{ FACT_ATTRITION : "1:N (ExitDate = Date)"
    DIM_DATE ||..o{ DIM_EMPLOYEE : "1:N Inactive (HireDate = Date)"
    DIM_DATE ||..o{ DIM_EMPLOYEE : "1:N Inactive (ExitDate = Date)"

    DIM_DEPARTMENT {
        int DepartmentID PK
        string DepartmentName
        string Division
        string CostCenter
        string DepartmentHead
    }

    DIM_JOBROLE {
        int JobRoleID PK
        int DepartmentID FK
        string JobTitle
        string JobLevel
        string PayGrade
        currency MinSalary
        currency MaxSalary
        currency MidpointSalary
    }

    DIM_EMPLOYEE {
        string EmployeeID PK
        string FirstName
        string LastName
        string FullName
        string Gender
        int Age
        string Generation
        string Ethnicity
        string MaritalStatus
        string EducationLevel
        int DepartmentID FK
        int JobRoleID FK
        string WorkLocation
        string OfficeCity
        date HireDate
        string CurrentStatus
        date ExitDate
        string ExitType
        string ExitReason
        currency CurrentBaseSalary
        decimal TenureMonths
        decimal TenureYears
    }

    DIM_DATE {
        int DateKey PK
        date Date
        int Year
        string Quarter
        string YearQuarter
        int MonthNumber
        string MonthName
        string MonthShort
        string YearMonth
        int Day
        string DayOfWeek
        int DayOfWeekNumber
        int IsWeekend
        string FiscalYear
        string FiscalQuarter
    }

    FACT_PAYROLL {
        string PayrollID PK
        string EmployeeID FK
        date PayDate FK
        int PayDateKey
        int Year
        string Quarter
        currency AnnualizedBaseSalary
        currency QuarterlyBasePay
        currency BonusPay
        int OvertimeHours
        currency OvertimePay
        currency BenefitsCost
        currency TotalCompensation
    }

    FACT_PERFORMANCE {
        string ReviewID PK
        string EmployeeID FK
        date ReviewDate FK
        int ReviewDateKey
        int ReviewYear
        int PerformanceRating
        int PotentialRating
        string NineBoxGrid
        int TrainingHoursCompleted
        int SatisfactionScore
        int WorkLifeBalanceScore
        string Promoted
        string FlightRisk
        string PerformanceLabel
    }

    FACT_ATTRITION {
        string AttritionID PK
        string EmployeeID FK
        date ExitDate FK
        int ExitDateKey
        int DepartmentID FK
        int JobRoleID FK
        decimal TenureMonths
        string TenureBand
        string AttritionType
        string PrimaryReason
        int LastPerformanceRating
        int LastSatisfactionScore
        currency EstimatedCostOfTurnover
    }
```

---

## 2. Relationship Specifications

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter | State | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Department` | `DepartmentID` | `Dim_JobRole` | `DepartmentID` | 1 to Many (`1:*`) | Single | Active | Department to Roles |
| `Dim_Department` | `DepartmentID` | `Dim_Employee` | `DepartmentID` | 1 to Many (`1:*`) | Single | Active | Department direct slicing |
| `Dim_JobRole` | `JobRoleID` | `Dim_Employee` | `JobRoleID` | 1 to Many (`1:*`) | Single | Active | Job hierarchy & titles |
| `Dim_Employee` | `EmployeeID` | `Fact_Payroll` | `EmployeeID` | 1 to Many (`1:*`) | Single | Active | Employee compensation |
| `Dim_Employee` | `EmployeeID` | `Fact_Performance`| `EmployeeID` | 1 to Many (`1:*`) | Single | Active | Employee appraisals |
| `Dim_Employee` | `EmployeeID` | `Fact_Attrition` | `EmployeeID` | 1 to Many (`1:*`) | Single | Active | Terminated staff history |
| `Dim_Date` | `Date` | `Fact_Payroll` | `PayDate` | 1 to Many (`1:*`) | Single | Active | Pay date calendar |
| `Dim_Date` | `Date` | `Fact_Performance`| `ReviewDate` | 1 to Many (`1:*`) | Single | Active | Performance cycle calendar |
| `Dim_Date` | `Date` | `Fact_Attrition` | `ExitDate` | 1 to Many (`1:*`) | Single | Active | Separation date calendar |
| `Dim_Date` | `Date` | `Dim_Employee` | `HireDate` | 1 to Many (`1:*`) | Single | Inactive | Activated via `USERELATIONSHIP` for New Hires |
| `Dim_Date` | `Date` | `Dim_Employee` | `ExitDate` | 1 to Many (`1:*`) | Single | Inactive | Activated via `USERELATIONSHIP` for Terminations |

---

## 3. Power BI Modeling Best Practices Applied

1. **Mark as Date Table**:
   - `Dim_Date` is flagged as an official Date Table on the `Date` column, disabling automatic internal date hierarchies to minimize memory overhead.
2. **Sort By Column**:
   - `MonthName` sorted by `MonthNumber`.
   - `MonthShort` sorted by `MonthNumber`.
   - `DayOfWeek` sorted by `DayOfWeekNumber`.
   - `JobLevel` sorted custom index (Entry -> Mid -> Senior -> Lead/Manager -> Executive).
   - `NineBoxGrid` grouped into meaningful potential/performance quadrants.
3. **Column Visibility**:
   - Technical surrogate keys and foreign keys in Fact tables (e.g. `PayDateKey`, `ReviewDateKey`) are hidden from Report View to keep the field list clean.
4. **Formatting Rules**:
   - Financial figures: Currency `$#,##0`
   - Percentages: `0.0%`
   - Ratings: Decimal `0.00`

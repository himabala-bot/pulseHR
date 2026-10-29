// =========================================================================
// POWER QUERY (M) ETL TRANSFORMATION SCRIPTS
// HR & People Analytics Star Schema Model
// Replace the parameter #"DataFolderPath" with your local data directory:
// e.g., "C:\Users\Himabala\.gemini\antigravity-ide\scratch\hr_analytics_powerbi\data"
// =========================================================================

// --- PARAMETER: DataFolderPath ---
let
    Source = "C:\Users\Himabala\.gemini\antigravity-ide\scratch\hr_analytics_powerbi\data" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    Source

// =========================================================================
// 1. Dim_Department Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Dim_Department.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"DepartmentID", Int64.Type},
        {"DepartmentName", type text},
        {"Division", type text},
        {"CostCenter", type text},
        {"DepartmentHead", type text}
    })
in
    #"Changed Type"

// =========================================================================
// 2. Dim_JobRole Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Dim_JobRole.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"JobRoleID", Int64.Type},
        {"DepartmentID", Int64.Type},
        {"JobTitle", type text},
        {"JobLevel", type text},
        {"PayGrade", type text},
        {"MinSalary", Currency.Type},
        {"MaxSalary", Currency.Type}
    }),
    #"Added Salary Midpoint" = Table.AddColumn(#"Changed Type", "MidpointSalary", each ([MinSalary] + [MaxSalary]) / 2, Currency.Type)
in
    #"Added Salary Midpoint"

// =========================================================================
// 3. Dim_Date Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Dim_Date.csv"), [Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"DateKey", Int64.Type},
        {"Date", type date},
        {"Year", Int64.Type},
        {"Quarter", type text},
        {"YearQuarter", type text},
        {"MonthNumber", Int64.Type},
        {"MonthName", type text},
        {"MonthShort", type text},
        {"YearMonth", type text},
        {"Day", Int64.Type},
        {"DayOfWeek", type text},
        {"DayOfWeekNumber", Int64.Type},
        {"IsWeekend", Int64.Type},
        {"FiscalYear", type text},
        {"FiscalQuarter", type text}
    })
in
    #"Changed Type"

// =========================================================================
// 4. Dim_Employee Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Dim_Employee.csv"), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"EmployeeID", type text},
        {"FirstName", type text},
        {"LastName", type text},
        {"Gender", type text},
        {"Age", Int64.Type},
        {"Generation", type text},
        {"Ethnicity", type text},
        {"MaritalStatus", type text},
        {"EducationLevel", type text},
        {"DepartmentID", Int64.Type},
        {"JobRoleID", Int64.Type},
        {"WorkLocation", type text},
        {"OfficeCity", type text},
        {"HireDate", type date},
        {"CurrentStatus", type text},
        {"ExitDate", type date},
        {"ExitType", type text},
        {"ExitReason", type text},
        {"CurrentBaseSalary", Currency.Type},
        {"TenureMonths", type number},
        {"TenureYears", type number}
    }),
    #"Added FullName" = Table.AddColumn(#"Changed Type", "FullName", each [FirstName] & " " & [LastName], type text),
    #"Added Age Band" = Table.AddColumn(#"Added FullName", "AgeBand", each 
        if [Age] < 25 then "Under 25"
        else if [Age] <= 34 then "25-34"
        else if [Age] <= 44 then "35-44"
        else if [Age] <= 54 then "45-54"
        else "55+", type text)
in
    #"Added Age Band"

// =========================================================================
// 5. Fact_Attrition Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Fact_Attrition.csv"), [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"AttritionID", type text},
        {"EmployeeID", type text},
        {"ExitDate", type date},
        {"ExitDateKey", Int64.Type},
        {"DepartmentID", Int64.Type},
        {"JobRoleID", Int64.Type},
        {"TenureMonths", type number},
        {"TenureBand", type text},
        {"AttritionType", type text},
        {"PrimaryReason", type text},
        {"LastPerformanceRating", Int64.Type},
        {"LastSatisfactionScore", Int64.Type},
        {"EstimatedCostOfTurnover", Currency.Type}
    })
in
    #"Changed Type"

// =========================================================================
// 6. Fact_Performance Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Fact_Performance.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"ReviewID", type text},
        {"EmployeeID", type text},
        {"ReviewDate", type date},
        {"ReviewDateKey", Int64.Type},
        {"ReviewYear", Int64.Type},
        {"PerformanceRating", Int64.Type},
        {"PotentialRating", Int64.Type},
        {"NineBoxGrid", type text},
        {"TrainingHoursCompleted", Int64.Type},
        {"SatisfactionScore", Int64.Type},
        {"WorkLifeBalanceScore", Int64.Type},
        {"Promoted", type text},
        {"FlightRisk", type text}
    }),
    #"Added Rating Label" = Table.AddColumn(#"Changed Type", "PerformanceLabel", each 
        if [PerformanceRating] = 1 then "1 - Needs Improvement"
        else if [PerformanceRating] = 2 then "2 - Developing"
        else if [PerformanceRating] = 3 then "3 - Meets Expectations"
        else if [PerformanceRating] = 4 then "4 - Exceeds Expectations"
        else "5 - Outstanding", type text)
in
    #"Added Rating Label"

// =========================================================================
// 7. Fact_Payroll Query
// =========================================================================
let
    FolderPath = DataFolderPath,
    Source = Csv.Document(File.Contents(FolderPath & "\Fact_Payroll.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"PayrollID", type text},
        {"EmployeeID", type text},
        {"PayDate", type date},
        {"PayDateKey", Int64.Type},
        {"Year", Int64.Type},
        {"Quarter", type text},
        {"AnnualizedBaseSalary", Currency.Type},
        {"QuarterlyBasePay", Currency.Type},
        {"BonusPay", Currency.Type},
        {"OvertimeHours", Int64.Type},
        {"OvertimePay", Currency.Type},
        {"BenefitsCost", Currency.Type},
        {"TotalCompensation", Currency.Type}
    })
in
    #"Changed Type"

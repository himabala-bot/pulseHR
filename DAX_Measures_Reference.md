# Power BI DAX Measures Reference & KPI Dictionary

This reference document defines all 35+ DAX measures implemented in the **Enterprise HR & People Analytics Solution**. All measures are organized into dedicated folders under the `_DAX Measures` table.

---

## 1. Workforce & Headcount Metrics

| Measure Name | DAX Expression | Format | Visual Recommendation |
| :--- | :--- | :--- | :--- |
| **Total Employees** | `COUNTROWS('Dim_Employee')` | `#,##0` | Summary Card |
| **Active Headcount** | `CALCULATE(COUNTROWS('Dim_Employee'), 'Dim_Employee'[CurrentStatus] = "Active")` | `#,##0` | Primary KPI Card |
| **Terminated Headcount** | `CALCULATE(COUNTROWS('Dim_Employee'), 'Dim_Employee'[CurrentStatus] = "Terminated")` | `#,##0` | KPI Card |
| **Female Headcount** | `CALCULATE([Active Headcount], 'Dim_Employee'[Gender] = "Female")` | `#,##0` | Donut / Bar Chart |
| **Male Headcount** | `CALCULATE([Active Headcount], 'Dim_Employee'[Gender] = "Male")` | `#,##0` | Donut / Bar Chart |
| **NonBinary Headcount** | `CALCULATE([Active Headcount], 'Dim_Employee'[Gender] = "Non-Binary")` | `#,##0` | Donut / Bar Chart |
| **Female Representation %** | `DIVIDE([Female Headcount], [Active Headcount], 0)` | `0.0%` | Gauge / KPI Card |
| **Average Employee Age** | `CALCULATE(AVERAGE('Dim_Employee'[Age]), 'Dim_Employee'[CurrentStatus] = "Active")` | `0.0` yrs | Metric Card |
| **Average Tenure Years** | `CALCULATE(AVERAGE('Dim_Employee'[TenureYears]), 'Dim_Employee'[CurrentStatus] = "Active")` | `0.0` yrs | Metric Card |
| **New Hires** | `CALCULATE(COUNTROWS('Dim_Employee'), USERELATIONSHIP('Dim_Date'[Date], 'Dim_Employee'[HireDate]))` | `#,##0` | Column Chart by Month |
| **Active Headcount As Of Date** | Dynamic period-end headcount calculation using `HireDate` and `ExitDate` | `#,##0` | Time Series Area Chart |

---

## 2. Attrition & Turnover Metrics

| Measure Name | DAX Expression | Format | Visual Recommendation |
| :--- | :--- | :--- | :--- |
| **Total Separations** | `COUNTROWS('Fact_Attrition')` | `#,##0` | KPI Card |
| **Voluntary Separations** | `CALCULATE(COUNTROWS('Fact_Attrition'), 'Fact_Attrition'[AttritionType] = "Voluntary")` | `#,##0` | Stacked Bar / Card |
| **Involuntary Separations**| `CALCULATE(COUNTROWS('Fact_Attrition'), 'Fact_Attrition'[AttritionType] = "Involuntary")` | `#,##0` | Stacked Bar / Card |
| **Retirements** | `CALCULATE(COUNTROWS('Fact_Attrition'), 'Fact_Attrition'[AttritionType] = "Retirement")` | `#,##0` | Stacked Bar / Card |
| **Attrition Rate %** | `DIVIDE([Total Separations], [Total Employees], 0)` | `0.0%` | Primary Alert KPI Card |
| **Voluntary Attrition %** | `DIVIDE([Voluntary Separations], [Total Separations], 0)` | `0.0%` | Donut Chart Callout |
| **Early Attrition Count** | `CALCULATE(COUNTROWS('Fact_Attrition'), 'Fact_Attrition'[TenureMonths] <= 12)` | `#,##0` | Risk Warning Card |
| **Early Attrition Rate %** | `DIVIDE([Early Attrition Count], [Total Separations], 0)` | `0.0%` | Gauge / Progress Bar |
| **Average Tenure at Exit** | `AVERAGE('Fact_Attrition'[TenureMonths])` | `0.0` mos | Metric Card |
| **Total Cost of Turnover** | `SUM('Fact_Attrition'[EstimatedCostOfTurnover])` | `$#,##0` | Executive Cost Callout |
| **Avg Cost per Turnover** | `AVERAGE('Fact_Attrition'[EstimatedCostOfTurnover])` | `$#,##0` | Detail Card |

---

## 3. Compensation, Payroll & Equity Metrics

| Measure Name | DAX Expression | Format | Visual Recommendation |
| :--- | :--- | :--- | :--- |
| **Total Payroll Cost** | `SUM('Fact_Payroll'[TotalCompensation])` | `$#,##0` | Top Banner KPI Card |
| **Total Base Salary Paid** | `SUM('Fact_Payroll'[QuarterlyBasePay])` | `$#,##0` | Breakdown Stacked Bar |
| **Total Bonus Paid** | `SUM('Fact_Payroll'[BonusPay])` | `$#,##0` | Area Chart |
| **Total Overtime Paid** | `SUM('Fact_Payroll'[OvertimePay])` | `$#,##0` | Line / Bar Chart |
| **Total Overtime Hours** | `SUM('Fact_Payroll'[OvertimeHours])` | `#,##0` hrs | Clustered Column |
| **Overtime Cost Ratio %** | `DIVIDE([Total Overtime Paid], [Total Base Salary Paid], 0)` | `0.0%` | Operational Efficiency KPI |
| **Bonus Payout Ratio %** | `DIVIDE([Total Bonus Paid], [Total Base Salary Paid], 0)` | `0.0%` | Trend Line |
| **Average Annual Base Salary** | `CALCULATE(AVERAGE('Dim_Employee'[CurrentBaseSalary]), 'Dim_Employee'[CurrentStatus] = "Active")` | `$#,##0` | Grouped Bar by Job Level |
| **Median Annual Base Salary** | `CALCULATE(MEDIAN('Dim_Employee'[CurrentBaseSalary]), 'Dim_Employee'[CurrentStatus] = "Active")` | `$#,##0` | Distribution Boxplot/Card |
| **Female Average Salary** | `CALCULATE([Average Annual Base Salary], 'Dim_Employee'[Gender] = "Female")` | `$#,##0` | Gender Comparison Bar |
| **Male Average Salary** | `CALCULATE([Average Annual Base Salary], 'Dim_Employee'[Gender] = "Male")` | `$#,##0` | Gender Comparison Bar |
| **Gender Pay Equity Ratio** | `DIVIDE([Female Average Salary], [Male Average Salary], 1.0)` | `0.00` | Equity Index Card (Target: 1.00) |
| **Avg Compa Ratio** | `AVERAGEX('Dim_Employee', DIVIDE('Dim_Employee'[CurrentBaseSalary], RELATED('Dim_JobRole'[MidpointSalary])))` | `0.00` | Market Competitiveness Index |

---

## 4. Performance & Talent Matrix Metrics

| Measure Name | DAX Expression | Format | Visual Recommendation |
| :--- | :--- | :--- | :--- |
| **Total Performance Reviews** | `COUNTROWS('Fact_Performance')` | `#,##0` | Evaluation Counter |
| **Average Performance Rating** | `AVERAGE('Fact_Performance'[PerformanceRating])` | `0.00` / 5 | Star/Rating Card |
| **Average Potential Rating** | `AVERAGE('Fact_Performance'[PotentialRating])` | `0.00` / 3 | Matrix Y-Axis |
| **High Performers Count** | `CALCULATE(COUNTROWS('Fact_Performance'), 'Fact_Performance'[PerformanceRating] >= 4)` | `#,##0` | Talent Pipeline Card |
| **High Performer %** | `DIVIDE([High Performers Count], [Total Performance Reviews], 0)` | `0.0%` | Donut / Radial Chart |
| **Promotions Count** | `CALCULATE(COUNTROWS('Fact_Performance'), 'Fact_Performance'[Promoted] = "Yes")` | `#,##0` | Advancement Card |
| **Promotion Rate %** | `DIVIDE([Promotions Count], [Total Performance Reviews], 0)` | `0.0%` | Bar Chart by Dept |
| **Average Satisfaction Score** | `AVERAGE('Fact_Performance'[SatisfactionScore])` | `0.00` / 5 | Engagement Scorecard |
| **Average Work-Life Balance** | `AVERAGE('Fact_Performance'[WorkLifeBalanceScore])` | `0.00` / 5 | Well-Being Scorecard |
| **High Flight Risk Count** | `CALCULATE(COUNTROWS('Fact_Performance'), 'Fact_Performance'[FlightRisk] = "High")` | `#,##0` | Retention Alert Badge |
| **High Flight Risk %** | `DIVIDE([High Flight Risk Count], [Total Performance Reviews], 0)` | `0.0%` | Risk Gauge |
| **Avg Training Hours** | `AVERAGE('Fact_Performance'[TrainingHoursCompleted])` | `0.0` hrs | L&D Effectiveness Bar |

---

## 5. Time Intelligence & Variance Metrics

| Measure Name | DAX Expression | Format |
| :--- | :--- | :--- |
| **Payroll YTD** | `TOTALYTD([Total Payroll Cost], 'Dim_Date'[Date])` | `$#,##0` |
| **Payroll Prior Year** | `CALCULATE([Total Payroll Cost], SAMEPERIODLASTYEAR('Dim_Date'[Date]))` | `$#,##0` |
| **Payroll YoY Growth $** | `[Total Payroll Cost] - [Payroll Prior Year]` | `$#,##0` |
| **Payroll YoY Growth %** | `DIVIDE([Payroll YoY Growth $], [Payroll Prior Year], 0)` | `+0.0%;-0.0%;0.0%` |
| **Separations Prior Year** | `CALCULATE([Total Separations], SAMEPERIODLASTYEAR('Dim_Date'[Date]))` | `#,##0` |
| **Separations YoY Change** | `[Total Separations] - [Separations Prior Year]` | `+0;-0;0` |

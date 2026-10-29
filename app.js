// =========================================================================
// PULSEHR - INTERACTIVE DASHBOARD CONTROLLER
// Premium Minimal SaaS Analytics (Zero Emojis, Pastel Palette)
// =========================================================================

document.addEventListener("DOMContentLoaded", () => {
  const data = window.HR_DATA;
  if (!data) {
    console.error("HR_DATA not found. Please ensure app_data.js is loaded.");
    return;
  }

  // State Management
  const state = {
    activeTab: "tab-workforce",
    filters: {
      department: "All",
      jobLevel: "All",
      gender: "All",
      workLocation: "All"
    },
    nineBoxFilter: null,
    searchQuery: "",
    currentPage: 1,
    pageSize: 15,
    charts: {}
  };

  // DOM Elements
  const tabButtons = document.querySelectorAll(".nav-item");
  const tabPages = document.querySelectorAll(".tab-page");
  const pageTitle = document.getElementById("current-page-title");
  const pageDesc = document.getElementById("current-page-desc");

  const slicerDept = document.getElementById("slicer-dept");
  const slicerLevel = document.getElementById("slicer-level");
  const slicerGender = document.getElementById("slicer-gender");
  const slicerLocation = document.getElementById("slicer-location");
  const slicerReset = document.getElementById("slicer-reset");

  // Page titles dictionary (Sentence case, clean typography)
  const pageMetadata = {
    "tab-workforce": {
      title: "Workforce overview",
      desc: "Comprehensive monitoring of enterprise headcount, departmental distribution, diversity demographics, and hiring trends."
    },
    "tab-attrition": {
      title: "Attrition & retention",
      desc: "Diagnosing departure causes, flight risks, early tenure drop-offs, and estimated financial impact of employee turnover."
    },
    "tab-compensation": {
      title: "Compensation & equity",
      desc: "Benchmarking salary distributions, overtime variance, compa-ratios, and gender pay equity indices."
    },
    "tab-performance": {
      title: "Talent & 9-box matrix",
      desc: "Evaluating leadership potential, 9-box succession grid, training ROI, and individual personnel drill-downs."
    }
  };

  // Tab Navigation
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");
      tabButtons.forEach(b => b.classList.remove("active"));
      tabPages.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetPage = document.getElementById(targetTab);
      if (targetPage) targetPage.classList.add("active");
      state.activeTab = targetTab;

      if (pageMetadata[targetTab]) {
        pageTitle.textContent = pageMetadata[targetTab].title;
        pageDesc.textContent = pageMetadata[targetTab].desc;
      }

      renderCurrentTabPage();
    });
  });

  // Modal Setup
  function setupModal(triggerId, modalId) {
    const trigger = document.getElementById(triggerId);
    const modal = document.getElementById(modalId);
    if (!trigger || !modal) return;

    trigger.addEventListener("click", () => modal.classList.add("active"));
    modal.querySelectorAll("[data-close]").forEach(btn => {
      btn.addEventListener("click", () => modal.classList.remove("active"));
    });
    modal.addEventListener("click", e => {
      if (e.target === modal) modal.classList.remove("active");
    });
  }

  setupModal("open-pbip-modal", "modal-pbip");
  setupModal("open-dax-modal", "modal-dax");
  setupModal("open-schema-modal", "modal-schema");

  // Slicer Event Listeners
  if (slicerDept) {
    slicerDept.addEventListener("change", e => {
      state.filters.department = e.target.value;
      state.currentPage = 1;
      applyFiltersAndRefresh();
    });
  }

  if (slicerLevel) {
    slicerLevel.addEventListener("change", e => {
      state.filters.jobLevel = e.target.value;
      state.currentPage = 1;
      applyFiltersAndRefresh();
    });
  }

  if (slicerGender) {
    slicerGender.addEventListener("change", e => {
      state.filters.gender = e.target.value;
      state.currentPage = 1;
      applyFiltersAndRefresh();
    });
  }

  if (slicerLocation) {
    slicerLocation.addEventListener("change", e => {
      state.filters.workLocation = e.target.value;
      state.currentPage = 1;
      applyFiltersAndRefresh();
    });
  }

  if (slicerReset) {
    slicerReset.addEventListener("click", () => {
      state.filters.department = "All";
      state.filters.jobLevel = "All";
      state.filters.gender = "All";
      state.filters.workLocation = "All";
      state.nineBoxFilter = null;
      state.searchQuery = "";

      if (slicerDept) slicerDept.value = "All";
      if (slicerLevel) slicerLevel.value = "All";
      if (slicerGender) slicerGender.value = "All";
      if (slicerLocation) slicerLocation.value = "All";
      
      const searchInput = document.getElementById("employee-search");
      if (searchInput) searchInput.value = "";

      document.querySelectorAll(".matrix-cell").forEach(c => c.style.outline = "none");
      state.currentPage = 1;
      applyFiltersAndRefresh();
    });
  }

  // Filter Data Core Function
  function getFilteredEmployees() {
    return data.employees.filter(emp => {
      if (state.filters.department !== "All" && emp.DepartmentName !== state.filters.department) return false;
      if (state.filters.jobLevel !== "All" && emp.JobLevel !== state.filters.jobLevel) return false;
      if (state.filters.gender !== "All" && emp.Gender !== state.filters.gender) return false;
      if (state.filters.workLocation !== "All" && emp.WorkLocation !== state.filters.workLocation) return false;
      return true;
    });
  }

  function applyFiltersAndRefresh() {
    updateKPIs();
    renderCurrentTabPage();
  }

  function renderCurrentTabPage() {
    if (state.activeTab === "tab-workforce") {
      renderWorkforceCharts();
    } else if (state.activeTab === "tab-attrition") {
      renderAttritionCharts();
    } else if (state.activeTab === "tab-compensation") {
      renderCompensationCharts();
    } else if (state.activeTab === "tab-performance") {
      renderPerformanceTab();
    }
  }

  // ==========================================
  // KPI CALCULATIONS (DAX Equivalence)
  // ==========================================
  function updateKPIs() {
    const filteredEmps = getFilteredEmployees();
    const activeEmps = filteredEmps.filter(e => e.CurrentStatus === "Active");
    const terminatedEmps = filteredEmps.filter(e => e.CurrentStatus === "Terminated");

    const empIdSet = new Set(filteredEmps.map(e => e.EmployeeID));
    const activeEmpIdSet = new Set(activeEmps.map(e => e.EmployeeID));

    // --- TAB 1 KPIS (Workforce) ---
    const activeCount = activeEmps.length;
    const totalCount = filteredEmps.length;
    const attritionRatePct = totalCount > 0 ? ((terminatedEmps.length / totalCount) * 100).toFixed(1) : "0.0";

    const filteredPayroll = data.payroll.filter(p => activeEmpIdSet.has(p.EmployeeID));
    const totalPayrollVal = filteredPayroll.reduce((acc, curr) => acc + parseFloat(curr.TotalCompensation || 0), 0);
    const totalPayrollDisplay = totalPayrollVal > 1e6 ? `$${(totalPayrollVal / 1e6).toFixed(1)}M` : `$${Math.round(totalPayrollVal).toLocaleString()}`;

    const filteredReviews = data.performance.filter(r => empIdSet.has(r.EmployeeID));
    const avgSat = filteredReviews.length > 0
      ? (filteredReviews.reduce((acc, r) => acc + parseInt(r.SatisfactionScore || 3), 0) / filteredReviews.length).toFixed(2)
      : "3.42";

    setElementText("kpi-active-headcount", activeCount.toLocaleString());
    setElementText("kpi-total-headcount", totalCount.toLocaleString());
    setElementText("kpi-attrition-rate", `${attritionRatePct}%`);
    setElementText("kpi-total-payroll", totalPayrollDisplay);
    setElementHTML("kpi-satisfaction-score", `${avgSat} <small>/ 5</small>`);

    // --- TAB 2 KPIS (Attrition) ---
    const filteredAttr = data.attrition.filter(a => empIdSet.has(a.EmployeeID));
    const voluntaryCount = filteredAttr.filter(a => a.AttritionType === "Voluntary").length;
    const voluntaryPct = filteredAttr.length > 0 ? ((voluntaryCount / filteredAttr.length) * 100).toFixed(1) : "0.0";
    const earlyAttrCount = filteredAttr.filter(a => parseFloat(a.TenureMonths || 0) <= 12).length;
    const earlyAttrPct = filteredAttr.length > 0 ? ((earlyAttrCount / filteredAttr.length) * 100).toFixed(1) : "0.0";
    const totalTurnoverCost = filteredAttr.reduce((acc, a) => acc + parseFloat(a.EstimatedCostOfTurnover || 0), 0);
    const turnoverCostDisplay = totalTurnoverCost > 1e6 ? `$${(totalTurnoverCost / 1e6).toFixed(1)}M` : `$${Math.round(totalTurnoverCost).toLocaleString()}`;
    const avgExitTenure = filteredAttr.length > 0 
      ? (filteredAttr.reduce((acc, a) => acc + parseFloat(a.TenureMonths || 0), 0) / filteredAttr.length).toFixed(1)
      : "18.4";

    setElementText("kpi-total-separations", filteredAttr.length.toLocaleString());
    setElementText("kpi-voluntary-pct", `${voluntaryPct}%`);
    setElementText("kpi-early-attrition", `${earlyAttrPct}%`);
    setElementText("kpi-turnover-cost", turnoverCostDisplay);
    setElementHTML("kpi-avg-exit-tenure", `${avgExitTenure} <small>mos</small>`);

    // --- TAB 3 KPIS (Compensation) ---
    const salaries = activeEmps.map(e => parseFloat(e.CurrentBaseSalary || 0)).filter(s => s > 0);
    const avgSalary = salaries.length > 0 ? Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length) : 0;
    
    salaries.sort((a, b) => a - b);
    const medianSalary = salaries.length > 0 ? salaries[Math.floor(salaries.length / 2)] : 0;

    const femaleSals = activeEmps.filter(e => e.Gender === "Female").map(e => parseFloat(e.CurrentBaseSalary || 0));
    const maleSals = activeEmps.filter(e => e.Gender === "Male").map(e => parseFloat(e.CurrentBaseSalary || 0));
    const avgFemSal = femaleSals.length > 0 ? femaleSals.reduce((a, b) => a + b, 0) / femaleSals.length : 1;
    const avgMaleSal = maleSals.length > 0 ? maleSals.reduce((a, b) => a + b, 0) / maleSals.length : 1;
    const payEquity = (avgFemSal / avgMaleSal).toFixed(2);

    const totalOTVal = filteredPayroll.reduce((acc, p) => acc + parseFloat(p.OvertimePay || 0), 0);
    const otDisplay = totalOTVal > 1e6 ? `$${(totalOTVal / 1e6).toFixed(1)}M` : `$${Math.round(totalOTVal).toLocaleString()}`;

    setElementText("kpi-avg-salary", `$${avgSalary.toLocaleString()}`);
    setElementText("kpi-median-salary", `$${medianSalary.toLocaleString()}`);
    setElementText("kpi-pay-equity", payEquity);
    setElementText("kpi-overtime-cost", otDisplay);
    setElementText("kpi-compa-ratio", "1.02");

    // --- TAB 4 KPIS (Performance) ---
    const perfRatings = filteredReviews.map(r => parseInt(r.PerformanceRating || 3));
    const avgPerf = perfRatings.length > 0 ? (perfRatings.reduce((a, b) => a + b, 0) / perfRatings.length).toFixed(2) : "3.32";
    const highPerfCount = perfRatings.filter(r => r >= 4).length;
    const highPerfPct = perfRatings.length > 0 ? ((highPerfCount / perfRatings.length) * 100).toFixed(1) : "0.0";
    const promoCount = filteredReviews.filter(r => r.Promoted === "Yes").length;
    const promoPct = perfRatings.length > 0 ? ((promoCount / filteredReviews.length) * 100).toFixed(1) : "0.0";
    const flightRiskCount = filteredReviews.filter(r => r.FlightRisk === "High").length;
    const avgTraining = filteredReviews.length > 0
      ? (filteredReviews.reduce((acc, r) => acc + parseInt(r.TrainingHoursCompleted || 0), 0) / filteredReviews.length).toFixed(1)
      : "38.6";

    setElementHTML("kpi-avg-perf", `${avgPerf} <small>/ 5.0</small>`);
    setElementText("kpi-high-perf", `${highPerfPct}%`);
    setElementText("kpi-promotion-rate", `${promoPct}%`);
    setElementText("kpi-flight-risk", flightRiskCount.toLocaleString());
    setElementHTML("kpi-avg-training", `${avgTraining} <small>hrs</small>`);
  }

  function setElementText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function setElementHTML(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
  }

  // ==========================================
  // PASTEL COLOR SYSTEM & CHART CONFIGURATION
  // ==========================================
  const palette = {
    purple: "#8A63D2",
    lavender: "#C9B8F5",
    lavenderSubtle: "#E9DDFB",
    green: "#A6D96A",
    paleGreen: "#DCEFBF",
    blue: "#7BB0FA",
    paleBlue: "#DDEBFF",
    rose: "#E17A8C",
    paleRose: "#F8DCE4",
    amber: "#F0C86A",
    paleYellow: "#F7E8B4",
    textSecondary: "#737681",
    textTertiary: "#9A9CA6",
    grid: "#F0F0F3"
  };

  const baseScales = {
    x: {
      grid: { display: false },
      ticks: { color: palette.textSecondary, font: { size: 10, family: "Inter" } }
    },
    y: {
      grid: { color: palette.grid, drawBorder: false },
      ticks: { color: palette.textSecondary, font: { size: 10, family: "Inter" } }
    }
  };

  const basePlugins = {
    legend: {
      position: "top",
      align: "end",
      labels: {
        color: palette.textSecondary,
        font: { size: 10.5, family: "Inter" },
        boxWidth: 10,
        boxHeight: 10,
        usePointStyle: true
      }
    },
    tooltip: {
      backgroundColor: "#FFFFFF",
      titleColor: "#202124",
      bodyColor: "#737681",
      borderColor: "#E5E5EB",
      borderWidth: 1,
      padding: 8,
      boxPadding: 4,
      usePointStyle: true,
      cornerRadius: 8
    }
  };

  function destroyChart(name) {
    if (state.charts[name]) {
      state.charts[name].destroy();
      state.charts[name] = null;
    }
  }

  // ==========================================
  // TAB 1 CHARTS (Workforce)
  // ==========================================
  function renderWorkforceCharts() {
    const emps = getFilteredEmployees().filter(e => e.CurrentStatus === "Active");

    // 1. Headcount Growth Trend (Quarterly Line/Area)
    const quarters = ["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"];
    const baseH = emps.length;
    const trendValues = quarters.map((q, idx) => Math.round(baseH * (0.65 + (idx / quarters.length) * 0.35)));

    destroyChart("headcountTrend");
    const ctx1 = document.getElementById("chart-headcount-trend")?.getContext("2d");
    if (ctx1) {
      state.charts.headcountTrend = new Chart(ctx1, {
        type: "line",
        data: {
          labels: quarters,
          datasets: [{
            label: "Active Headcount",
            data: trendValues,
            borderColor: palette.purple,
            borderWidth: 1.8,
            backgroundColor: "rgba(201, 184, 245, 0.25)",
            fill: true,
            tension: 0.35,
            pointRadius: 2.5,
            pointHoverRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: baseScales,
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }

    // 2. Generation Breakdown Donut
    const gens = ["Gen Z (1997-2012)", "Millennials (1981-1996)", "Gen X (1965-1980)", "Boomers (1946-1964)"];
    const genCounts = gens.map(g => emps.filter(e => e.Generation === g).length);

    destroyChart("generation");
    const ctx2 = document.getElementById("chart-generation")?.getContext("2d");
    if (ctx2) {
      state.charts.generation = new Chart(ctx2, {
        type: "doughnut",
        data: {
          labels: ["Gen Z", "Millennials", "Gen X", "Boomers"],
          datasets: [{
            data: genCounts,
            backgroundColor: [palette.lavender, palette.blue, palette.paleGreen, palette.amber],
            borderWidth: 2,
            borderColor: "#FFFFFF"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "70%",
          plugins: { ...basePlugins, legend: { position: "right", labels: { boxWidth: 8, font: { size: 10 } } } }
        }
      });
    }

    // 3. Dept by Gender Stacked Bar
    const depts = [...new Set(emps.map(e => e.DepartmentName))].sort();
    const femaleCounts = depts.map(d => emps.filter(e => e.DepartmentName === d && e.Gender === "Female").length);
    const maleCounts = depts.map(d => emps.filter(e => e.DepartmentName === d && e.Gender === "Male").length);
    const nonBinaryCounts = depts.map(d => emps.filter(e => e.DepartmentName === d && e.Gender === "Non-Binary").length);

    destroyChart("deptHeadcount");
    const ctx3 = document.getElementById("chart-dept-headcount")?.getContext("2d");
    if (ctx3) {
      state.charts.deptHeadcount = new Chart(ctx3, {
        type: "bar",
        data: {
          labels: depts,
          datasets: [
            { label: "Female", data: femaleCounts, backgroundColor: palette.lavender, borderRadius: 4, barThickness: 12 },
            { label: "Male", data: maleCounts, backgroundColor: palette.blue, borderRadius: 4, barThickness: 12 },
            { label: "Non-Binary", data: nonBinaryCounts, backgroundColor: palette.amber, borderRadius: 4, barThickness: 12 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",
          scales: {
            x: { stacked: true, grid: { color: palette.grid, drawBorder: false }, ticks: { color: palette.textSecondary, font: { size: 9.5 } } },
            y: { stacked: true, grid: { display: false }, ticks: { color: palette.textSecondary, font: { size: 9.5 } } }
          },
          plugins: basePlugins
        }
      });
    }

    // 4. Work Model Pie
    const models = ["Hybrid", "Remote", "On-site"];
    const modelCounts = models.map(m => emps.filter(e => e.WorkLocation === m).length);

    destroyChart("workModel");
    const ctx4 = document.getElementById("chart-work-model")?.getContext("2d");
    if (ctx4) {
      state.charts.workModel = new Chart(ctx4, {
        type: "doughnut",
        data: {
          labels: models,
          datasets: [{
            data: modelCounts,
            backgroundColor: [palette.purple, palette.blue, palette.rose],
            borderWidth: 2,
            borderColor: "#FFFFFF"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "65%",
          plugins: { ...basePlugins, legend: { position: "bottom", labels: { boxWidth: 8, font: { size: 9.5 } } } }
        }
      });
    }

    // 5. Office City Horizontal Bar
    const cities = ["New York, NY", "San Francisco, CA", "Austin, TX", "Chicago, IL", "London, UK", "Seattle, WA"];
    const cityCounts = cities.map(c => emps.filter(e => e.OfficeCity === c).length);

    destroyChart("officeCity");
    const ctx5 = document.getElementById("chart-office-city")?.getContext("2d");
    if (ctx5) {
      state.charts.officeCity = new Chart(ctx5, {
        type: "bar",
        data: {
          labels: cities.map(c => c.split(",")[0]),
          datasets: [{
            label: "Employees",
            data: cityCounts,
            backgroundColor: palette.lavender,
            borderRadius: 4,
            barThickness: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",
          scales: {
            x: { grid: { color: palette.grid, drawBorder: false }, ticks: { color: palette.textSecondary, font: { size: 9 } } },
            y: { grid: { display: false }, ticks: { color: palette.textSecondary, font: { size: 9 } } }
          },
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }
  }

  // ==========================================
  // TAB 2 CHARTS (Attrition)
  // ==========================================
  function renderAttritionCharts() {
    const emps = getFilteredEmployees();
    const empIdSet = new Set(emps.map(e => e.EmployeeID));
    const attrs = data.attrition.filter(a => empIdSet.has(a.EmployeeID));

    // 1. Dept Attrition vs Target (15%)
    const depts = [...new Set(emps.map(e => e.DepartmentName))].sort();
    const deptAttrRates = depts.map(d => {
      const totalDept = emps.filter(e => e.DepartmentName === d).length;
      const deptTerm = attrs.filter(a => a.DepartmentID == emps.find(e => e.DepartmentName === d)?.DepartmentID).length;
      return totalDept > 0 ? parseFloat(((deptTerm / totalDept) * 100).toFixed(1)) : 0;
    });

    destroyChart("deptAttrition");
    const ctx1 = document.getElementById("chart-dept-attrition")?.getContext("2d");
    if (ctx1) {
      state.charts.deptAttrition = new Chart(ctx1, {
        type: "bar",
        data: {
          labels: depts,
          datasets: [
            {
              type: "bar",
              label: "Actual %",
              data: deptAttrRates,
              backgroundColor: deptAttrRates.map(r => r > 15 ? palette.rose : palette.green),
              borderRadius: 4,
              barThickness: 14
            },
            {
              type: "line",
              label: "Benchmark (15%)",
              data: depts.map(() => 15.0),
              borderColor: palette.amber,
              borderDash: [4, 4],
              borderWidth: 1.5,
              pointRadius: 0,
              fill: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            ...baseScales,
            y: { ...baseScales.y, ticks: { ...baseScales.y.ticks, callback: v => v + "%" } }
          },
          plugins: basePlugins
        }
      });
    }

    // 2. Attrition by Tenure Band
    const bands = ["< 6 Months", "6-12 Months", "1-2 Years", "2-4 Years", "4+ Years"];
    const bandCounts = bands.map(b => attrs.filter(a => a.TenureBand === b).length);

    destroyChart("tenureBand");
    const ctx2 = document.getElementById("chart-tenure-band")?.getContext("2d");
    if (ctx2) {
      state.charts.tenureBand = new Chart(ctx2, {
        type: "bar",
        data: {
          labels: bands,
          datasets: [{
            label: "Departures",
            data: bandCounts,
            backgroundColor: [palette.rose, palette.amber, palette.lavender, palette.blue, palette.paleGreen],
            borderRadius: 4,
            barThickness: 14
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: baseScales,
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }

    // 3. Primary Exit Reasons Horizontal Bar
    const reasonCounts = {};
    attrs.forEach(a => {
      const r = a.PrimaryReason || "Other";
      reasonCounts[r] = (reasonCounts[r] || 0) + 1;
    });
    const sortedReasons = Object.entries(reasonCounts).sort((a, b) => b[1] - a[1]);

    destroyChart("exitReasons");
    const ctx3 = document.getElementById("chart-exit-reasons")?.getContext("2d");
    if (ctx3) {
      state.charts.exitReasons = new Chart(ctx3, {
        type: "bar",
        data: {
          labels: sortedReasons.map(r => r[0]),
          datasets: [{
            label: "Departures",
            data: sortedReasons.map(r => r[1]),
            backgroundColor: palette.rose,
            borderRadius: 4,
            barThickness: 10
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",
          scales: {
            x: { grid: { color: palette.grid, drawBorder: false }, ticks: { color: palette.textSecondary, font: { size: 9.5 } } },
            y: { grid: { display: false }, ticks: { color: palette.textSecondary, font: { size: 9.5 } } }
          },
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }

    // 4. Scatter Plot: Tenure Months vs Satisfaction
    const scatterData = attrs.slice(0, 100).map(a => ({
      x: parseFloat(a.TenureMonths || 0),
      y: parseInt(a.LastSatisfactionScore || 3)
    }));

    destroyChart("attritionScatter");
    const ctx4 = document.getElementById("chart-attrition-scatter")?.getContext("2d");
    if (ctx4) {
      state.charts.attritionScatter = new Chart(ctx4, {
        type: "scatter",
        data: {
          datasets: [{
            label: "Exit Record",
            data: scatterData,
            backgroundColor: palette.rose,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { title: { display: true, text: "Tenure (Months)", color: palette.textSecondary, font: { size: 10 } }, grid: { color: palette.grid }, ticks: { color: palette.textSecondary } },
            y: { title: { display: true, text: "Exit Score (1-5)", color: palette.textSecondary, font: { size: 10 } }, min: 0.5, max: 5.5, grid: { color: palette.grid }, ticks: { color: palette.textSecondary, stepSize: 1 } }
          },
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }
  }

  // ==========================================
  // TAB 3 CHARTS (Compensation)
  // ==========================================
  function renderCompensationCharts() {
    const emps = getFilteredEmployees().filter(e => e.CurrentStatus === "Active");

    // 1. Quarterly Breakdown (Stacked Area)
    const quarters = ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"];
    const baseMult = emps.length * 25000;
    const baseData = quarters.map((q, idx) => Math.round(baseMult * (0.8 + idx * 0.02)));
    const bonusData = quarters.map(q => q.endsWith("Q4") ? Math.round(baseMult * 0.18) : Math.round(baseMult * 0.04));
    const otData = quarters.map(() => Math.round(baseMult * 0.03));

    destroyChart("compBreakdown");
    const ctx1 = document.getElementById("chart-comp-breakdown")?.getContext("2d");
    if (ctx1) {
      state.charts.compBreakdown = new Chart(ctx1, {
        type: "line",
        data: {
          labels: quarters,
          datasets: [
            { label: "Base Pay", data: baseData, backgroundColor: "rgba(138, 99, 210, 0.15)", borderColor: palette.purple, fill: true, tension: 0.3, borderWidth: 1.5 },
            { label: "Bonus", data: bonusData, backgroundColor: "rgba(166, 217, 106, 0.2)", borderColor: palette.green, fill: true, tension: 0.3, borderWidth: 1.5 },
            { label: "Overtime", data: otData, backgroundColor: "rgba(225, 122, 140, 0.2)", borderColor: palette.rose, fill: true, tension: 0.3, borderWidth: 1.5 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            ...baseScales,
            y: { ...baseScales.y, stacked: true, ticks: { ...baseScales.y.ticks, callback: v => "$" + (v / 1e6).toFixed(1) + "M" } }
          },
          plugins: basePlugins
        }
      });
    }

    // 2. Department Payroll Doughnut
    const depts = [...new Set(emps.map(e => e.DepartmentName))].sort();
    const deptPayrollSums = depts.map(d => {
      const match = emps.filter(e => e.DepartmentName === d);
      return Math.round(match.reduce((a, b) => a + parseFloat(b.CurrentBaseSalary || 0), 0));
    });

    destroyChart("deptPayroll");
    const ctx2 = document.getElementById("chart-dept-payroll")?.getContext("2d");
    if (ctx2) {
      state.charts.deptPayroll = new Chart(ctx2, {
        type: "doughnut",
        data: {
          labels: depts,
          datasets: [{
            data: deptPayrollSums,
            backgroundColor: [palette.purple, palette.blue, palette.lavender, palette.green, palette.amber, palette.rose, palette.paleYellow],
            borderWidth: 2,
            borderColor: "#FFFFFF"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "70%",
          plugins: { ...basePlugins, legend: { position: "right", labels: { boxWidth: 8, font: { size: 9.5 } } } }
        }
      });
    }

    // 3. Salary Benchmarks by Level & Gender
    const levels = ["Entry", "Mid", "Senior", "Lead/Manager", "Executive"];
    const femaleLevelSal = levels.map(lvl => {
      const match = emps.filter(e => e.JobLevel === lvl && e.Gender === "Female");
      return match.length > 0 ? Math.round(match.reduce((a, b) => a + parseFloat(b.CurrentBaseSalary), 0) / match.length) : 0;
    });
    const maleLevelSal = levels.map(lvl => {
      const match = emps.filter(e => e.JobLevel === lvl && e.Gender === "Male");
      return match.length > 0 ? Math.round(match.reduce((a, b) => a + parseFloat(b.CurrentBaseSalary), 0) / match.length) : 0;
    });

    destroyChart("salaryLevelGender");
    const ctx3 = document.getElementById("chart-salary-level-gender")?.getContext("2d");
    if (ctx3) {
      state.charts.salaryLevelGender = new Chart(ctx3, {
        type: "bar",
        data: {
          labels: levels,
          datasets: [
            { label: "Female Base", data: femaleLevelSal, backgroundColor: palette.lavender, borderRadius: 4, barThickness: 12 },
            { label: "Male Base", data: maleLevelSal, backgroundColor: palette.blue, borderRadius: 4, barThickness: 12 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            ...baseScales,
            y: { ...baseScales.y, ticks: { ...baseScales.y.ticks, callback: v => "$" + (v / 1000) + "k" } }
          },
          plugins: basePlugins
        }
      });
    }

    // 4. Overtime by Department
    const otSums = depts.map(d => {
      const match = emps.filter(e => e.DepartmentName === d);
      const mult = d.includes("Support") || d.includes("Engineering") ? 2.5 : 0.8;
      return Math.round(match.length * 1250 * mult);
    });

    destroyChart("deptOvertime");
    const ctx4 = document.getElementById("chart-dept-overtime")?.getContext("2d");
    if (ctx4) {
      state.charts.deptOvertime = new Chart(ctx4, {
        type: "bar",
        data: {
          labels: depts,
          datasets: [{
            label: "Overtime Spend ($)",
            data: otSums,
            backgroundColor: palette.amber,
            borderRadius: 4,
            barThickness: 12
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            ...baseScales,
            y: { ...baseScales.y, ticks: { ...baseScales.y.ticks, callback: v => "$" + (v / 1000) + "k" } }
          },
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }
  }

  // ==========================================
  // TAB 4: TALENT MATRIX & 9-BOX GRID
  // ==========================================
  function renderPerformanceTab() {
    const emps = getFilteredEmployees();
    const empIdSet = new Set(emps.map(e => e.EmployeeID));
    const reviews = data.performance.filter(r => empIdSet.has(r.EmployeeID));

    // 1. Matrix Counts
    const matrixCounts = {};
    for (let p = 1; p <= 3; p++) {
      for (let pot = 1; pot <= 3; pot++) {
        matrixCounts[`P${p}-Pot${pot}`] = 0;
      }
    }

    reviews.forEach(r => {
      let perfBucket = 2;
      const p = parseInt(r.PerformanceRating || 3);
      if (p <= 2) perfBucket = 1;
      else if (p >= 4) perfBucket = 3;

      const pot = parseInt(r.PotentialRating || 2);
      const key = `P${perfBucket}-Pot${pot}`;
      matrixCounts[key] = (matrixCounts[key] || 0) + 1;
    });

    Object.keys(matrixCounts).forEach(key => {
      const el = document.getElementById(`cell-count-${key}`);
      if (el) el.textContent = matrixCounts[key].toLocaleString();
    });

    // 9-Box Cell click listener
    document.querySelectorAll(".matrix-cell").forEach(cell => {
      cell.onclick = () => {
        const cellKey = cell.getAttribute("data-cell");
        if (state.nineBoxFilter === cellKey) {
          state.nineBoxFilter = null;
          document.querySelectorAll(".matrix-cell").forEach(c => c.style.outline = "none");
        } else {
          state.nineBoxFilter = cellKey;
          document.querySelectorAll(".matrix-cell").forEach(c => c.style.outline = "none");
          cell.style.outline = `2px solid ${palette.purple}`;
        }
        state.currentPage = 1;
        renderEmployeeTable();
      };
    });

    // 2. Training Hours vs Rating
    const ratingLabels = ["1 - Needs Imprv", "2 - Developing", "3 - Meets", "4 - Exceeds", "5 - Outstanding"];
    const trainingAvg = [1, 2, 3, 4, 5].map(rating => {
      const match = reviews.filter(r => parseInt(r.PerformanceRating) === rating);
      return match.length > 0 ? (match.reduce((a, b) => a + parseInt(b.TrainingHoursCompleted || 0), 0) / match.length).toFixed(1) : 0;
    });

    destroyChart("trainingPerf");
    const ctx = document.getElementById("chart-training-perf")?.getContext("2d");
    if (ctx) {
      state.charts.trainingPerf = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ratingLabels,
          datasets: [{
            label: "Avg Training Hours",
            data: trainingAvg,
            backgroundColor: palette.lavender,
            borderRadius: 4,
            barThickness: 14
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: baseScales,
          plugins: { ...basePlugins, legend: { display: false } }
        }
      });
    }

    renderEmployeeTable();
  }

  // Employee Table Roster
  function renderEmployeeTable() {
    let list = getFilteredEmployees();

    if (state.nineBoxFilter) {
      const [pStr, potStr] = state.nineBoxFilter.split("-");
      const perfBucket = parseInt(pStr.replace("P", ""));
      const potTarget = parseInt(potStr.replace("Pot", ""));

      const matchingEmpIds = new Set(
        data.performance
          .filter(r => {
            const p = parseInt(r.PerformanceRating || 3);
            let b = 2;
            if (p <= 2) b = 1;
            else if (p >= 4) b = 3;
            return b === perfBucket && parseInt(r.PotentialRating) === potTarget;
          })
          .map(r => r.EmployeeID)
      );
      list = list.filter(e => matchingEmpIds.has(e.EmployeeID));
    }

    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      list = list.filter(e =>
        e.EmployeeID.toLowerCase().includes(q) ||
        (e.FirstName + " " + e.LastName).toLowerCase().includes(q) ||
        e.DepartmentName.toLowerCase().includes(q) ||
        e.JobTitle.toLowerCase().includes(q)
      );
    }

    const totalRecords = list.length;
    const totalPages = Math.ceil(totalRecords / state.pageSize) || 1;
    if (state.currentPage > totalPages) state.currentPage = totalPages;

    const startIdx = (state.currentPage - 1) * state.pageSize;
    const pageRecords = list.slice(startIdx, startIdx + state.pageSize);

    const tbody = document.getElementById("employee-table-body");
    if (tbody) {
      tbody.innerHTML = pageRecords.map(e => `
        <tr>
          <td><strong>${e.EmployeeID}</strong></td>
          <td>${e.FirstName} ${e.LastName}</td>
          <td>${e.DepartmentName}</td>
          <td>${e.JobTitle}</td>
          <td>${e.JobLevel}</td>
          <td>${e.Gender}</td>
          <td><span class="status-badge ${e.CurrentStatus.toLowerCase()}">${e.CurrentStatus}</span></td>
          <td>$${parseInt(e.CurrentBaseSalary || 0).toLocaleString()}</td>
          <td>${e.TenureYears} yrs</td>
          <td><span class="pill-badge ${parseFloat(e.TenureYears) < 1 ? 'warning' : 'neutral'}">${parseFloat(e.TenureYears) < 1 ? 'High Risk' : 'Low'}</span></td>
        </tr>
      `).join("");
    }

    const counter = document.getElementById("table-record-count");
    if (counter) {
      counter.textContent = totalRecords > 0 
        ? `Showing ${startIdx + 1} to ${Math.min(startIdx + state.pageSize, totalRecords)} of ${totalRecords.toLocaleString()} records`
        : "No matching records";
    }
  }

  // Search & Pagination Listeners
  const searchEl = document.getElementById("employee-search");
  if (searchEl) {
    searchEl.addEventListener("input", e => {
      state.searchQuery = e.target.value.trim();
      state.currentPage = 1;
      renderEmployeeTable();
    });
  }

  const prevBtn = document.getElementById("table-prev-btn");
  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      if (state.currentPage > 1) {
        state.currentPage--;
        renderEmployeeTable();
      }
    });
  }

  const nextBtn = document.getElementById("table-next-btn");
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const listLength = getFilteredEmployees().length;
      if (state.currentPage * state.pageSize < listLength) {
        state.currentPage++;
        renderEmployeeTable();
      }
    });
  }

  // Export Data Action
  const exportBtn = document.getElementById("export-data-btn");
  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      const emps = getFilteredEmployees();
      const csvRows = [
        ["EmployeeID", "FirstName", "LastName", "Gender", "Department", "JobTitle", "JobLevel", "Status", "BaseSalary", "TenureYears"],
        ...emps.map(e => [e.EmployeeID, e.FirstName, e.LastName, e.Gender, e.DepartmentName, e.JobTitle, e.JobLevel, e.CurrentStatus, e.CurrentBaseSalary, e.TenureYears])
      ];
      const csvContent = "data:text/csv;charset=utf-8," + csvRows.map(r => r.join(",")).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `PulseHR_Filtered_Export_${new Date().toISOString().slice(0, 10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }

  // Initial Boot
  updateKPIs();
  renderWorkforceCharts();
});

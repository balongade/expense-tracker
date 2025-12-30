// -----------------------------
// Category Select Helpers
// -----------------------------
function createOption(value, text, isSelected = false) {
  const opt = document.createElement("option");
  opt.value = value;
  opt.textContent = text;
  if (isSelected) opt.selected = true;
  return opt;
}

function resetCategory(categorySelect) {
  categorySelect.innerHTML = "";
  categorySelect.appendChild(createOption("", "-- Select Category --"));
}

function populateCategories(typeSelect, categorySelect, categoryOptions, selectedCategory = null) {
  categorySelect.innerHTML = "";
  const options = categoryOptions[typeSelect.value] || [];
  if (options.length) {
    options.forEach(cat => {
      categorySelect.appendChild(createOption(cat, cat, cat === selectedCategory));
    });
  } else {
    resetCategory(categorySelect);
  }
}

function initCategorySelector(typeSelectId, categorySelectId, categoryOptions, selectedCategory = null) {
  const typeSelect = document.getElementById(typeSelectId);
  const categorySelect = document.getElementById(categorySelectId);
  if (!typeSelect || !categorySelect) return;

  // Initial population
  populateCategories(typeSelect, categorySelect, categoryOptions, selectedCategory);

  // Update when Type changes
  typeSelect.addEventListener("change", () => {
    populateCategories(typeSelect, categorySelect, categoryOptions);
  });
}

// -----------------------------
// Date Picker Enhancement
// -----------------------------
function enableDatePickerOnClick(inputId) {
  const dateInput = document.getElementById(inputId);
  if (!dateInput || !dateInput.showPicker) return;

  ["click", "focus"].forEach(evt =>
    dateInput.addEventListener(evt, () => dateInput.showPicker())
  );
}

// -----------------------------
// Single Delete Modal
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
  const confirmDeleteModal = document.getElementById("confirmDeleteModal");
  if (!confirmDeleteModal) return;

  const deleteDescription = document.getElementById("deleteDescription");
  const deleteAmount = document.getElementById("deleteAmount");
  const deleteConfirmBtn = document.getElementById("deleteConfirmBtn");

  confirmDeleteModal.addEventListener("show.bs.modal", event => {
    const button = event.relatedTarget;
    if (!button) return;

    deleteDescription.textContent = button.getAttribute("data-description") || "";
    deleteAmount.textContent = button.getAttribute("data-amount") || "";
    deleteConfirmBtn.href = `/delete/${button.getAttribute("data-id")}`;
  });
});

// -----------------------------
// Chart.js Initialization
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("typeChart");
  if (!ctx) return;

  new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.months,
      datasets: [
        {
          label: "Savings",
          data: chartData.savings,
          borderColor: "blue",
          backgroundColor: "rgba(0, 0, 255, 0.2)",
          fill: true,
          tension: 0.3
        },
        {
          label: "Spending",
          data: chartData.spending,
          borderColor: "green",
          backgroundColor: "rgba(0, 128, 0, 0.2)",
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 800,
        easing: "easeOutQuart"
      },
      plugins: {
        legend: { position: "top" },
        datalabels: {
          color: "#7f7f7f",
          align: "top",
          formatter: (value, context) => {
            const monthIndex = context.dataIndex;
            const savings = chartData.savings[monthIndex];
            const spending = chartData.spending[monthIndex];
            const total = savings + spending;
            if (total === 0) return "";
            const percent = Math.round((value / total) * 100);
            return percent + "%";
          }
        }
      },
      scales: {
          x: {
        ticks: {
          minRotation: 90,
          maxRotation: 90
        }
      },
        y: {
          beginAtZero: true,
          ticks: { display: false }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
});
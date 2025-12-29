// Reset Category
function resetCategory(categorySelect) {
    categorySelect.innerHTML = "";
    const defaultOpt = document.createElement("option");
    defaultOpt.value = "";
    defaultOpt.textContent = "-- Select Category --";
    categorySelect.appendChild(defaultOpt);
}
function populateCategories(typeSelect, categorySelect, categoryOptions, selectedCategory = null) {
    categorySelect.innerHTML = "";
    if (typeSelect.value && categoryOptions[typeSelect.value]) {
        categoryOptions[typeSelect.value].forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat;
            opt.textContent = cat;
            if (cat === selectedCategory) {
                opt.selected = true;
            }
            categorySelect.appendChild(opt);
        });
    } else {
        resetCategory(categorySelect);
    }
}
function initCategorySelector(typeSelectId, categorySelectId, categoryOptions, selectedCategory = null) {
    const typeSelect = document.getElementById(typeSelectId);
    const categorySelect = document.getElementById(categorySelectId);
    // Initial population
    populateCategories(typeSelect, categorySelect, categoryOptions, selectedCategory);
    // Update when Type changes
    typeSelect.addEventListener("change", function() {
        populateCategories(typeSelect, categorySelect, categoryOptions);
    });
}
function enableDatePickerOnClick(inputId) {
    const dateInput = document.getElementById(inputId);
    if (!dateInput) return;
    // Open picker when clicking anywhere in the field
    dateInput.addEventListener("click", function() {
        this.showPicker && this.showPicker(); // modern browsers
    });
    // Also open when focusing via keyboard/tab
    dateInput.addEventListener("focus", function() {
        this.showPicker && this.showPicker();
    });
}
// Single Delete Modal
document.addEventListener('DOMContentLoaded', () => {
  const confirmDeleteModal = document.getElementById('confirmDeleteModal');
  confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const expId = button.getAttribute('data-id');
    const description = button.getAttribute('data-description');
    const amount = button.getAttribute('data-amount');
    // Fill modal content
    document.getElementById('deleteDescription').textContent = description;
    document.getElementById('deleteAmount').textContent = amount;
    // Update confirm button link
    document.getElementById('deleteConfirmBtn').href = `/delete/${expId}`;
  });
});
// Chart.js
document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('typeChart');
  if (!ctx) return; // safeguard if chart not present on some pages
  const typeChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.months,
      datasets: [
        {
          label: 'Savings',
          data: chartData.savings,
          borderColor: 'blue',
          backgroundColor: 'rgba(0, 0, 255, 0.2)',
          fill: true,
          tension: 0.3
        },
        {
          label: 'Spending',
          data: chartData.spending,
          borderColor: 'green',
          backgroundColor: 'rgba(0, 128, 0, 0.2)',
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        datalabels: {
          color: '#7f7f7f',
          align: 'top',
          formatter: function(value, context) {
            const monthIndex = context.dataIndex;
            const savings = chartData.savings[monthIndex];
            const spending = chartData.spending[monthIndex];
            const total = savings + spending;
            if (total === 0) return '';
            const percent = Math.round((value / total) * 100);
            return percent + '%';
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => '₱' + value }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
});
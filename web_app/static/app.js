// static/app.js

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
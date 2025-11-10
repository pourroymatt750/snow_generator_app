const combos = []; // store combos temporarily
function addSubcategoryField() {
  const container = document.getElementById("subcategories-container");

  // wrapper div
  const wrapper = document.createElement("div");
  wrapper.className = "subcategory-wrapper";

  // input
  const input = document.createElement("input");
  input.type = "text";
  input.name = "subcategories[]";
  input.className = "input-box";
  input.placeholder = "Enter subcategory";

  // remove button
  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.className = "btn btn-danger";
  removeBtn.textContent = "Remove";
  removeBtn.onclick = function() {
    container.removeChild(wrapper);
  };

  wrapper.appendChild(input);
  wrapper.appendChild(removeBtn);
  container.appendChild(wrapper);
}

function addCombo(event) {
  event.preventDefault(); // stop form submission

  const category = document.querySelector('input[name="category"]').value.trim();
  const subInputs = document.querySelectorAll('input[name="subcategories[]"]');
  const subcategories = Array.from(subInputs).map(input => input.value.trim()).filter(Boolean);

  if (!category || subcategories.length === 0) {
    alert("Please enter a category and at least one subcategory.");
    return;
  }

  // Save combo locally
  combos.push({ category, subcategories });

  // Update table
  const tbody = document.getElementById("combo-table-body");

  // remove "No categories yet" if it exists
  if (tbody.children.length === 1 && tbody.children[0].cells[0].colSpan === 2) {
    tbody.innerHTML = "";
  }

  const row = document.createElement("tr");
  const catCell = document.createElement("td");
  catCell.textContent = category;

  const subCell = document.createElement("td");
  subCell.textContent = subcategories.join(", ");

  row.appendChild(catCell);
  row.appendChild(subCell);
  tbody.appendChild(row);

  // Reset form inputs
  document.querySelector('input[name="category"]').value = "";
  document.getElementById("subcategories-container").innerHTML = `
    <div class="subcategory-wrapper">
      <input type="text" name="subcategories[]" placeholder="Enter subcategory" class="input-box" required>
    </div>
  `;
}

function submitAll() {
  if (combos.length === 0) {
    alert("No combos to submit.");
    return;
  }

  // Find the form
  const form = document.getElementById("combo-form");

  // Remove any old hidden inputs so we don't duplicate
  const oldHidden = document.querySelector('input[name="all_combos"]');
  if (oldHidden) oldHidden.remove();

  // Create new hidden input
  const hiddenInput = document.createElement("input");
  hiddenInput.type = "hidden";
  hiddenInput.name = "all_combos";
  hiddenInput.value = JSON.stringify(combos);

  // Append to the form
  form.appendChild(hiddenInput);

  // Explicitly set method to POST to avoid fallback
  form.method = "POST";

  // Submit with POST
  form.submit();
}
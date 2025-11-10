// generate_scripts.js
document.getElementById("generate-form").addEventListener("submit", function (e) {
  e.preventDefault(); // stop page reload

  fetch("/generate_scripts/", {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest", // mark as AJAX
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Fill the textareas with the scripts returned
      document.getElementById("category-script-textarea").value =
        data.category_based_on_subcat_script;
      document.getElementById("subcategory-script-textarea").value =
        data.subcat_based_on_category_script;
    })
    .catch((error) => console.error("Error:", error));
});

function copyCode(textareaId, btn) {
  const text = document.getElementById(textareaId).value;
  navigator.clipboard.writeText(text).then(() => {
    btn.innerHTML = "✔️ Copied!";
    btn.style.background = "#28a745";
    setTimeout(() => {
      btn.innerHTML = "📋";
      btn.style.background = "#0078d7";
    }, 1500);
  }).catch(err => {
    console.error("Clipboard failed:", err);
  });
}

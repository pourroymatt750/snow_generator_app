function markDone(button) {
  if (button.classList.contains("done")) {
    // If it's already marked done → uncheck it
    button.innerHTML = "DONE";
    button.classList.remove("done");
  } else {
    // Otherwise → mark as done
    button.innerHTML = "✔";
    button.classList.add("done");
  }
}

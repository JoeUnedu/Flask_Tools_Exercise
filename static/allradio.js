const answerRadioHolder = document.getElementById("answer");

// add event listener to the todo-list div
answerRadioHolder.addEventListener("click", function (e) {
  if (e.target.tagName === "LABEL") {
    // the label was clicked on. Set the checked to true on the
    //control element for the label.
    e.target.control.checked = true;
  }

  document.getElementById("answer").submit();
});

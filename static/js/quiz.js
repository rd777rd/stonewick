/*
 * Scent Memory Quiz -- progressive disclosure enhancement.
 *
 * The server renders every question in one plain form (so the quiz works
 * fully without JavaScript). If JS is available, this script turns it into
 * a step-through experience: one question at a time, with Back/Next
 * controls, keyboard-friendly focus handling, and a small progress label.
 *
 * No framework, no build step -- just the DOM APIs.
 */
(function () {
  var form = document.querySelector("[data-quiz-form]");
  if (!form) return;

  var steps = Array.prototype.slice.call(form.querySelectorAll("[data-quiz-step]"));
  if (steps.length < 2) return; // nothing to paginate

  var nav = form.querySelector("[data-quiz-nav]");
  var backBtn = form.querySelector("[data-quiz-back]");
  var nextBtn = form.querySelector("[data-quiz-next]");
  var submitBtn = form.querySelector("[data-quiz-submit]");
  var progress = document.querySelector("[data-quiz-progress]");

  var current = 0;

  function showStep(index) {
    steps.forEach(function (step, i) {
      step.hidden = i !== index;
    });

    backBtn.hidden = index === 0;
    var isLastStep = index === steps.length - 1;
    nextBtn.hidden = isLastStep;
    submitBtn.hidden = !isLastStep;

    if (progress) {
      progress.hidden = false;
      progress.textContent = "Question " + (index + 1) + " of " + steps.length;
    }

    // Move focus to the new question's heading for keyboard/screen-reader users.
    var legend = steps[index].querySelector("legend");
    if (legend) {
      legend.setAttribute("tabindex", "-1");
      legend.focus();
    }
  }

  function currentStepIsAnswered() {
    var inputs = steps[current].querySelectorAll("input");
    return Array.prototype.some.call(inputs, function (input) {
      return input.checked;
    });
  }

  nextBtn.addEventListener("click", function () {
    if (!currentStepIsAnswered()) {
      steps[current].classList.add("quiz-question-error");
      return;
    }
    steps[current].classList.remove("quiz-question-error");
    if (current < steps.length - 1) {
      current += 1;
      showStep(current);
    }
  });

  backBtn.addEventListener("click", function () {
    if (current > 0) {
      current -= 1;
      showStep(current);
    }
  });

  nav.hidden = false;
  showStep(current);
})();

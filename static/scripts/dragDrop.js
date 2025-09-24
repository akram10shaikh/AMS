const dragDropContainer = document.getElementById("dragDropContainer");
const availableTestsCol = document.getElementById("availableTests");
const selectedTestsCol = document.getElementById("selectedTests");
const MAX_SELECTED_TESTS = 4;

export function createTestCards(headers) {
  dragDropContainer.style.display = "flex";
  availableTestsCol.innerHTML = "<h3>Available Tests</h3>";
  selectedTestsCol.innerHTML = "<h3>Selected Tests</h3>";

  headers.forEach((h) => {
    const card = document.createElement("div");
    card.className = "test-card";
    card.draggable = true;
    card.dataset.header = h;
    card.textContent = h;

    card.addEventListener("click", () => {
      if (card.parentElement === availableTestsCol) {
        tryMoveToSelected(card);
      } else {
        availableTestsCol.appendChild(card);
      }
    });
    availableTestsCol.appendChild(card);
  });
}

function tryMoveToSelected(card) {
  if (selectedTestsCol.querySelectorAll(".test-card").length >= MAX_SELECTED_TESTS) {
    alert(`You can select up to ${MAX_SELECTED_TESTS} tests.`);
    return;
  }
  selectedTestsCol.appendChild(card);
}

export function getSelectedTestHeaders() {
  return [...selectedTestsCol.querySelectorAll(".test-card")].map((c) => c.dataset.header);
}

export function destroyCharts() {} // replaced by uiRenderer
export function clearCanvases() {} // replaced by uiRenderer

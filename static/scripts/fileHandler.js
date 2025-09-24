import { parseCSVText } from "./dataParser.js";
import { populatePlayerDropdown } from "./uiRenderer.js";
import { createTestCards, destroyCharts, clearCanvases } from "./dragDrop.js";

export let playerData = [];
export let headers = [];

export function handleCSVUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (ev) => {
    const text = ev.target.result;
    const parsed = parseCSVText(text);
    headers = parsed.hdr || [];
    playerData = parsed.data || [];

    if (!headers.some((h) => h.toLowerCase() === "player")) {
      alert("CSV does not contain a 'Player' header.");
      return;
    }

    // Reset & update UI
    populatePlayerDropdown(playerData);
    createTestCards(headers);
    destroyCharts();
    clearCanvases();
  };
  reader.readAsText(file);
}

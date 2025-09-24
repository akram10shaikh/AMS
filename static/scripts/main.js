import { handleCSVUpload } from "./fileHandler.js";
import {
  updatePlayerInfo,
  renderChartWithTable,
  destroyCharts
} from "./uiRenderer.js";
import { getSelectedTestHeaders } from "./dragDrop.js";
import { playerData, headers } from "./fileHandler.js";

document.getElementById("uploadCSV").addEventListener("change", handleCSVUpload);
document.getElementById("generateBtn").addEventListener("click", generateReport);

function generateReport() {
  const playerName = document.getElementById("playerSelect").value;
  const selectedHeaders = getSelectedTestHeaders();
  const testCount = parseInt(document.getElementById("testCountSelect").value, 10);

  if (!playerName) { alert("Select player"); return; }
  if (!selectedHeaders.length) { alert("Select at least 1 test"); return; }

  updatePlayerInfo(playerName);
  destroyCharts();

  selectedHeaders.forEach((header, idx) => {
    const rows = playerData.filter(r => r["Player"] === playerName && r[header]);
    rows.sort((a, b) => new Date(a["Date"]) - new Date(b["Date"]));
    const lastRows = rows.slice(-testCount);

    const labels = lastRows.map(r => r["Date"]);
    const values = lastRows.map(r => parseFloat(r[header]) || null);
    const grp = lastRows.map(r => parseFloat(r[`${header} GRP Average`]) || null);
    const indv = lastRows.map(r => parseFloat(r[`${header} INDV Average`]) || null);
    const target = lastRows.map(r => parseFloat(r[`${header} Target`]) || null);

    const datasets = [
      { label: "Value", data: values, backgroundColor: "#3b82f6", borderRadius: 6 },
      { label: "GRP Average", data: grp, type: "line", borderColor: "red", borderDash: [5, 5], fill: false, pointRadius: 0 },
      { label: "INDV Average", data: indv, type: "line", borderColor: "orange", borderDash: [5, 5], fill: false, pointRadius: 0 },
      { label: "Target", data: target, type: "line", borderColor: "green", fill: false, pointRadius: 0 }
    ];

    const tableData = lastRows.map(r => ({
      date: r["Date"] || "-",
      phase: r["Phase"] || "-",
      value: r[header] || "-",
      grp: r[`${header} GRP Average`] || "-",
      indv: r[`${header} INDV Average`] || "-",
      target: r[`${header} Target`] || "-"
    }));

    renderChartWithTable(document.getElementById(`chartCanvas${idx+1}`), labels, datasets, tableData);
  });
}

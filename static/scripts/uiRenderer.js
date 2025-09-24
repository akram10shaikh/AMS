import { headers, playerData } from "./fileHandler.js";

const chartCanvases = [
  document.getElementById("chartCanvas1"),
  document.getElementById("chartCanvas2"),
  document.getElementById("chartCanvas3"),
  document.getElementById("chartCanvas4"),
];
const chartArea = document.getElementById("chartArea");
let chartInstances = [];

export function populatePlayerDropdown(playerData) {
  const playerSelect = document.getElementById("playerSelect");
  playerSelect.innerHTML = '<option value="" disabled selected>-- Select Player --</option>';
  const uniquePlayers = [...new Set(playerData.map((r) => r["Player"]).filter(Boolean))];
  uniquePlayers.forEach((player) => {
    const opt = document.createElement("option");
    opt.value = player;
    opt.textContent = player;
    playerSelect.appendChild(opt);
  });
}

export function updatePlayerInfo(playerName) {
  const row = playerData.find(r => r["Player"] === playerName) || {};
  document.getElementById("playerNameTitle").textContent = row["Player"]?.toUpperCase() || "-";
  document.getElementById("playerName").textContent = row["Player"] || "-";
  document.getElementById("playerGender").textContent = row["Gender"] || "N/A";
  document.getElementById("playerAge").textContent = row["Age Category"] || "N/A";
  document.getElementById("playerHandedness").textContent = row["Handedness"] || "N/A";
  document.getElementById("playerRole").textContent = row["Role"] || "Batsman";
  document.getElementById("coachName").textContent = row["Coach Name"] || "N/A";

  chartArea.style.display = "block";
}

export function renderChartWithTable(canvas, labels, datasets, tableData) {
  const ctx = canvas.getContext("2d");
  const newChart = new Chart(ctx, {
    type: "bar",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: "top", align: "start" }
      }
    }
  });
  chartInstances.push(newChart);

  // --- Append stats table below chart ---
  const table = document.createElement("table");
  table.className = "stats-table";
  table.innerHTML = `
    <thead>
      <tr>
        <th>Date</th>
        <th>Phase</th>
        <th>Value</th>
        <th>GRP Avg</th>
        <th>INDV Avg</th>
        <th>Target</th>
      </tr>
    </thead>
    <tbody>
      ${tableData.map(r => `
        <tr>
          <td>${r.date}</td>
          <td>${r.phase}</td>
          <td>${r.value}</td>
          <td>${r.grp}</td>
          <td>${r.indv}</td>
          <td>${r.target}</td>
        </tr>
      `).join("")}
    </tbody>
  `;
  canvas.parentNode.appendChild(table);
}

export function destroyCharts() {
  chartInstances.forEach(c => c.destroy());
  chartInstances = [];
}

export function clearCanvases() {
  chartCanvases.forEach((canvas) => {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });
}

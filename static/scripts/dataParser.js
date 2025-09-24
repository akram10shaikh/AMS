export function parseCSVText(text) {
  const rows = text.replace(/\r/g, "").split("\n").filter((r) => r.trim() !== "");
  if (rows.length === 0) return { hdr: [], data: [] };

  const headerIdx = rows.findIndex((r) => r.split(",").map((c) => c.trim().toLowerCase()).includes("player"));
  const headerCells = rows[headerIdx === -1 ? 0 : headerIdx].split(",").map((h) => h.trim());

  const dataRows = [];
  for (let i = headerIdx + 1; i < rows.length; i++) {
    const cells = rows[i].split(",");
    if (cells.length <= 1 && !cells[0]?.trim()) continue;
    const obj = {};
    for (let j = 0; j < headerCells.length; j++) {
      obj[headerCells[j]] = cells[j] !== undefined ? cells[j].trim() : "";
    }
    dataRows.push(obj);
  }
  return { hdr: headerCells, data: dataRows };
}

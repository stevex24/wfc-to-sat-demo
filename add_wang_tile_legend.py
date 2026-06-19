from pathlib import Path

p = Path("index.html")
text = p.read_text()
Path("index.html.before-wang-legend").write_text(text)

html_marker = '''<div class="grid-container">'''

legend_html = '''<div class="panel">
  <h2>Wang Tile Legend</h2>
  <p>Border colors are the real Wang-tile edge colors. Adjacent borders must match.</p>
  <div id="tileLegend" class="grid"></div>
</div>

<div class="grid-container">'''

text = text.replace(html_marker, legend_html)

old = '''function renderGrid(grid, elementId) {'''

legend_function = '''function renderTileLegend() {
  const container = document.getElementById("tileLegend");
  container.className = "grid";
  container.style.gridTemplateColumns = "repeat(4, 40px)";
  container.innerHTML = "";

  for (const tileInfo of tileObjects) {
    const cell = document.createElement("div");
    cell.className = `cell tile-${tileInfo.name}`;
    cell.textContent = tileInfo.name;
    cell.title =
      `${tileInfo.name}: ` +
      `N=${tileInfo.north}, E=${tileInfo.east}, ` +
      `S=${tileInfo.south}, W=${tileInfo.west}`;

    cell.style.borderTopColor = tileInfo.north;
    cell.style.borderRightColor = tileInfo.east;
    cell.style.borderBottomColor = tileInfo.south;
    cell.style.borderLeftColor = tileInfo.west;

    container.appendChild(cell);
  }
}

function printAllowedRules() {
  let lines = [];

  lines.push("Right-neighbor rules:");
  for (const t of tiles) {
    lines.push(`${t} -> ${spec.allowed.right[t].join(", ")}`);
  }

  lines.push("");
  lines.push("Down-neighbor rules:");
  for (const t of tiles) {
    lines.push(`${t} -> ${spec.allowed.down[t].join(", ")}`);
  }

  return lines.join("\\n");
}

'''

text = text.replace(old, legend_function + old)

old_output = '''document.getElementById("summaryOutput").textContent =
  `Tiles: ${tiles.join(", ")}\\n` +
  `Variables: ${cnf.numVars}\\n` +
  `Clauses: ${cnf.clauses.length}`;'''

new_output = '''renderTileLegend();

document.getElementById("summaryOutput").textContent =
  `Tiles: ${tiles.join(", ")}\\n` +
  `Variables: ${cnf.numVars}\\n` +
  `Clauses: ${cnf.clauses.length}\\n\\n` +
  printAllowedRules();'''

if old_output not in text:
    raise SystemExit("Could not find summary output block.")

text = text.replace(old_output, new_output)
p.write_text(text)

print("Added Wang tile legend and adjacency rule summary.")
print("Backup saved as index.html.before-wang-legend")

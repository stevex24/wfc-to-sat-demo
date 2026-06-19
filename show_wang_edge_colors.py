from pathlib import Path

p = Path("index.html")
text = p.read_text()
Path("index.html.before-edge-colors").write_text(text)

text = text.replace(
'''.cell {
  width: 40px;
  height: 40px;
  border-radius: 4px;
}''',
'''.cell {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  box-sizing: border-box;
  border-style: solid;
  border-width: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 14px;
  background: #333;
}'''
)

old = '''      cell.className = `cell tile-${tile}`;
      cell.title = tile;

      container.appendChild(cell);'''

new = '''      cell.className = `cell tile-${tile}`;
      cell.textContent = tile;
      cell.title = tile;

      const tileInfo = tileObjects.find(t => t.name === tile);
      if (tileInfo) {
        cell.style.borderTopColor = tileInfo.north;
        cell.style.borderRightColor = tileInfo.east;
        cell.style.borderBottomColor = tileInfo.south;
        cell.style.borderLeftColor = tileInfo.west;
      }

      container.appendChild(cell);'''

if old not in text:
    raise SystemExit("Could not find renderGrid cell block.")

text = text.replace(old, new)
p.write_text(text)

print("Updated Wang tile rendering to show actual edge colors.")
print("Backup saved as index.html.before-edge-colors")

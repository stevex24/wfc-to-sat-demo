from pathlib import Path

path = Path("index.html")
text = path.read_text()
Path("index.html.before-pattern-key-fix").write_text(text)

old = '''function patternKey(pattern) {
  return pattern.map(row => Array.isArray(row) ? row.join("") : String(row)).join("/");
}'''

new = '''function patternKey(pattern) {
  const rows = pattern.rows || pattern;
  return rows.map(row => Array.isArray(row) ? row.join("") : String(row)).join("/");
}'''

if old not in text:
    raise SystemExit("Could not find old patternKey function.")

text = text.replace(old, new)
path.write_text(text)

print("Fixed patternKey to handle pattern.rows")
print("Backup saved as index.html.before-pattern-key-fix")

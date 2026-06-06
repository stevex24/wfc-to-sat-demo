from pathlib import Path

p = Path("index.html")
text = p.read_text()
Path("index.html.before-biased-overlap-sample").write_text(text)

old = '''const sampleTextGrid = [
  "ABABA",
  "BABAB",
  "ABABA",
  "BABAB",
  "ABABA"
];'''

new = '''const sampleTextGrid = [
  "AAAAA",
  "AAAAA",
  "AAAAB",
  "AAAAB",
  "AAAAB"
];'''

if old not in text:
    raise SystemExit("Could not find original sampleTextGrid.")

text = text.replace(old, new)
p.write_text(text)

print("Changed sampleTextGrid to biased overlap test sample.")
print("Backup saved as index.html.before-biased-overlap-sample")

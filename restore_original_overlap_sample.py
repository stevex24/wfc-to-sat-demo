from pathlib import Path

p = Path("index.html")
text = p.read_text()

biased = '''const sampleTextGrid = [
  "AAAAA",
  "AAAAA",
  "AAAAB",
  "AAAAB",
  "AAAAB"
];'''

original = '''const sampleTextGrid = [
  "ABABA",
  "BABAB",
  "ABABA",
  "BABAB",
  "ABABA"
];'''

if biased not in text:
    raise SystemExit("Could not find biased sampleTextGrid.")

text = text.replace(biased, original)
p.write_text(text)

print("Restored original sampleTextGrid.")

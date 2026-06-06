from pathlib import Path
import re

path = Path("index.html")
text = path.read_text()
Path("index.html.before-overlap-weights-2").write_text(text)

old = "const overlappingPatterns = extractOverlappingPatterns(sampleTextGrid, 2);"
new = """const overlappingPatterns = extractOverlappingPatterns(sampleTextGrid, 2);
const overlapPatternFrequencies = countPatternFrequencies(overlappingPatterns);
const overlapPatternWeightsById = new Map(
  overlappingPatterns.map(pattern => [
    pattern.id,
    overlapPatternFrequencies.get(patternKey(pattern)) || 1
  ])
);
console.log("Overlapping pattern frequencies:", overlapPatternFrequencies);"""

if old in text and "const overlapPatternFrequencies" not in text:
    text = text.replace(old, new)
else:
    print("Frequency block already present or target not found.")

old_choice = """const tile = [...domains[best.y][best.x]][Math.floor(Math.random() * domains[best.y][best.x].size)];"""
new_choice = """const tile = weightedRandomChoice(
      [...domains[best.y][best.x]],
      id => overlapPatternWeightsById.get(id) || 1
    );"""

if old_choice in text:
    text = text.replace(old_choice, new_choice)
else:
    print("Random domain choice target not found.")

path.write_text(text)
print("Patched index.html")
print("Backup saved as index.html.before-overlap-weights-2")

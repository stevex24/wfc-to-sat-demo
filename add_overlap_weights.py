from pathlib import Path
import re

path = Path("index.html")
text = path.read_text()

backup = Path("index.html.before-overlap-weights")
backup.write_text(text)

helper_code = r'''
function patternKey(pattern) {
  return pattern.map(row => Array.isArray(row) ? row.join("") : String(row)).join("/");
}

function countPatternFrequencies(patterns) {
  const counts = new Map();

  for (const p of patterns) {
    const key = patternKey(p);
    counts.set(key, (counts.get(key) || 0) + 1);
  }

  return counts;
}

function weightedRandomChoice(items, weightFn) {
  const total = items.reduce((sum, item) => sum + weightFn(item), 0);
  let r = Math.random() * total;

  for (const item of items) {
    r -= weightFn(item);
    if (r <= 0) return item;
  }

  return items[items.length - 1];
}
'''

if "function countPatternFrequencies(patterns)" not in text:
    marker = "function extractOverlappingPatterns"
    if marker not in text:
        raise SystemExit("Could not find extractOverlappingPatterns. Add helpers manually near overlap code.")
    text = text.replace(marker, helper_code + "\n\n" + marker)

# Insert frequency computation after common pattern extraction forms.
patterns = [
    r"(const\s+patterns\s*=\s*extractOverlappingPatterns\([^;]+;\n)",
    r"(let\s+patterns\s*=\s*extractOverlappingPatterns\([^;]+;\n)",
]

inserted = False
for pat in patterns:
    m = re.search(pat, text)
    if m and "countPatternFrequencies(patterns)" not in text[m.end():m.end()+500]:
        insert = (
            m.group(1)
            + "const patternFrequencies = countPatternFrequencies(patterns);\n"
            + 'console.log("Overlapping pattern frequencies:", patternFrequencies);\n'
        )
        text = text[:m.start()] + insert + text[m.end():]
        inserted = True
        break

if not inserted and "const patternFrequencies = countPatternFrequencies(patterns);" not in text:
    print("WARNING: Could not automatically place patternFrequencies after pattern extraction.")

# Replace common uniform random choice forms.
replacements = [
    (
        r"legalPatterns\s*\[\s*Math\.floor\s*\(\s*Math\.random\(\)\s*\*\s*legalPatterns\.length\s*\)\s*\]",
        "weightedRandomChoice(legalPatterns, p => patternFrequencies.get(patternKey(p)) || 1)"
    ),
    (
        r"possiblePatterns\s*\[\s*Math\.floor\s*\(\s*Math\.random\(\)\s*\*\s*possiblePatterns\.length\s*\)\s*\]",
        "weightedRandomChoice(possiblePatterns, p => patternFrequencies.get(patternKey(p)) || 1)"
    ),
    (
        r"patterns\s*\[\s*Math\.floor\s*\(\s*Math\.random\(\)\s*\*\s*patterns\.length\s*\)\s*\]",
        "weightedRandomChoice(patterns, p => patternFrequencies.get(patternKey(p)) || 1)"
    ),
]

changed_choice = False
for old, new in replacements:
    text2, n = re.subn(old, new, text)
    if n:
        changed_choice = True
        text = text2
        print(f"Replaced {n} random choice occurrence(s).")

path.write_text(text)

print("Wrote index.html")
print("Backup saved as index.html.before-overlap-weights")

if not changed_choice:
    print("WARNING: No random choice expression was replaced. Search manually for Math.random.")

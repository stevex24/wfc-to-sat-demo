from pathlib import Path

p = Path("index.html")
text = p.read_text()
Path("index.html.before-entropy-selection").write_text(text)

old = '''  while (true) {
    let best = null;

    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        if (domains[y][x].size > 1) {
          best = { x, y };
        }
      }
    }

    if (!best) break;
'''

new = '''  while (true) {
    let best = null;
    let bestEntropy = Infinity;

    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        const entropy = domains[y][x].size;

        if (entropy > 1 && entropy < bestEntropy) {
          best = { x, y };
          bestEntropy = entropy;
        }
      }
    }

    if (!best) break;

    console.log("Lowest-entropy choice:", {
      x: best.x,
      y: best.y,
      entropy: bestEntropy,
      domain: [...domains[best.y][best.x]]
    });
'''

if old not in text:
    raise SystemExit("Could not find old WFC best-cell selection block.")

text = text.replace(old, new)
p.write_text(text)

print("Added lowest-entropy cell selection.")
print("Backup saved as index.html.before-entropy-selection")

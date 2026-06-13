from pathlib import Path

p = Path("index.html")
text = p.read_text()
Path("index.html.before-overlap-scaling-experiment").write_text(text)

marker = '''function gridToOverlapSatAssignment(patternGrid, cnf, patterns) {'''

insert = '''function runOverlapScalingExperiment(sizes) {
  console.log("=== Overlap scaling experiment ===");
  console.log("size, vars, clauses, encodeMs, backtrackingMs, success");

  for (const size of sizes) {
    let cnf = null;
    let encodeMs = null;
    let backtrackingMs = null;
    let success = true;

    try {
      const encodeStart = performance.now();
      cnf = overlappingPatternsToCnf(
        overlappingPatterns,
        overlapAllowed,
        size,
        size
      );
      encodeMs = performance.now() - encodeStart;

      const backtrackingStart = performance.now();
      solveOverlapBacktracking(
        overlappingPatterns,
        overlapAllowed,
        size,
        size
      );
      backtrackingMs = performance.now() - backtrackingStart;
    } catch (err) {
      success = false;
      console.warn("Overlap scaling failed at size", size, err);
    }

    console.log({
      size: `${size}x${size}`,
      vars: cnf ? cnf.numVars : null,
      clauses: cnf ? cnf.clauses.length : null,
      encodeMs: encodeMs === null ? null : Number(encodeMs.toFixed(3)),
      backtrackingMs: backtrackingMs === null ? null : Number(backtrackingMs.toFixed(3)),
      success
    });
  }
}

runOverlapScalingExperiment([4, 8, 12, 16, 20]);

'''

if insert.strip() in text:
    raise SystemExit("Scaling experiment already inserted.")

if marker not in text:
    raise SystemExit("Could not find insertion marker.")

text = text.replace(marker, insert + marker)
p.write_text(text)

print("Added overlap scaling experiment.")

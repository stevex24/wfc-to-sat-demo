from pathlib import Path
import subprocess
import time
import shutil

SAMPLES = {
    "checkerboard": [
        "ABABA",
        "BABAB",
        "ABABA",
        "BABAB",
        "ABABA",
    ],
    "complex": [
        "ABCDAB",
        "BCADBC",
        "CDABCD",
        "DABCDA",
        "ABCDAB",
        "BCADBC",
    ],
}

SIZES = [4, 8, 12, 16, 20]
PATTERN_SIZE = 2
OUT_DIR = Path("experiments/minisat")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_patterns(grid, n):
    seen = {}
    patterns = []
    h, w = len(grid), len(grid[0])

    for y in range(h - n + 1):
        for x in range(w - n + 1):
            rows = tuple(row[x:x+n] for row in grid[y:y+n])
            if rows not in seen:
                seen[rows] = {"id": len(patterns), "rows": rows, "frequency": 0}
                patterns.append(seen[rows])
            seen[rows]["frequency"] += 1

    return patterns


def overlap_right(a, b):
    return all(row[1:] == other[:-1] for row, other in zip(a["rows"], b["rows"]))


def overlap_down(a, b):
    return a["rows"][1:] == b["rows"][:-1]


def build_allowed(patterns):
    right = {p["id"]: [] for p in patterns}
    down = {p["id"]: [] for p in patterns}

    for a in patterns:
        for b in patterns:
            if overlap_right(a, b):
                right[a["id"]].append(b["id"])
            if overlap_down(a, b):
                down[a["id"]].append(b["id"])

    return {"right": right, "down": down}


def var_for(x, y, p, width, num_patterns):
    return (y * width + x) * num_patterns + p + 1


def encode_cnf(patterns, allowed, width, height):
    p_count = len(patterns)
    clauses = []

    for y in range(height):
        for x in range(width):
            # At least one pattern per cell.
            clauses.append([var_for(x, y, p["id"], width, p_count) for p in patterns])

            # At most one pattern per cell.
            for i in range(p_count):
                for j in range(i + 1, p_count):
                    clauses.append([
                        -var_for(x, y, i, width, p_count),
                        -var_for(x, y, j, width, p_count),
                    ])

    for y in range(height):
        for x in range(width):
            for p1 in patterns:
                p1_id = p1["id"]

                if x + 1 < width:
                    allowed_right = set(allowed["right"][p1_id])
                    for p2 in patterns:
                        if p2["id"] not in allowed_right:
                            clauses.append([
                                -var_for(x, y, p1_id, width, p_count),
                                -var_for(x + 1, y, p2["id"], width, p_count),
                            ])

                if y + 1 < height:
                    allowed_down = set(allowed["down"][p1_id])
                    for p2 in patterns:
                        if p2["id"] not in allowed_down:
                            clauses.append([
                                -var_for(x, y, p1_id, width, p_count),
                                -var_for(x, y + 1, p2["id"], width, p_count),
                            ])

    return width * height * p_count, clauses


def write_dimacs(path, num_vars, clauses):
    with path.open("w") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def run_minisat(cnf_path):
    minisat = shutil.which("minisat")
    if minisat is None:
        raise SystemExit("MiniSat not found. Try: brew install minisat")

    out_path = cnf_path.with_suffix(".out")

    start = time.perf_counter()
    proc = subprocess.run(
        [minisat, str(cnf_path), str(out_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    text = proc.stdout + proc.stderr
    if "UNSATISFIABLE" in text:
        status = "UNSAT"
    elif "SATISFIABLE" in text:
        status = "SAT"
    else:
        status = f"unknown(exit={proc.returncode})"

    return elapsed_ms, status


print("| Sample | Size | Patterns | Vars | Clauses | MiniSat ms | Status |")
print("|---|---:|---:|---:|---:|---:|---|")

for sample_name, grid in SAMPLES.items():
    patterns = extract_patterns(grid, PATTERN_SIZE)
    allowed = build_allowed(patterns)

    for size in SIZES:
        num_vars, clauses = encode_cnf(patterns, allowed, size, size)
        cnf_path = OUT_DIR / f"{sample_name}_{size}x{size}.cnf"
        write_dimacs(cnf_path, num_vars, clauses)

        elapsed_ms, status = run_minisat(cnf_path)

        print(
            f"| {sample_name} | {size}x{size} | {len(patterns)} | "
            f"{num_vars} | {len(clauses)} | {elapsed_ms:.3f} | {status} |"
        )

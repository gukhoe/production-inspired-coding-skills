"""Recheck imported evidence without overwriting source artifacts (stdlib only)."""
import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "verification"
OUT.mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode = True


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe(function, *args):
    try:
        return {"returned": function(*args)}
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}


errors = []
manifest = read_json(ROOT / "sources/manifest.json")
for item in manifest["archives"] + manifest["files"] + manifest.get("supplemental_files", []):
    actual = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
    if actual != item["sha256"]:
        errors.append("Source hash mismatch: " + item["path"])

review_dir = ROOT / "evidence/completeness-review"
review = read_json(review_dir / "COMPLETENESS_REVIEWS.json")
rows = review["records"]
expected = {(f"T{task:02}", repeat, group) for task in range(1, 11)
            for repeat in range(1, 4) for group in "ABC"}
if len(rows) != 90 or len({row["run_id"] for row in rows}) != 90:
    errors.append("Expected 90 unique review rows")
if {(r["task_id"], r["repeat"], r["group"]) for r in rows} != expected:
    errors.append("Unbalanced review rows")
if hashlib.sha256((review_dir / review["rubric"]).read_bytes()).hexdigest() != review["rubric_sha256"]:
    errors.append("Rubric hash mismatch")
summary = {}
features = ("assertion_evidence", "beyond_example_test", "explicit_raise",
            "finite_numeric_check", "stdlib_date_validation")
for group in "ABC":
    group_rows = [r for r in rows if r["group"] == group]
    values = {"n": len(group_rows), "core_pass": sum(r["core"] == "PASS" for r in group_rows),
              "structured_and_reusable": sum(r["S"] == 2 and r["R"] == 2 for r in group_rows)}
    values.update({f: sum(bool(r["observable_features"][f]) for r in group_rows) for f in features})
    values["no_assertion_evidence"] = len(group_rows) - values["assertion_evidence"]
    values["standalone_authored_docs"] = sum(bool(r["observable_features"]["standalone_authored_docs"]) for r in group_rows)
    values["ordinal_label_counts"] = {d: dict(collections.Counter(str(r[d]) for r in group_rows)) for d in "SRETD"}
    summary[group] = values
if summary != read_json(review_dir / "COMPLETENESS_GROUP_SUMMARY.json"):
    errors.append("Group summary differs from individual review records")
with (review_dir / "COMPLETENESS_REVIEWS.csv").open(encoding="utf-8-sig", newline="") as stream:
    csv_rows = list(csv.DictReader(stream))
by_id = {r["run_id"]: r for r in csv_rows}
if len(csv_rows) != 90 or len(by_id) != 90:
    errors.append("Expected 90 unique CSV records")
for row in rows:
    other = by_id.get(row["run_id"], {})
    for key in ("task_id", "group", "repeat", "core", "S", "R", "E", "T", "D"):
        if str(row[key]) != other.get(key):
            errors.append(f"CSV/JSON mismatch: {row['run_id']} {key}")
    for key in features:
        if str(row["observable_features"][key]).lower() != other.get(key, "").lower():
            errors.append(f"CSV/JSON feature mismatch: {row['run_id']} {key}")

# All upstream benchmark code was inspected before this recheck was added.
# Run its writer in a disposable copy, preserving the imported result files.
with tempfile.TemporaryDirectory(prefix="manufacturing-evidence-") as temporary:
    copied = Path(temporary) / "abc"
    shutil.copytree(ROOT / "benchmarks/abc-v1", copied)
    run = subprocess.run([sys.executable, "-B", str(copied / "run_benchmark.py")],
                         capture_output=True, text=True, encoding="utf-8", timeout=30)
    (OUT / "abc.stdout.txt").write_text(run.stdout, encoding="utf-8")
    (OUT / "abc.stderr.txt").write_text(run.stderr, encoding="utf-8")
    if run.returncode:
        errors.append("Original ABC benchmark runner failed")
        rerun = {}
    else:
        rerun = read_json(copied / "results/results.json")
    recorded = read_json(ROOT / "benchmarks/abc-v1/results/results.json")
    for group in "ABC":
        if rerun.get(group, {}).get("tests") != recorded[group]["tests"]:
            errors.append("ABC case outcomes differ: " + group)
    (OUT / "abc-rerun.json").write_text(json.dumps(rerun, indent=2) + "\n", encoding="utf-8")

suite = load_module("review_abc_tests", ROOT / "benchmarks/abc-v1/tests/hidden_tests.py")

def always_raise(quotes, quantity):
    raise ValueError("deliberately broken implementation")

mutant = suite.run(always_raise)
impl_a = load_module("review_abc_a", ROOT / "benchmarks/abc-v1/implementations/a_basic.py")
numeric_quote = {"supplier": "Alpha", "unit_price": 10, "freight": 100, "duty_rate": 0.1, "tooling": 1000}
diagnostics = {
    "description": "Post-hoc diagnostic probes, not a replacement benchmark or new skill-effect experiment.",
    "always_raise_passed": sum(r["pass"] for r in mutant.values()),
    "always_raise_total": len(mutant),
    "always_raise_tests": mutant,
    "a_numeric_valid": observe(impl_a.evaluate, [numeric_quote], 100),
    "a_numeric_zero_quantity": observe(impl_a.evaluate, [numeric_quote], 0),
    "a_numeric_fractional_quantity": observe(impl_a.evaluate, [numeric_quote], 1.5),
    "a_numeric_duplicate_supplier": observe(impl_a.evaluate, [numeric_quote, dict(numeric_quote, supplier="alpha")], 100),
    "recorded_a_actual_failed_tests": [name for name, test in recorded["A"]["tests"].items() if not test["pass"]],
}
(OUT / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8")

sample = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_sample"],
                        cwd=ROOT / "skills/benchmark", capture_output=True, text=True,
                        encoding="utf-8", timeout=30)
(OUT / "sample-tests.stdout.txt").write_text(sample.stdout, encoding="utf-8")
(OUT / "sample-tests.stderr.txt").write_text(sample.stderr, encoding="utf-8")
if sample.returncode:
    errors.append("Original skill sample tests failed")
result = {
    "status": "PASS" if not errors else "FAIL",
    "meaning": "Evidence integrity and outcome reproduction only; not benchmark validity or production readiness.",
    "python": platform.python_version(), "platform": platform.platform(),
    "review_rows": len(rows), "recomputed_summary": summary,
    "abc_pass_counts": {k: v["passed"] for k, v in rerun.items()},
    "always_raise_pass_count": diagnostics["always_raise_passed"],
    "sample_test_exit_code": sample.returncode, "errors": errors,
}
(OUT / "audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k != "recomputed_summary"}, indent=2))
raise SystemExit(bool(errors))

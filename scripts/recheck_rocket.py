"""Rerun the three submitted rocket renderers in temporary copies."""
import ast
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "comparisons/rocket-code"
OUT = BASE / "verification"
OUT.mkdir(exist_ok=True)
results = {}
errors = []
for group in "ABC":
    source = BASE / group
    code = (source / "draw_rocket.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(code)
    checks = source / "verify_output.py"
    with tempfile.TemporaryDirectory(prefix=f"rocket-{group}-") as temporary:
        copied = Path(temporary)
        for p in source.glob("*.py"):
            shutil.copy2(p, copied / p.name)
        process = subprocess.run([sys.executable, "-B", "draw_rocket.py"], cwd=copied,
                                 capture_output=True, text=True, encoding="utf-8", timeout=60)
        # Preserve complete output; replace only the machine-specific temporary root.
        log = f"command: python -B draw_rocket.py\nexit_code: {process.returncode}\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
        check_exit = None
        if checks.exists() and process.returncode == 0:
            checked = subprocess.run([sys.executable, "-B", "verify_output.py"], cwd=copied,
                                     capture_output=True, text=True, encoding="utf-8", timeout=30)
            check_exit = checked.returncode
            log += f"\ncommand: python -B verify_output.py\nexit_code: {check_exit}\nSTDOUT:\n{checked.stdout}\nSTDERR:\n{checked.stderr}"
        (OUT / f"{group}.log").write_text(log.replace(str(copied), "<temporary-copy>"), encoding="utf-8")
        if process.returncode or (check_exit is not None and check_exit):
            errors.append(f"Execution failed: {group}")
        output = copied / "rocket.png"
        with Image.open(output) as im:
            im.verify()
        with Image.open(output) as im:
            im.load()
            dimensions, mode, image_format = list(im.size), im.mode, im.format
        output_hash = hashlib.sha256(output.read_bytes()).hexdigest()
        original_hash = hashlib.sha256((source / "rocket.png").read_bytes()).hexdigest()
        if output_hash != original_hash:
            errors.append(f"Fresh-process image hash differs: {group}")
        results[group] = {
            "render_exit_code": process.returncode,
            "separate_verifier_exit_code": check_exit,
            "render_source_lines": len(code.splitlines()),
            "render_source_bytes": (source / "draw_rocket.py").stat().st_size,
            "separate_verifier_lines": len(checks.read_text(encoding="utf-8-sig").splitlines()) if checks.exists() else 0,
            "function_definitions_including_nested": sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree)),
            "dimensions": dimensions, "mode": mode, "format": image_format,
            "image_bytes": output.stat().st_size, "image_sha256": original_hash,
            "fresh_process_reproduces_original_image": output_hash == original_hash,
            "code_sha256": hashlib.sha256((source / "draw_rocket.py").read_bytes()).hexdigest(),
        }
common_inputs = {}
for name in ("TASK.md", "ADMIN.md"):
    hashes = {g: hashlib.sha256((BASE / g / name).read_bytes()).hexdigest() for g in "ABC"}
    common_inputs[name] = hashes
    if len(set(hashes.values())) != 1:
        errors.append("Unequal common input: " + name)
for p in (BASE / "B/.skills").glob("*/SKILL.md"):
    if p.read_bytes() != (ROOT / "comparators" / p.parent.name / "SKILL.md").read_bytes():
        errors.append("B skill snapshot mismatch")
for p in (BASE / "C/.skills").glob("*/SKILL.md"):
    if p.read_bytes() != (ROOT / "skills" / p.parent.name / "SKILL.md").read_bytes():
        errors.append("C skill snapshot mismatch: " + p.parent.name)
result = {"status": "PASS" if not errors else "FAIL", "python": platform.python_version(),
          "pillow": pillow_version, "groups": results, "common_input_hashes": common_inputs,
          "visual_check": "Coordinator opened all three original PNGs; recognizable rocket, window, fins and flame observed. No automated aesthetic score.",
          "scope": "One fresh-process reproduction of each submission; no new generation, no cross-platform check, no causal claim.",
          "errors": errors}
(OUT / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))

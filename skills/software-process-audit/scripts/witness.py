"""Opt-in local execution recorder. This is not a sandbox or remote attestation."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess  # nosec B404
import time
from datetime import datetime, timezone


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def record(repo, out, revision, command, sources, timeout=60, max_output=4*1024*1024):
    if __package__:
        from .audit import safe_file, AuditError
    else:
        from audit import safe_file, AuditError
    root = Path(repo).resolve()
    if not root.is_dir() or not command or not revision or not 0 < timeout <= 600:
        raise AuditError('Witness needs an existing repo, revision, explicit argv and timeout in (0, 600]')
    if not sources or len(sources) > 500:
        raise AuditError('Witness needs 1..500 source paths to bind the selected input identity')
    selected = [(path, safe_file(root, path)) for path in sources]
    before = {path: sha(file) for path, file in selected}
    output = Path(out).resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    reason = None
    options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {'start_new_session': True}
    with (output/'stdout.log').open('wb') as stdout, (output/'stderr.log').open('wb') as stderr:
        # Argument list is deliberately supplied by the local user; never a shell command or MCP action.
        process = subprocess.Popen(command, cwd=root, stdout=stdout, stderr=stderr, shell=False, **options)  # nosec B603
        deadline = time.monotonic()+timeout
        while process.poll() is None:
            if time.monotonic() >= deadline:
                reason = 'timeout'
            elif sum((output/name).stat().st_size for name in ('stdout.log', 'stderr.log')) > max_output:
                reason = 'output_limit'
            if reason:
                if os.name == 'nt':
                    # Absolute OS utility and internally obtained PID, never project-supplied argv.
                    taskkill = Path(os.environ['SystemRoot'])/'System32'/'taskkill.exe'
                    try:
                        subprocess.run([str(taskkill), '/PID', str(process.pid), '/T', '/F'], capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)  # nosec B603
                    finally:
                        if process.poll() is None:
                            process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                if process.poll() is None:
                    process.kill()
                break
            time.sleep(0.02)
        code = process.wait(timeout=10)
    # A short-lived process can finish between polls; never label oversized logs admissible.
    if reason is None and sum((output/name).stat().st_size for name in ('stdout.log', 'stderr.log')) > max_output:
        reason = 'output_limit'
    after = {path: sha(file) if file.is_file() else None for path, file in selected}
    receipt = {'schema': 'software-audit-witness/1', 'revision': revision, 'command': command, 'cwd': str(root),
               'recorded_at': started, 'completed_at': datetime.now(timezone.utc).isoformat(), 'exit_code': code,
               'termination_reason': reason, 'sources_before': before, 'sources_after': after,
               'logs': {name: sha(output/name) for name in ('stdout.log', 'stderr.log')},
               'trust': 'Local observation only. A writer with access to these files can forge the receipt. No CI attestation or identity signature.'}
    (output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    return receipt


def verify_receipt(root, item, safe_file):
    path = safe_file(root, item['witness_receipt'])
    if path.stat().st_size > 1024*1024:
        raise ValueError('Receipt too large')
    receipt = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(receipt, dict) or receipt.get('schema') != 'software-audit-witness/1' or receipt.get('termination_reason') is not None:
        return False
    if receipt.get('revision') != item.get('revision') or receipt.get('exit_code') != item.get('exit_code'):
        return False
    if json.dumps(receipt.get('command')) != item.get('command') or receipt.get('recorded_at') != item.get('recorded_at'):
        return False
    before, after = receipt.get('sources_before'), receipt.get('sources_after')
    if not isinstance(before, dict) or not before or before != after:
        return False
    if any(sha(safe_file(root, relative)) != value for relative, value in before.items()):
        return False
    evidence_path = safe_file(root, item['path'])
    logs = receipt.get('logs')
    if not isinstance(logs, dict) or evidence_path != path.parent/'stdout.log' or logs.get('stdout.log') != item.get('sha256'):
        return False
    return all(sha(safe_file(root, (path.parent/name).relative_to(root).as_posix())) == logs.get(name)
               for name in ('stdout.log', 'stderr.log'))

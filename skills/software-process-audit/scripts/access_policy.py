"""One file-access policy for every MCP read route; not a content DLP scanner."""
from pathlib import Path, PurePosixPath

SENSITIVE_DIRECTORIES = {'.git', '.ssh', '.aws', '.azure', '.gnupg', '.kube'}
SENSITIVE_NAMES = {'.npmrc', '.pypirc', '.netrc', 'credentials', 'credentials.json', 'id_rsa', 'id_ed25519'}
SENSITIVE_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.keystore'}


def sensitive_path(relative):
    parts = PurePosixPath(str(relative).replace('\\', '/').lower()).parts
    return any(part in SENSITIVE_DIRECTORIES or part in SENSITIVE_NAMES or
               part.startswith('.env') or ':' in part or
               PurePosixPath(part).suffix in SENSITIVE_SUFFIXES for part in parts)


def project_file(root, relative):
    if __package__:
        from .audit import safe_file, AuditError
    else:
        from audit import safe_file, AuditError
    root = Path(root).resolve()
    path = safe_file(root, relative)
    if sensitive_path(relative) or sensitive_path(path.relative_to(root).as_posix()):
        raise AuditError('Access denied by sensitive-file policy')
    # Do not let aliases bypass an inventory exclusion, including in-root symlinks.
    candidate = root / relative
    while candidate != root:
        if candidate.is_symlink():
            raise AuditError('Symlink paths are not exposed by MCP')
        candidate = candidate.parent
    return path

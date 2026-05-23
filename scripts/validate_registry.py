from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_MODULE_FIELDS = {
    "name": str,
    "repo": str,
    "default_branch": str,
    "description": str,
    "compat": list,
    "latest_version": str,
    "module_api": str,
    "tags": list,
}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z_.-]+)?$")


def main() -> int:
    registry = json.loads(Path("modules.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    if registry.get("registry_version") != 1:
        errors.append("registry_version must be 1")

    modules = registry.get("modules")
    if not isinstance(modules, dict) or not modules:
        errors.append("modules must be a non-empty object")
    else:
        for module_id, entry in sorted(modules.items()):
            validate_module(module_id, entry, errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(modules)} modules")
    return 0


def validate_module(module_id: str, entry: object, errors: list[str]) -> None:
    if not isinstance(entry, dict):
        errors.append(f"{module_id}: entry must be an object")
        return

    for field, expected_type in REQUIRED_MODULE_FIELDS.items():
        value = entry.get(field)
        if not isinstance(value, expected_type):
            errors.append(f"{module_id}: {field} must be {expected_type.__name__}")

    repo = entry.get("repo")
    if isinstance(repo, str):
        parsed = urlparse(repo)
        if parsed.scheme not in {"https", "ssh"} and not repo.startswith("git@"):
            errors.append(f"{module_id}: repo should be an https or ssh Git URL")

    version = entry.get("latest_version")
    if isinstance(version, str) and not SEMVER_RE.match(version):
        errors.append(f"{module_id}: latest_version must be semantic version text")

    compat = entry.get("compat")
    if isinstance(compat, list) and not all(isinstance(item, str) and item for item in compat):
        errors.append(f"{module_id}: compat entries must be non-empty strings")

    tags = entry.get("tags")
    if isinstance(tags, list) and not all(isinstance(item, str) and item for item in tags):
        errors.append(f"{module_id}: tags entries must be non-empty strings")


if __name__ == "__main__":
    raise SystemExit(main())

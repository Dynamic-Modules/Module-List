# Dynamic Modules Module List

This repository hosts the default remote registry for Dynamic SS13 Modules.

Use the raw `modules.json` URL from a host repo:

```toml
[[registries]]
name = "dynamic-modules"
url = "https://raw.githubusercontent.com/Dynamic-Modules/Module-List/main/modules.json"
trusted = true
```

Then install listed modules by id:

```bash
dynamic-modules module add dynamic-tgui
dynamic-modules module add contraband-warning
```

The registry is intentionally metadata-only. Each module still owns its source,
manifest, dependencies, config, and versioning policy in its own repository.
Published 1.0 entries include exact commit pins so `dynamic-modules module add`
installs a known-good release snapshot.

## Validation

Before updating the hosted registry, validate the JSON files:

```bash
python3 -m json.tool modules.json
python3 -m json.tool schema.json
python3 scripts/validate_registry.py
```

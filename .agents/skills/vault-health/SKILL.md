---
name: vault-health
description: Check an Obsidian project vault for structural defects such as missing fields, broken links, duplicate tasks, invalid states, and dependency cycles.
---

# Structural health

Read `Agent System/system/vault-model.md` and `Agent System/system/ownership.md` from the vault root. Run `python "Agent System/scripts/vault_tools.py" health` there. Dependencies and command options are documented in `Agent System/scripts/USAGE.md`.

The checker inspects managed content folders, validates record fields, resolves note and `.base` wikilinks, and reports duplicate IDs, possible duplicate task titles, and dependency cycles. It does not evaluate Bases formulas or named views, project success, semantic duplication, attachments, or heading and block anchors. Separate errors from advisory findings and state the scan scope.

Health checks are read-only. Route requested repairs to the skill owning the affected record, or to the architect for schema and implementation changes. After repairs, rerun the check and report remaining findings. Reviews may reference these results without taking ownership of the validation procedure.

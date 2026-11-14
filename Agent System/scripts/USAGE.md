# Vault tools

Run from the vault root with Python 3.8 or newer. Install dependencies if needed with `python -m pip install -r "Agent System/scripts/requirements.txt"`.

```powershell
python "Agent System/scripts/vault_tools.py" health
python -m unittest discover -s "Agent System/tests" -v
```

Health accepts `--root <vault-path>`, prints a Markdown report, and exits 1 for structural errors or 0 for a clean scan or advisory-only findings. Invalid arguments exit 2. It never writes notes. Dashboard generation has been removed; open `Project Management/Dashboards/Overview.md` in Obsidian to use the native Bases views.

Managed scan folders are `Project Management/Projects`, `Project Management/Tasks`, `Project Management/Inbox`, `Project Management/Reviews`, `Project Management/Dashboards`, and `Agent System/Decisions`. Hidden folders, instruction files, and other notes are outside field validation. Note and `.base` link targets may resolve anywhere in the vault except hidden folders; resolution is case-insensitive and supports vault-relative paths and unique basenames. Folder-relative links, Markdown links, attachments, and heading/block or named-view existence are outside the checker's scope. Duplicate task titles are advisory candidates, not proof of duplicate intent.

The scan also validates `Project Management/References` and `Project Management/Decisions`, including reference-input links, producing-task provenance, and project-decision status and targets. Architecture and project decision replacements must remain within their respective note types. Task dependencies remain separate from reference links.

The built-in Bases core plugin renders dashboard and project task views directly from note properties. It is already enabled in this vault. `Project Management/Templates/Project.md` includes the contextual task embed: use a lowercase hyphenated project filename, apply the template, and set its display title as desired. No project records exist yet to migrate. Native views do not require Python. Reopen the missing-next-actions view after source changes if needed because it uses backlinks and cross-file properties.

For behavioral verification, follow `Agent System/system/regression-scenarios.md`. Unit tests exercise the health tools; YAML parsing and embed checks cannot prove Obsidian formula evaluation or rendering. Verify native views in the app with the scenarios before relying on their results.

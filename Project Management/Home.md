# Project management vault

- [[Project Management/Dashboards/Overview|Project overview]] — native Obsidian Bases views of projects, tasks, deadlines, blockers, and missing next actions.
- [[Project Management/Templates/Project|Project template]] — project structure with an embedded task view.
- [[Project Management/Templates/Task|Task template]] — one task with a list of linked projects.
- [[Project Management/Bases/References.base|Reference library]] — reusable findings, requirements, and source information.
- [[Project Management/Bases/Project decisions.base|Project decisions]] — proposed and accepted choices about project execution.
- [[Project Management/Templates/Reference|Reference template]] and [[Project Management/Templates/Project Decision|project decision template]].
- [[Agent System/system/ownership|Responsibility map]] — which role or skill owns each operation.
- [[Agent System/system/vault-model|Vault conventions]] — note fields, states, and editing rules.
- [[Agent System/system/regression-scenarios|Regression scenarios]] — behavior checks for agent changes.
- [[Agent System/Decisions/2026-11-13-vault-capabilities|Architecture decision]] — why the capabilities are divided this way.

## Try these requests

- “Capture this idea in the inbox: …”
- “Suggest how to organize the unprocessed inbox notes.”
- “Process this inbox note into a project and tasks.”
- “Review this project's progress and suggest next actions.”
- “Check the vault for structural problems.”
- “Add a view to the project overview.”
- “Audit the agents and skills for conflicting responsibilities.”

Capture and triage preserve the original text. Project and task skills create the resulting work when requested. Reviews interpret progress; health checks identify structural defects; dashboards summarize source records. Architecture changes are recorded in Decisions.

## Reuse information across tasks

Store reusable findings in `Project Management/References/` using the reference template. Add project links to make them appear in project reference views; add producing tasks to `source_tasks` for provenance. Consuming tasks link the note in their `references` list. Keep one authoritative copy, so completing a research task does not hide its findings. Use `depends_on` separately when later work must wait for that task.

Store execution choices in `Project Management/Decisions/`. Fill in at least one project before using a project decision note; the template starts as a proposal. Agent architecture decisions remain under `Agent System/Decisions/`.

## Run the tools

From this vault's folder:

```powershell
python "Agent System/scripts/vault_tools.py" health
python -m unittest discover -s "Agent System/tests" -v
```

Open the overview in Obsidian; its Bases tables read source note properties without a generation command. Use the project and task templates for new records. Assign a task to one or more projects using its `projects` wikilink list; each project displays the same task. The missing-next-actions view may require reopening after changes because it uses backlinks.

See [[Agent System/scripts/USAGE|Tool usage]] for health-check setup and limitations.

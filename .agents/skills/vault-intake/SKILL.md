---
name: vault-intake
description: Capture rough notes in an Obsidian inbox and classify or process them into projects, tasks, or reusable references, preserving original captures and output links.
---

# Inbox processing

Read `Agent System/system/vault-model.md` and `Agent System/system/ownership.md` from the vault root. Capture requested material in an inbox note using the shared contract. Distinguish the user's text from your interpretation.

For processing, inspect existing outputs and likely matching projects or tasks first. Classify the material as project intent, actionable work, reference material, or unresolved input. Present suggested outcomes when the user asks only for triage or proposals. Create records only when the request authorizes conversion or processing into work.

Delegate project creation to `vault-projects` and task creation to `vault-tasks`. Reuse existing matching records where appropriate. Preserve source text, record resulting links and disposition, and apply the shared processing rules. After partial success, retain links to completed outputs and leave unresolved work unprocessed so a retry can continue without duplicates. Report captured or processed paths and remaining questions.

When the same deliverable serves multiple projects, delegate adding the requested project links to the existing task's list rather than creating one task per project. Record the reused task as an output and retain its other associations.

For material intended as reusable information, delegate authorized conversion to `vault-references` and record the reference output. Triage alone remains a proposal; reference material does not need an invented task to be useful.

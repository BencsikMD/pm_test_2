---
type: decision
date: 2026-11-13
title: Native Bases for project and task views
status: accepted
---
# Native Bases for project and task views

## Context

The user prefers built-in Obsidian Bases for dashboard and project task displays. Python remains welcome for supporting capabilities. This decision replaces the generated dashboard portion of [[Agent System/Decisions/2026-11-13-vault-capabilities]] and carries forward its other ownership assignments.

## Decision and ownership

Use `Project Management/Bases/Projects.base` and `Project Management/Bases/Tasks.base` for native dashboard tables. Use `Project Management/Bases/Project tasks.base` in project notes, matching each task's project property to the embedding note. The dashboard skill owns shared Bases definitions and overview presentation; the project skill owns placing the contextual embed. Task state remains in task-note properties. Keep dashboard commentary in place.

Retire Python dashboard rendering and its command. Keep Python health checks and extend link resolution to `.base` embeds. No project records existed at migration time; provide a project template for future records.

## Alternatives and consequences

Continuing generated Markdown requires regeneration and duplicates display state. A community query plugin adds a dependency the requested native feature avoids. Native Bases reads properties directly and permits row edits. The missing-next-actions formula uses backlinks and cross-file properties; Obsidian documents that these may require reopening a view after changes. Treat that view as advisory. Historical assessments belong in review notes rather than changing live dashboard filters.

## Validation

Check health-tool tests, changed skill structure, Bases YAML, referenced embeds and named views. Verify project filtering, date boundaries, and row edits in Obsidian using `Agent System/system/regression-scenarios.md`. Static validation does not establish native formula evaluation or rendering; in-app behavior remains a manual check.

Completed checks: eight health-tool tests passed; all three changed skills passed structural validation; three Bases definitions parsed as YAML; seven named-view embeds resolved; the vault health scan reported no structural findings. Ownership walkthrough: dashboard changes update shared view definitions, project creation embeds the contextual task view, and task edits update source properties. Historical reviews retain review ownership. No new competing owner was introduced; native rendering and formula behavior have not been tested in the app.

## References

- [Obsidian Bases syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian Bases functions](https://help.obsidian.md/bases/functions)
- [Embedding named views](https://help.obsidian.md/bases/views)

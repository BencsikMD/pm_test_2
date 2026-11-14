---
type: decision
date: 2026-11-13
title: Shared tasks with multiple project links
status: accepted
---
# Shared tasks with multiple project links

## Context and decision

The user authorized multiple project associations per task. Replace the singular task `project` field with optional `projects`, a YAML list of distinct project wikilinks. Keep one task record and one status, owner, due date, dependency set, and set of acceptance criteria for a shared deliverable. Omit the list or use an empty list for unassigned work. Separate deliverables remain separate tasks.

This refines the association rules in [[Agent System/Decisions/2026-11-13-native-bases]] while preserving its native display approach. The task skill owns associations; project views display membership; intake reuses matching tasks; project lifecycle status remains independently owned.

## Implementation and migration

Update contextual task filters, task-table columns, and missing-next-actions membership tests. A shared task appears once in each assigned project and once in the global table. The health checker validates list shape, each target, and duplicate resolved projects; it flags legacy singular fields instead of silently choosing an association. No existing task notes were present to migrate. Future conversions merge legacy links into the canonical list and preserve unrelated data.

## Alternatives and consequences

Duplicating the task per project allows contradictory states for the same deliverable. Keeping a primary project plus related projects adds distinct association semantics the request does not need. A single project list expresses equal membership. Completing a shared task does not automatically complete any linked project. The backlink-based missing-next-actions view retains its documented refresh limitation.

## Validation

Exercise multiple links, unassigned tasks, malformed lists, missing and wrong targets, duplicate aliases, and retired-field detection in the health-tool tests. Parse Bases YAML and verify embeds. In-app shared-task display and row edits remain manual regression scenarios; static tests do not evaluate Obsidian formulas. Ownership walkthroughs cover adding one association without replacing others, retrying intake without duplicating work, and finishing a shared task without changing project states; these are reasoning checks rather than independent agent runs.

Completed verification: all 15 health-tool tests passed, the vault health scan was clean, three modified skills passed structural validation, and three Bases definitions plus their named-view embeds passed static checks. No existing task notes required migration.

## References

- [Obsidian list functions](https://obsidian.md/help/bases/functions)
- [Obsidian Bases links and properties](https://obsidian.md/help/bases/syntax)

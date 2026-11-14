---
type: decision
date: 2026-11-13
title: Separate agent system and project management folders
status: accepted
---
# Separate agent system and project management folders

## Context and decision

The user requested two main folders for visible content, excluding hidden folders and files required at the root. Place agent roles, shared conventions, scripts, tests, and architecture decisions under `Agent System/`. Place Home, dashboards, Bases, templates, and operational records under `Project Management/`.

Keep root `AGENTS.md` as the instruction entry point. Keep `.agents/` and `.obsidian/` in place; skill references are updated for the new locations. Preserve existing decisions, notes, and user content. The existing role and skill ownership boundaries remain unchanged.

## Implementation and alternatives

Update vault-relative wikilinks, skill references, Bases folder filters, health scan folders, typed-link validation, and test fixtures. The health command resolves the vault root from its new script location. Commands quote paths containing spaces. Create Projects, Tasks, Inbox, and Reviews as empty operational folders rather than introducing sample records.

Leaving visible infrastructure at the root would not meet the requested separation. Moving hidden skill and application folders would change their discovery or configuration locations, so they retain their locations.

## Validation

Run the relocated test suite and health checker; check visible root entries, skill references, named-view embeds, Bases folder filters, and internal file links. In-app Bases rendering remains outside static validation.

Completed verification: nine tests passed, all six skills passed structural validation, and the health scan found no structural issues. Static checks confirmed exactly the two main visible folders plus root AGENTS.md, three Bases definitions with updated folder filters, named-view embeds, internal note links, and referenced agent/skill file paths.

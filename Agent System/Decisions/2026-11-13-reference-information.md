---
type: decision
date: 2026-11-13
title: Reusable reference information and project decisions
status: accepted
---
# Reusable reference information and project decisions

## Context and decision

The user approved a structure for project and task reference information that survives completion of its producing task. Store authoritative reusable notes under `Project Management/References/`. Store execution decisions under `Project Management/Decisions/`, separate from this architecture history.

Reference notes use project lists for discovery and source-task lists for provenance. Tasks use reference lists for consumption and keep dependencies separate. Native Bases views display project references and decisions plus task inputs and outputs. Templates provide the structures without fabricated project content.

## Ownership and alternatives

The new reference skill owns reusable information and provenance, a distinct outcome from task state, project scope, reviews, or intake. Existing task and project skills own consumer links and execution decisions respectively. Intake delegates reference filing; dashboard ownership covers shared view presentation. No skill duplicates another's authoritative record procedure.

Copying findings into every task risks divergent information. Keeping findings only in a completed task makes them harder to discover across a project. A standalone linked note preserves one authoritative source and its provenance.

## Validation and limitations

Check reference persistence after producer completion, input/provenance link types, inbox reference outputs, required project-decision associations, and separation of decision replacement targets. Parse Bases YAML and check named-view embeds. Native rendering remains an in-app check. The new regression scenarios define expected agent behavior; ownership walkthroughs are reasoning checks, not independent behavioral runs.

Completed verification: all 20 health-tool tests passed, the vault health scan was clean, and all five new or modified skills passed structural validation. Five Bases definitions and their named-view links passed static checks; both storage folders exist. Ownership walkthroughs retain a single owner for reference content, task inputs, execution decisions, architecture decisions, and view presentation.

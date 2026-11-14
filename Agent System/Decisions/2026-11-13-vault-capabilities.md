---
type: decision
date: 2026-11-13
title: Vault capability ownership
status: superseded
superseded_by: "[[Agent System/Decisions/2026-11-13-native-bases]]"
---

# Vault capability ownership

## Context and decision

The user requested regression scenarios, health checks, decision history, inbox processing, and an evidence-based dashboard. Add three focused skills for intake, structural health, and dashboard generation. Keep architecture decision history and scenario maintenance with the architect.

Intake owns capture and provenance; project and task skills own resulting work. Health owns structural findings; reviews own progress interpretation. Dashboards own derived presentation. The shared vault model remains the data contract.

## Alternatives

Putting every procedure in the project manager would mix coordination and execution. Creating a skill for each supporting document would add routing without a separate operational outcome. These boundaries preserve existing owners.

## Validation and limitations

Mechanical verification uses `Agent System/tests/` and the health command. Agent expectations are in `Agent System/system/regression-scenarios.md`. Reasoning walkthroughs cover project creation, intake retry, review versus health, dashboard refresh, and skill consolidation: each decision has one owner with delegation for adjacent changes. These are not independent agent executions and do not prove absence of semantic overlap.

Initial verification on 2026-11-13: all eight mechanical tests passed, all six skills passed the skill-creator structural validator, dashboard generation succeeded, and the resulting vault health scan reported no structural findings. There are no project or task records yet; meaningful source-data cases were exercised in isolated temporary test vaults.

## Consequences

The overview is a generated snapshot, not a live plugin view. Tooling requires Python and PyYAML. Validation must evolve with the shared model. Captures and source work records remain authoritative.

---
name: vault-tasks
description: Capture, decompose, and update Obsidian task records and their dependencies. Use for actionable work items and task state changes.
---

# Task lifecycle

Read `Agent System/system/vault-model.md` for the data contract and `Agent System/system/ownership.md` for boundaries, resolving paths from the vault root.

Locate the task and its project context before editing. Check for an existing equivalent before creating work. Decompose broad work into independently verifiable outcomes when useful; give each task a clear next action and acceptance criteria proportional to the work.

Preserve user-provided assignments and dates without inferring missing commitments. Validate project and dependency targets. Inspect the reachable dependency chain before adding dependencies to avoid cycles; report missing targets rather than treating them as satisfied.

Use `Project Management/Templates/Task.md` when useful. Follow the shared `projects` list contract even for one association. Reuse one task for the same deliverable across projects and preserve its existing associations when adding another. Distinct deliverables need separate tasks. Flag legacy singular fields and migrate them under the shared contract when a task update includes that conversion.

Apply requested state changes using the shared contract. Flag an unresolved dependency when work is started or completed and preserve an explicit user override with its reason. Do not infer completion from an expired due date or a passing mention.

Return changed task paths, dependency concerns, and remaining ambiguities. Route changes to project scope or status to `vault-projects`.

Maintain the task's input `references` links and preserve its contextual reference views. Delegate reusable findings and output provenance to `vault-references`; link the resulting note so later work can use it after the producing task completes. Follow the shared distinction between information links and scheduling dependencies.

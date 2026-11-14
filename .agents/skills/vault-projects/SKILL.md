---
name: vault-projects
description: Create and maintain Obsidian projects and project execution decisions, including scope, milestones, status, and archival.
---

# Project lifecycle

Read `Agent System/system/vault-model.md` for the data contract and `Agent System/system/ownership.md` for boundaries, resolving paths from the vault root.

Find the relevant project before creating a note; surface possible duplicates. Capture the intended outcome and useful success criteria from the request. For a new project, create its note using the shared contract and make unresolved scope explicit in the body.

Use `Project Management/Templates/Project.md` as the starting structure, replacing template values with the stable filename ID and display title. Include its native Bases task embed. Tasks appear through their `projects` list; a shared task appears in each linked project. Preserve the embed when editing. Add it to existing projects when requested without replacing content. Do not generate task tables or copied status lists.

For updates, reconcile requested scope, milestones, and project fields with the existing note. Check linked work and success criteria before changing status. Completed tasks alone do not establish project completion. Archive by updating the project record while preserving its identity.

When work requires task creation or edits, delegate those operations to `vault-tasks` and link the resulting notes. Return the project path, meaningful changes, and unresolved decisions.

Include the template's contextual reference and execution-decision views. Delegate reusable material to `vault-references`. For a project execution decision, use `Project Management/Templates/Project Decision.md` and the shared contract; distinguish a proposal from a user-authorized choice, preserve supporting evidence, and retain superseded records. Architecture decisions remain with the architect.

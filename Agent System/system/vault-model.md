# Vault model

These are initial local conventions. The architect maintains this contract; project operations follow it. Preserve existing user content and inspect actual notes before applying conventions to an imported vault.

## Storage and identity

Visible vault content is grouped under `Agent System/` and `Project Management/`. Root `AGENTS.md` and hidden directories retain their required locations. Agent definitions, supporting tools, shared conventions, and architecture history belong to Agent System; operational notes and display assets belong to Project Management. All paths below are relative to the vault root.

- `Project Management/Projects/<project-id>.md`: one project per note.
- `Project Management/Tasks/<task-id>.md`: one task per note, linked to zero or more projects.
- `Project Management/Reviews/<YYYY-MM-DD>-<topic>.md`: dated review findings and proposed actions.
- `Project Management/Inbox/<capture-id>.md`: captured material and its processing provenance.
- `Project Management/References/<reference-id>.md`: authoritative reusable findings, requirements, and source material.
- `Project Management/Decisions/<decision-id>.md`: decisions about executing projects.
- `Agent System/Decisions/<YYYY-MM-DD>-<topic>.md`: architecture decision history.
- `Project Management/Dashboards/Overview.md`: maintained dashboard with native Bases embeds.
- `Project Management/Bases/*.base`: shared native Obsidian view definitions.
- `Project Management/Templates/Project.md`: reusable project structure with a contextual task view.
- `Project Management/Templates/Task.md`: reusable task structure with a project-link list.
- `Project Management/Templates/Reference.md` and `Project Management/Templates/Project Decision.md`: reusable knowledge and execution-decision structures.
- Use readable, unique, lowercase hyphenated IDs. Keep IDs and filenames stable when display titles change. Check collisions before creation.
- Use YAML frontmatter for fields and Markdown for narrative. Use quoted Obsidian wikilinks with vault-relative paths and without `.md`, such as `"[[Project Management/Projects/website-refresh]]"`, in frontmatter.
- Store calendar dates as `YYYY-MM-DD`. Omit unknown optional fields; do not manufacture values.

## Projects

Required fields: `type: project`, `id`, `title`, and `status`.

Statuses: `planned`, `active`, `on-hold`, `completed`, `archived`.

Optional fields: `owner`, `due`, `completed`, `archived`.

The body records the desired outcome, scope, success criteria, milestones, and relevant decisions. Link tasks instead of copying their authoritative status into project notes. Mark completion only when the success criteria are satisfied or the user explicitly confirms completion; explain exceptions. Archival preserves the note and links.

New project notes include `![[Project Management/Bases/Project tasks.base#Project tasks]]`. This base selects task records whose `projects` list contains the embedding project file. A mention in a task body alone does not assign it to a project. Open the project note to use this contextual view; the standalone base has no project context. Use `Project Management/Templates/Project.md` as the starting structure, filling its ID with the lowercase hyphenated filename and its title with a readable name. Existing projects retain their content when adding the embed.

Include the contextual References and Project decisions embeds from the project template. Keep brief project context in the body; reusable material belongs in a linked reference rather than copied into each task.

## Tasks

Required fields: `type: task`, `id`, `title`, and `status`.

Statuses: `todo`, `doing`, `blocked`, `done`, `cancelled`.

Optional fields: `projects` (a list of distinct project wikilinks), `owner`, `due`, `completed`, `depends_on` (a list of task wikilinks). Omit `projects` or use `projects: []` for unassigned work. A scalar link or null is invalid; use a list even for one project. The singular `project` field is retired and health checks flag it for migration.

Optional `references` is a list of reference-note wikilinks identifying information the task consumes. It does not impose scheduling dependencies. Use `depends_on` when the task must wait for other work to finish. The task template displays reference inputs and outputs through native Bases embeds.

```yaml
projects:
  - "[[Project Management/Projects/website-refresh]]"
  - "[[Project Management/Projects/product-launch]]"
```

Keep one task record for a shared deliverable, with one status, owner, due date, and set of acceptance criteria. Each linked project displays that same task; global task views show it once. Finishing a shared task does not complete its projects automatically. Use separate dependent tasks when the deliverables or acceptance criteria differ. Preserve unrelated project links when adding or removing one association. When migrating a legacy record, merge its singular link into the list without duplicate targets, remove the retired field, and preserve other fields and body content.

Record acceptance criteria in the body and a reason for blocked or cancelled work. A dependency is satisfied by a `done` task; cancellation does not silently satisfy it. Avoid self-dependencies and cycles. Record completion dates when known; reopening clears the current completion field while preserving useful history in the body.

## References

Required fields: `type: reference`, `id`, and `title`. Optional `projects` and `source_tasks` are lists of distinct project and producing-task wikilinks. Omit these lists or use empty lists when unknown or unassigned. The body contains the reusable information, evidence or source links, and relevant uncertainty. Keep one authoritative note per distinct body of information; link it from consumers instead of copying it. Source-task links record provenance, not dependency or completion.

Reference notes can serve multiple projects independently of the producing task's own associations. Link through `projects` for project-wide discovery and through a task's `references` for explicit consumption. Completing or archiving producing work preserves references. Changes to requirements remain visible in the reference narrative; decisions about accepting or applying them belong in project decisions. Use the reference template and fill its ID and display title as for tasks.

## Project decisions

Required fields: `type: project-decision`, `id`, `title`, `date`, `status`, and `projects` (a nonempty list of distinct project wikilinks). Statuses: `proposed`, `accepted`, `rejected`, `superseded`. Optional `references` lists supporting reference notes; optional `superseded_by` links another project decision. Record context, the choice, rationale, consequences, and evidence in the body. Use `proposed` unless the user has made or authorized the choice; do not manufacture approval. Keep superseded decisions and link their replacement. These execution decisions are separate from architecture records under `Agent System/Decisions/`.

## Reviews

Required fields: `type: review`, `date`, and `scope` (a string describing the reviewed projects or vault area).

Include evidence links, findings, proposed next actions, and any source changes actually made. Distinguish a finding from an approved commitment.

## Inbox

Required fields: `type: inbox`, `id`, `title`, `status` (`unprocessed` or `processed`), and `captured` (calendar date). Optional `outputs` is a list of resulting project, task, or reference wikilinks. Preserve original captured text. Mark processed only after requested classification or delegated creation finishes, recording its disposition and any outputs in the body. A processed item may intentionally produce no work, with a reason. Leave unresolved items unprocessed; check outputs before retrying to avoid duplicate creation.

## Architecture decisions

Required fields: `type: decision`, `date`, `title`, and `status` (`accepted` or `superseded`). Optional `superseded_by` is a decision wikilink. Record context, chosen responsibility boundaries, rationale, alternatives, and validation. Preserve earlier decisions when superseding them.

## Dashboards

The overview is a maintained note marked `type: dashboard`; it needs no snapshot date. Render projects and tasks with native Obsidian Bases embeds. Python may support health checks and other operations, but does not generate dashboards or task listings in project notes. Preserve dashboard commentary and view customizations.

Task views use `todo`, `doing`, and `blocked` as open states. Overdue means a due date earlier than `today()`. Upcoming deadlines span today through today plus seven calendar days inclusive. Show blocked tasks and active projects without an assigned open task. Historical as-of assessments belong in dated reviews.

The missing-next-actions view counts backlinks from task notes, checking membership in their `projects` list and open status rather than incidental mentions. A shared open task counts for each of its linked projects. Obsidian documents that backlink and cross-file property results may require reopening the view after changes. Treat this as advisory and verify underlying tasks before acting. Do not infer project health solely from task counts. Other task and project tables read source properties directly.

## Shared editing rules

Preserve unknown frontmatter fields, narrative, attachments, and unrelated formatting. Treat `.obsidian` settings as outside ordinary project edits. Do not replace user notes with templates. Inspect inbound links before requested renames or moves and update affected references within scope. Report unresolved or ambiguous links. Do not delete notes merely to complete or archive work.

# Responsibility ownership

Each decision or maintained convention has one authoritative owner. Callers may reference it and coordinate operations without duplicating its procedure.

| Responsibility | Owner | Boundary |
| --- | --- | --- |
| Request routing | `AGENTS.md` | Selects roles; does not define skill procedures |
| Agent and skill evolution, consolidation, overlap audits | `Agent System/agents/vault-architect.md` | Changes definitions; content migration is a separate operation |
| Project work coordination | `Agent System/agents/project-manager.md` | Selects and sequences skills |
| Paths, fields, states, links, shared editing rules | `Agent System/system/vault-model.md` | Defines the common data contract |
| Project lifecycle and project fields | `vault-projects` | Owns project notes; delegates task changes |
| Project execution decisions | `vault-projects` | Owns project decision records; architecture decisions remain with the architect |
| Reusable reference information and provenance | `vault-references` | Owns reference notes and their project/source-task associations; consumers own their links |
| Task lifecycle and dependencies | `vault-tasks` | Owns task records; does not infer project status |
| Review findings and review notes | `vault-reviews` | Assesses content; delegates source-record changes |
| Inbox capture, classification, and processing provenance | `vault-intake` | Owns inbox records; delegates project and task creation |
| Structural findings and integrity checks | `vault-health` | Reports data defects; source owners perform requested repairs |
| Dashboard presentation and shared Bases definitions | `vault-dashboard` | Owns overview and Bases view configuration; source fields remain with project and task skills |
| Project task-view embedding | `vault-projects` | Embeds the contextual shared base in project notes; does not copy task states |
| Architecture decision history | `Agent System/agents/vault-architect.md` | Records reasons for definition changes, not project decisions |
| Behavioral regression expectations | `Agent System/system/regression-scenarios.md` | Architect maintains scenarios and evaluates actual outcomes |

`Agent System/scripts/vault_tools.py` implements mechanical health checks. Obsidian Bases renders project and task views directly from note properties. The shared contract remains authoritative; update affected filters, validation, and checks when it changes.

For example, a weekly review may identify a blocked task, ask the task skill to update it when requested, and ask the project skill to revise the project status when warranted. The review owns the finding, while the other skills own their respective edits.

When introducing a capability, update this map and check both adjacent owners. Shared access to a note is acceptable when field and decision ownership remain clear.

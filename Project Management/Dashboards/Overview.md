---
type: dashboard
---
# Project overview

These Obsidian Bases views read project and task note properties directly. Edit a row's properties or open its note to update the underlying record. You can keep commentary here; no script rewrites this dashboard.

## Active projects

![[Project Management/Bases/Projects.base#Active projects]]

## Open tasks

![[Project Management/Bases/Tasks.base#Open tasks]]

## Overdue tasks

![[Project Management/Bases/Tasks.base#Overdue]]

## Deadlines in the next seven days (including today)

![[Project Management/Bases/Tasks.base#Upcoming]]

## Blocked tasks

![[Project Management/Bases/Tasks.base#Blocked]]

## Active projects without next actions

![[Project Management/Bases/Projects.base#Missing next actions]]

This last view uses backlinks to count assigned open tasks. Obsidian may require reopening the view after task links or statuses change. Ordinary task and project tables query source properties directly.

## Browse everything

- [[Project Management/Bases/Projects.base|All project views]]
- [[Project Management/Bases/Tasks.base|All task views]]

Structural integrity checks remain available through `python "Agent System/scripts/vault_tools.py" health`.

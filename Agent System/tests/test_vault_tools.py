import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vault_tools.py"
SPEC = importlib.util.spec_from_file_location("vault_tools", SCRIPT)
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)


class VaultToolsTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)

    def note(self, path, fields, body="Acceptance criteria: verified result."):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"---\n{fields}\n---\n{body}\n", encoding="utf-8")
        return target

    def task(self, identifier, extra="", title=None):
        return self.note(f"Project Management/Tasks/{identifier}.md", f"type: task\nid: {identifier}\ntitle: {title or identifier}\nstatus: todo\n{extra}")

    def test_valid_records_and_read_only_scan(self):
        project = self.note("Project Management/Projects/release.md", "type: project\nid: release\ntitle: Release\nstatus: active")
        task = self.task("ship", 'projects: ["[[Project Management/Projects/release]]"]\ndue: 2026-11-14')
        before = {path: path.read_bytes() for path in (project, task)}
        records, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(len(records), 2)
        self.assertEqual(findings, [])
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_link_errors_and_target_types(self):
        self.note("Project Management/Projects/shared.md", "type: project\nid: shared\ntitle: Shared\nstatus: active")
        self.note("References/shared.md", "type: reference")
        self.task("first", 'projects: ["[[Project Management/Tasks/second]]"]\ndepends_on: ["[[missing]]"]')
        self.task("second")
        self.note("Project Management/Inbox/capture.md", "type: inbox\nid: capture\ntitle: Capture\nstatus: unprocessed\ncaptured: 2026-11-13", "[[shared]]")
        _, findings, _ = TOOLS.scan(self.root)
        messages = "\n".join(message for _, _, message in findings)
        for expected in ("Broken link", "Ambiguous link", "Wrong target type"):
            self.assertIn(expected, messages)

    def test_cycles_and_duplicate_titles(self):
        self.task("first", 'depends_on: ["[[Project Management/Tasks/second]]"]', "Check release")
        self.task("second", 'depends_on: ["[[Project Management/Tasks/first]]"]', "check   release")
        _, findings, _ = TOOLS.scan(self.root)
        self.assertTrue(any(level == "error" and "cycle" in message for level, _, message in findings))
        self.assertTrue(any(level == "warning" and "duplicate task" in message for level, _, message in findings))

    def test_malformed_data_reports_without_crashing(self):
        self.task("bad", 'due: "2026-02-30"\ndepends_on: false\nprojects: []')
        self.note("Project Management/Tasks/broken.md", "type: [unterminated")
        self.note("Project Management/Projects/empty.md", "type: project\nstatus: [active]")
        _, findings, _ = TOOLS.scan(self.root)
        messages = "\n".join(message for _, _, message in findings)
        for expected in ("Cannot parse note", "Missing id", "depends_on must be a list"):
            self.assertIn(expected, messages)

    def test_duplicate_ids(self):
        self.task("shared")
        self.note("Project Management/Projects/shared.md", "type: project\nid: shared\ntitle: Shared\nstatus: planned")
        _, findings, _ = TOOLS.scan(self.root)
        self.assertTrue(any("Duplicate ID" in message for _, _, message in findings))

    def test_reference_outlives_completed_producer_and_can_be_consumed(self):
        self.note("Project Management/Projects/launch.md", "type: project\nid: launch\ntitle: Launch\nstatus: active")
        self.note("Project Management/Tasks/research.md", "type: task\nid: research\ntitle: Research\nstatus: done")
        reference = self.note("Project Management/References/findings.md", 'type: reference\nid: findings\ntitle: Findings\nprojects: ["[[Project Management/Projects/launch]]"]\nsource_tasks: ["[[Project Management/Tasks/research]]"]', "Authoritative findings remain available.")
        consumer = self.task("implement", 'references: ["[[Project Management/References/findings]]"]')
        before = {path: path.read_bytes() for path in (reference, consumer)}
        records, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(findings, [])
        self.assertEqual(sum(record["kind"] == "reference" for record in records), 1)
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_reference_link_types_and_list_shapes(self):
        self.task("producer")
        self.note("Project Management/References/invalid.md", 'type: reference\nid: invalid\ntitle: Invalid\nsource_tasks: ["[[Project Management/References/invalid]]"]')
        self.task("bad-inputs", 'references: ["[[Project Management/Tasks/producer]]"]')
        self.task("scalar-input", 'references: "[[Project Management/References/invalid]]"')
        _, findings, _ = TOOLS.scan(self.root)
        messages = "\n".join(message for _, _, message in findings)
        for expected in ("Wrong target type for source_tasks", "Wrong target type for references", "references must be a list"):
            self.assertIn(expected, messages)

    def test_project_decision_requires_project_and_valid_status(self):
        self.note("Project Management/Decisions/choice.md", "type: project-decision\nid: choice\ntitle: Choice\ndate: 2026-11-13\nstatus: unknown\nprojects: []")
        _, findings, _ = TOOLS.scan(self.root)
        messages = "\n".join(message for _, _, message in findings)
        self.assertIn("Project decisions require at least one project", messages)
        self.assertIn("Invalid status", messages)

    def test_decision_replacements_stay_in_their_own_domain(self):
        self.note("Project Management/Projects/launch.md", "type: project\nid: launch\ntitle: Launch\nstatus: active")
        self.note("Agent System/Decisions/architecture.md", 'type: decision\ntitle: Architecture\ndate: 2026-11-13\nstatus: superseded\nsuperseded_by: "[[Project Management/Decisions/choice]]"')
        self.note("Project Management/Decisions/replacement.md", 'type: project-decision\nid: replacement\ntitle: Replacement\ndate: 2026-11-13\nstatus: accepted\nprojects: ["[[Project Management/Projects/launch]]"]')
        choice = self.note("Project Management/Decisions/choice.md", 'type: project-decision\nid: choice\ntitle: Choice\ndate: 2026-11-13\nstatus: superseded\nprojects: ["[[Project Management/Projects/launch]]"]\nsuperseded_by: "[[Project Management/Decisions/replacement]]"')
        _, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(sum("Wrong target type for superseded_by" in message for _, _, message in findings), 1)
        self.assertFalse(any(path == choice.relative_to(self.root).as_posix() for _, path, _ in findings))

    def test_inbox_can_output_reference_without_creating_work(self):
        self.note("Project Management/References/reading.md", "type: reference\nid: reading\ntitle: Reading")
        self.note("Project Management/Inbox/capture.md", 'type: inbox\nid: capture\ntitle: Capture\nstatus: processed\ncaptured: 2026-11-13\noutputs: ["[[Project Management/References/reading]]"]')
        records, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(findings, [])
        self.assertFalse(any(record["kind"] in {"task", "project"} for record in records))

    def test_shared_task_accepts_multiple_projects_without_copying(self):
        for identifier in ("website", "launch"):
            self.note(f"Project Management/Projects/{identifier}.md", f"type: project\nid: {identifier}\ntitle: {identifier}\nstatus: active")
        task = self.task("shared-work", 'projects: ["[[Project Management/Projects/website]]", "[[Project Management/Projects/launch]]"]')
        before = task.read_bytes()
        records, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(findings, [])
        self.assertEqual(sum(record["kind"] == "task" for record in records), 1)
        self.assertEqual(task.read_bytes(), before)

    def test_unassigned_tasks_allow_absent_or_empty_projects(self):
        self.task("unassigned")
        self.task("empty-list", "projects: []")
        _, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(findings, [])

    def test_projects_rejects_scalar_null_and_non_link_entries(self):
        self.note("Project Management/Projects/website.md", "type: project\nid: website\ntitle: Website\nstatus: active")
        self.task("scalar", 'projects: "[[Project Management/Projects/website]]"')
        self.task("null", "projects: null")
        self.task("invalid-entry", "projects: [17, plain-text]")
        _, findings, _ = TOOLS.scan(self.root)
        messages = [message for _, _, message in findings]
        self.assertEqual(messages.count("projects must be a list"), 2)
        self.assertEqual(messages.count("projects requires wikilinks"), 2)

    def test_projects_rejects_missing_and_wrong_target(self):
        self.task("other-task")
        self.task("invalid-targets", 'projects: ["[[Project Management/Projects/missing]]", "[[Project Management/Tasks/other-task]]"]')
        _, findings, _ = TOOLS.scan(self.root)
        messages = "\n".join(message for _, _, message in findings)
        self.assertIn("Broken link", messages)
        self.assertIn("Wrong target type for projects", messages)

    def test_duplicate_project_aliases_are_rejected(self):
        self.note("Project Management/Projects/website.md", "type: project\nid: website\ntitle: Website\nstatus: active")
        self.task("duplicate-links", 'projects: ["[[Project Management/Projects/website]]", "[[website|Website]]"]')
        _, findings, _ = TOOLS.scan(self.root)
        self.assertTrue(any("Duplicate project target" in message for _, _, message in findings))

    def test_legacy_field_is_reported_without_mutation(self):
        self.note("Project Management/Projects/website.md", "type: project\nid: website\ntitle: Website\nstatus: active")
        task = self.task("legacy", 'project: "[[Project Management/Projects/website]]"\nprojects: ["[[Project Management/Projects/website]]"]')
        before = task.read_bytes()
        _, findings, _ = TOOLS.scan(self.root)
        self.assertTrue(any("Retired project field" in message for _, _, message in findings))
        self.assertEqual(task.read_bytes(), before)

    def test_architecture_decisions_resolve_across_main_folders(self):
        self.note("Agent System/Decisions/previous.md", 'type: decision\ndate: 2026-11-13\ntitle: Previous\nstatus: superseded\nsuperseded_by: "[[Agent System/Decisions/current]]"')
        self.note("Agent System/Decisions/current.md", "type: decision\ndate: 2026-11-13\ntitle: Current\nstatus: accepted")
        self.note("Project Management/Dashboards/Overview.md", "type: dashboard", "[[Agent System/Decisions/current]]")
        records, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(len(records), 3)
        self.assertEqual(findings, [])

    def test_native_base_embeds_resolve_and_missing_bases_report(self):
        base = self.root / "Project Management" / "Bases" / "Tasks.base"
        base.parent.mkdir(parents=True)
        base.write_text("views: []\n", encoding="utf-8")
        self.note("Project Management/Dashboards/Overview.md", "type: dashboard", "![[Project Management/Bases/Tasks.base#Open tasks]]\n![[Tasks.base]]")
        _, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(findings, [])
        base.unlink()
        _, findings, _ = TOOLS.scan(self.root)
        self.assertEqual(sum("Broken link" in message for _, _, message in findings), 2)

    def test_health_preserves_native_dashboard_and_commentary(self):
        target = self.note("Project Management/Dashboards/Overview.md", "type: dashboard", "Manual notes")
        before = target.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "health", "--root", str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(target.read_bytes(), before)

    def test_health_exit_code_and_retired_generator_cannot_write(self):
        self.task("broken", 'depends_on: ["[[Project Management/Tasks/missing]]"]')
        result = subprocess.run([sys.executable, str(SCRIPT), "health", "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Broken link", result.stdout)
        result = subprocess.run([sys.executable, str(SCRIPT), "dashboard", "--root", str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "Project Management" / "Dashboards").exists())


if __name__ == "__main__":
    unittest.main()

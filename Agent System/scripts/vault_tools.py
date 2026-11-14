"""Read managed vault notes and report structural integrity without changing files."""

import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path
import re
import sys

import yaml


FOLDERS = {"Project Management/Projects": "project", "Project Management/Tasks": "task",
           "Project Management/Inbox": "inbox", "Project Management/Reviews": "review",
           "Agent System/Decisions": "decision", "Project Management/Dashboards": "dashboard",
           "Project Management/References": "reference", "Project Management/Decisions": "project-decision"}
REQUIRED = {"project": ("id", "title", "status"), "task": ("id", "title", "status"),
            "inbox": ("id", "title", "status", "captured"),
            "review": ("date", "scope"), "decision": ("date", "title", "status"),
            "dashboard": (), "reference": ("id", "title"),
            "project-decision": ("id", "title", "date", "status", "projects")}
STATES = {"project": {"planned", "active", "on-hold", "completed", "archived"},
          "task": {"todo", "doing", "blocked", "done", "cancelled"},
          "inbox": {"unprocessed", "processed"}, "decision": {"accepted", "superseded"},
          "project-decision": {"proposed", "accepted", "rejected", "superseded"}}
LINK = re.compile(r"\[\[([^\]]+)\]\]")


def calendar_date(value):
    if isinstance(value, date):
        return date.fromisoformat(str(value))
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("expected YYYY-MM-DD")
    return date.fromisoformat(value)


def read_note(path):
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text[match.end():], text


def scan(root):
    records, findings = [], []
    targets = defaultdict(list)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".base"}:
            continue
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        key = relative.with_suffix("").as_posix() if path.suffix.lower() == ".md" else relative.as_posix()
        targets[key.casefold()].append(key)

    def resolve(raw):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if not target:
            return []
        target = target.casefold()
        if target.endswith(".md"):
            target = target[:-3]
        if "/" in target:
            return targets.get(target, [])
        return [key for group in targets.values() for key in group
                if key.rsplit("/", 1)[-1].casefold() == target]

    def issue(level, path, message):
        findings.append((level, path, message))

    identities, titles = defaultdict(list), defaultdict(list)
    for folder, kind in FOLDERS.items():
        for path in sorted((root / folder).rglob("*.md")):
            relative = path.relative_to(root).as_posix()
            if any(part.startswith(".") for part in path.relative_to(root).parts):
                continue
            try:
                data, body, text = read_note(path)
            except (ValueError, yaml.YAMLError, UnicodeError, OSError) as error:
                issue("error", relative, f"Cannot parse note: {error}")
                continue
            record = {"path": relative, "key": relative[:-3], "data": data, "kind": kind}
            records.append(record)
            if data.get("type") != kind:
                issue("error", relative, f"Expected type {kind}")
            for field in REQUIRED[kind]:
                if field not in data or data[field] is None or data[field] == "":
                    issue("error", relative, f"Missing {field}")
            for field in ("id", "title", "status", "scope", "owner"):
                if field in data and not isinstance(data[field], str):
                    issue("error", relative, f"{field} must be a string")
            if kind in STATES and str(data.get("status")) not in STATES[kind]:
                issue("error", relative, "Invalid status")
            identifier = data.get("id")
            if isinstance(identifier, str):
                identities[identifier.casefold()].append(relative)
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
                    issue("error", relative, "ID must be lowercase and hyphenated")
                if identifier != path.stem:
                    issue("error", relative, "ID does not match filename")
            if kind == "task" and isinstance(data.get("title"), str):
                titles[" ".join(data["title"].casefold().split())].append(relative)
            for field in ("due", "completed", "archived", "captured", "date"):
                if field in data:
                    try:
                        calendar_date(data[field])
                    except (ValueError, TypeError):
                        issue("error", relative, f"Invalid {field} date")
            for raw in LINK.findall(text):
                if raw.startswith("#"):
                    continue
                matches = resolve(raw)
                if len(matches) != 1:
                    issue("error", relative, f"{'Ambiguous' if matches else 'Broken'} link: [[{raw}]]")
            if kind == "task" and "project" in data:
                issue("error", relative, "Retired project field: migrate its link into the projects list")
            if kind == "project-decision" and data.get("projects") == []:
                issue("error", relative, "Project decisions require at least one project")
            for field, target_kind, multiple in (("projects", "project", True),
                                                  ("source_tasks", "task", True),
                                                  ("references", "reference", True),
                                                  ("depends_on", "task", True),
                                                  ("outputs", None, True),
                                                  ("superseded_by", "project-decision" if kind == "project-decision" else "decision", False)):
                if field not in data:
                    continue
                values = data[field] if multiple else [data[field]]
                if not isinstance(values, list):
                    issue("error", relative, f"{field} must be a list")
                    continue
                seen_targets = set()
                for value in values:
                    match = LINK.fullmatch(value) if isinstance(value, str) else None
                    if not match:
                        issue("error", relative, f"{field} requires wikilinks")
                        continue
                    matches = resolve(match.group(1))
                    if len(matches) == 1:
                        if field == "projects" and matches[0] in seen_targets:
                            issue("error", relative, "Duplicate project target in projects")
                        elif field in {"references", "source_tasks"} and matches[0] in seen_targets:
                            issue("error", relative, f"Duplicate target in {field}")
                        seen_targets.add(matches[0])
                        expected = {name for name, value in FOLDERS.items()
                                    if value == target_kind} if target_kind else {
                                        "Project Management/Projects", "Project Management/Tasks", "Project Management/References"}
                        if matches[0].endswith(".base") or not any(matches[0].startswith(folder + "/") for folder in expected):
                            issue("error", relative, f"Wrong target type for {field}")
            if kind == "task" and data.get("status") in {"blocked", "cancelled"} and not body.strip():
                issue("warning", relative, "Add a reason in the task body")

    for identifier, paths in identities.items():
        if len(paths) > 1:
            issue("error", ", ".join(paths), f"Duplicate ID: {identifier}")
    for title, paths in titles.items():
        if len(paths) > 1:
            issue("warning", ", ".join(paths), f"Possible duplicate task title: {title}")
    graph = {}
    for record in records:
        if record["kind"] != "task":
            continue
        dependencies = record["data"].get("depends_on", [])
        graph[record["key"]] = []
        for value in dependencies if isinstance(dependencies, list) else []:
            match = LINK.fullmatch(value) if isinstance(value, str) else None
            matches = resolve(match.group(1)) if match else []
            if len(matches) == 1:
                graph[record["key"]].append(matches[0])
    visiting, visited = set(), set()

    def visit(key):
        if key in visiting:
            issue("error", key + ".md", "Dependency cycle")
            return
        if key in visited:
            return
        visiting.add(key)
        for dependency in graph.get(key, []):
            visit(dependency)
        visiting.remove(key)
        visited.add(key)

    for key in graph:
        visit(key)
    return records, findings, resolve


def health_report(findings):
    lines = ["# Vault integrity", "", "Scope: " + ", ".join(FOLDERS) + ".", ""]
    lines.extend(f"- {level.upper()}: {path}: {message}" for level, path, message in findings)
    if not findings:
        lines.append("No structural findings in scanned notes.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("health",))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("Vault root must be an existing directory")
    _, findings, _ = scan(root)
    print(health_report(findings))
    return int(any(level == "error" for level, _, _ in findings))


if __name__ == "__main__":
    sys.exit(main())

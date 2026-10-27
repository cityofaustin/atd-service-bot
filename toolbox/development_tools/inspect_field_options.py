#!/usr/bin/env python3
"""
Print each GitHub issue field on atd-data-tech and its dropdown options.

The listing includes the numeric field id, the field type, and each option's
name and description. Intake stores field ids in config, and stores option
descriptions only for fields it matches by description, such as TPW Divisions.

Run from the repository root:

    python toolbox/development_tools/inspect_field_options.py
"""
import json
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.config import FIELDS

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Option descriptions are included for both select types. Intake matches
# Knack workgroup values to those descriptions.
ISSUE_FIELDS_QUERY = """
{
  repository(owner: "cityofaustin", name: "atd-data-tech") {
    issueFields(first: 25) {
      nodes {
        __typename
        ... on IssueFieldNumber {
          name
          fullDatabaseId
        }
        ... on IssueFieldMultiSelect {
          name
          fullDatabaseId
          options {
            name
            description
          }
        }
        ... on IssueFieldDate {
          name
          fullDatabaseId
        }
        ... on IssueFieldSingleSelect {
          name
          fullDatabaseId
          options {
            name
            description
          }
        }
        ... on IssueFieldText {
          name
          fullDatabaseId
        }
      }
    }
  }
}
"""

TYPE_LABELS = {
    "IssueFieldSingleSelect": "single select",
    "IssueFieldMultiSelect": "multi select",
    "IssueFieldText": "text",
    "IssueFieldNumber": "number",
    "IssueFieldDate": "date",
}

INTAKE_METHOD_NOTES = {
    "map_issue_field_by_description": "Knack values are matched to option descriptions",
    "map_issue_field": "Knack values are mapped to option names in config",
}


def fetch_issue_fields():
    """Load repository issue fields and their dropdown options from GitHub."""
    res = requests.post(
        GITHUB_GRAPHQL_URL,
        headers=GITHUB_HEADERS,
        json={"query": ISSUE_FIELDS_QUERY},
    )
    res.raise_for_status()
    payload = res.json()
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload


def issue_field_nodes(payload):
    nodes = (
        payload.get("data", {})
        .get("repository", {})
        .get("issueFields", {})
        .get("nodes", [])
    )
    return nodes or []


def intake_field_notes():
    """How intake.py uses each issue field it resolves from the GitHub catalog."""
    notes = {}
    for field in FIELDS:
        name = field.get("field_name")
        note = INTAKE_METHOD_NOTES.get(field.get("method"))
        if name and note:
            notes[name] = note
    return notes


def type_label(typename):
    if not typename:
        return "unknown"
    return TYPE_LABELS.get(typename, typename)


def format_description(description):
    lines = str(description).splitlines() or [""]
    formatted = [f"      Description: {lines[0]}"]
    formatted.extend(f"                   {line}" for line in lines[1:])
    return "\n".join(formatted)


def print_issue_field_options(payload):
    """Print each repository issue field, its id, and its dropdown options."""
    notes = intake_field_notes()
    fields = [field for field in issue_field_nodes(payload) if field]
    fields_by_name = {field.get("name"): field for field in fields if field.get("name")}

    print("GitHub issue fields on cityofaustin/atd-data-tech")
    print()
    print("Field id is the number sent when setting that field on an issue.")
    print("For a field matched by description, that description is the Knack text intake must match exactly.")
    print()
    print("Intake currently looks these up from GitHub on every run:")
    if notes:
        for name, note in notes.items():
            if name in fields_by_name:
                print(f"  {name} — {note}")
            else:
                print(f"  {name} — {note} (not found on the repository)")
    else:
        print("  (none)")
    print()

    for field in fields:
        name = field.get("name") or "(unnamed)"
        print(name)
        print(f"  Type: {type_label(field.get('__typename'))}")
        field_id = field.get("fullDatabaseId")
        print(f"  Field id: {field_id if field_id is not None else '(missing)'}")
        note = notes.get(name)
        if note:
            print(f"  Used by intake: {note}")

        options = field.get("options") or []
        if not options:
            print("  (no options)")
            print()
            continue

        print("  Options:")
        for option in options:
            if not option:
                continue
            print(f"    - {option.get('name') or '(unnamed)'}")
            description = option.get("description")
            if description:
                print(format_description(description))
        print()


def main():
    if not GITHUB_ACCESS_TOKEN:
        raise SystemExit("GITHUB_ACCESS_TOKEN is not set.")
    print_issue_field_options(fetch_issue_fields())


if __name__ == "__main__":
    main()

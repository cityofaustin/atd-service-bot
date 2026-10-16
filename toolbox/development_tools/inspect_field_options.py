#!/usr/bin/env python3
"""
Print each GitHub issue field on atd-data-tech and its dropdown options.

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

from config.queries import ISSUE_FIELDS_QUERY

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
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


def print_issue_field_options(payload):
    """Print each repository issue field and its dropdown options."""
    for field in issue_field_nodes(payload):
        if not field:
            continue
        name = field.get("name") or "(unnamed)"
        typename = field.get("__typename", "unknown")
        print(f"{name} [{typename}]")
        options = field.get("options") or []
        if not options:
            print("  (no options)")
            continue
        for option in options:
            option_name = option.get("name")
            option_id = option.get("id")
            print(f"  - {option_name} ({option_id})")
        print()


def main():
    print_issue_field_options(fetch_issue_fields())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Intake.py — Create github issues from service requests received via the the knack-based
DTS portal.

Before you modify this app! Be aware that successful processing is contingent on
coded values in the Knack app, as well as our label definitions on github.

You must update `config/config.py` if you change any of these in the DTS Knack app:
- Workgroup names
- Any pre-defined choice-list options (impact, need, application, workgroup, etc)

...or if you change any of these things on github:
- repo names
- labels
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import knackpy
import requests

from config.config import KNACK_APP, FIELDS
import _transforms

KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME = os.getenv(
    "KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME"
)
KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD = os.getenv(
    "KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD"
)
KNACK_API_KEY = os.getenv("KNACK_API_KEY")
KNACK_APP_ID = os.getenv("KNACK_APP_ID")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
REPO = "atd-data-tech"

CAPTURE_DIR = Path("captures")
CAPTURE_SUFFIX = "_knack_payload.json"

GITHUB_URL = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
# Organization issue type (Settings > Planning > Issue types), not a custom issue field.
ISSUE_TYPE = "Task"
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

ISSUE_FIELDS_QUERY = """
{
  repository(owner: "cityofaustin", name: "atd-data-tech") {
    issueFields(first: 25) {
      nodes {
        __typename
        ... on IssueFieldNumber {
          name
          description
          dataType
          id
          fullDatabaseId
        }
        ... on IssueFieldMultiSelect {
          description
          name
          id
          fullDatabaseId
          options {
            id
            name
            databaseId
            fullDatabaseId
            description
          }
        }
        ... on IssueFieldDate {
          description
          id
          name
          fullDatabaseId
        }
        ... on IssueFieldSingleSelect {
          id
          description
          name
          fullDatabaseId
          options {
            id
            name
            databaseId
            fullDatabaseId
          }
        }
        ... on IssueFieldText {
          name
          id
          description
          fullDatabaseId
        }
      }
    }
  }
}
"""


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

    # print("--- raw issue fields response ---")
    # print(json.dumps(payload, indent=2))


def blockquote(text):
    lines = str(text).splitlines()
    if not lines:
        return ">"
    return "\n".join(f"> {line}" if line else ">" for line in lines)


def map_issue(issue, fields):
    github_issue = {
        "description": "",
        "labels": [],
        "title": "",
        "assignee": [],
        "github_url": None,
        "knack_id": None,
        "repo": REPO,  # hardcoded since we switched to a monorepo
        "issue_fields": {},
    }

    for field in fields:
        """Formatting and placement of Knack issue text is driven by
        config/config.py
        """
        knack_field_id = field["knack"]
        knack_field_label = issue.fields[knack_field_id].name
        knack_field_value = issue.fields[knack_field_id].formatted

        if not knack_field_value:
            continue

        if field["method"] == "merge":
            old_value = github_issue[field["github"]]

            value = knack_field_value

            if field.get("rename"):
                knack_field_label = field.get("rename")

            if field.get("format") == "quote_text":
                label = f"### {knack_field_label}\n\n"
                value = f"{blockquote(value)}\n\n"

                new_value = f"{old_value}{label}{value}"

            elif field.get("format") == "quote_text_hidden":
                label = f"<!-- {knack_field_label} -->\n"
                value = f"<!-- {value} -->\n\n"

                new_value = f"{label}{value}{old_value}"

            else:
                new_value = (
                    f"{old_value}### {knack_field_label}\n\n{blockquote(value)}\n\n"
                )

            github_issue[field["github"]] = new_value

        elif field["method"] == "transform_merge":
            untransformed = issue[knack_field_id]

            # get the transform function
            transform_func = getattr(_transforms, field["transform"])
            if field.get("transform") == "knack_issue_url":
                transformed_value = transform_func(
                    untransformed, issue.get("field_388") # Request ID
                )
            else:
                transformed_value = transform_func(untransformed)

            # now merge
            old_value = github_issue[field["github"]]

            if field.get("rename"):
                knack_field_label = field.get("rename")

            # Use special header name if sensitive information is available in Knack
            if field.get("transform") == "knack_issue_url" and issue.get(
                "field_1134" # boolean for if additional details are available in Knack
            ) in (1, "1"):
                knack_field_label = "Additional Details available in Knack"

            if field.get("format") == "no_label":
                new_value = f"{old_value}{transformed_value}\n\n"

            elif field.get("format") == "quote_text":
                label = f"### {knack_field_label}\n\n"

                value = f"{blockquote(transformed_value)}\n\n"

                new_value = f"{old_value}{label}{value}"

            else:
                new_value = (
                    f"{old_value}### {knack_field_label}\n\n"
                    f"{blockquote(transformed_value)}\n\n"
                )

            github_issue[field["github"]] = new_value

        elif field["method"] == "map_issue_field":
            option_name = field["map"].get(knack_field_value)
            if not option_name:
                raise RuntimeError(
                    f"No {field['field_name']} option for Knack value {knack_field_value!r}"
                )
            github_issue[field["github"]][field["field_name"]] = option_name

        elif field["method"] == "map_append":
            val_mapped = field["map"].get(knack_field_value)

            if val_mapped:
                github_issue[field["github"]].append(val_mapped)

        elif field["method"] == "map_append_all":
            vals_mapped = field["map"].get(knack_field_value)

            if vals_mapped:
                for val_mapped in vals_mapped:
                    github_issue[field["github"]].append(val_mapped)

        elif field["method"] == "copy":
            github_issue[field["github"]] = knack_field_value

        elif field["method"] == "split_append":
            for val in knack_field_value.split(","):
                val = val.strip()
                if val:
                    github_issue[field["github"]].append(val)

        elif field["method"] == "append":
            github_issue[field["github"]].append(knack_field_value)

    return github_issue


def format_title(issue):
    # Format is: `([Urgent?]) [Truncated Title]...`

    urgent = ""

    if len(issue["title"]) > 100:
        issue["title"] = issue["title"][0:100] + "..."

    if any("severe" in label.lower() for label in issue["labels"]):
        # we want to include "Urgent" in the title for "Impact: Severe" issues
        urgent = "[URGENT] "

    issue["title"] = f"{urgent}{issue['title']}"

    return issue


def create_github_issue(github_payload):
    logging.info("Creating issue")
    res = requests.post(GITHUB_URL, headers=GITHUB_HEADERS, json=github_payload)
    res.raise_for_status()
    return res.json()


def single_select_field_assignment(issue_fields, field_name, option_name):
    """Resolve a single-select issue field to the REST field id and option name."""
    field = next(
        (
            node
            for node in issue_field_nodes(issue_fields)
            if node and node.get("name") == field_name
        ),
        None,
    )
    if not field:
        raise RuntimeError(f"GitHub issue field {field_name!r} was not found")

    option_names = {
        option.get("name") for option in (field.get("options") or []) if option
    }
    if option_name not in option_names:
        raise RuntimeError(
            f"GitHub issue field {field_name!r} has no option {option_name!r}"
        )

    return {"field_id": int(field["fullDatabaseId"]), "value": option_name}


def add_issue_field_values(issue_number, field_values):
    """Add organization issue field values without replacing fields already set."""
    headers = {**GITHUB_HEADERS, "X-GitHub-Api-Version": "2026-03-10"}
    res = requests.post(
        f"{GITHUB_URL}/{issue_number}/issue-field-values",
        headers=headers,
        json={"issue_field_values": field_values},
    )
    res.raise_for_status()
    return res.json()


def get_token(email, pw, app_id):
    # get knack app token for forms api
    data = {"email": email, "password": pw}
    url = f"https://api.knack.com/v1/applications/{app_id}/session"
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()["session"]["user"]["token"]


def form_submit(token, app_id, scene, view, payload):
    record_id = payload["id"]
    url = f"https://api.knack.com/v1/pages/{scene}/views/{view}/records/{record_id}"
    headers = {"X-Knack-Application-Id": app_id, "Authorization": token}
    res = requests.put(url, headers=headers, json=payload)

    try:
        res.raise_for_status()

    except:
        # merge request response error w/ payload so that we can track down the bad record
        raise Exception(
            f"Knack Form Submit error for payload {payload}. Error: {res.text}"
        )

    return res


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Create GitHub issues from Knack DTS portal service requests."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--capture",
        action="store_true",
        help="Write records queried from Knack to ./captures/<timestamp>_knack_payload.json, print them, then exit.",
    )
    mode.add_argument(
        "--use-capture",
        action="store_true",
        help="Process the latest ./captures/*_knack_payload.json instead of querying Knack records.",
    )
    parser.add_argument(
        "--no-send-to-github",
        action="store_true",
        help="Print prepared issues instead of creating GitHub issues or updating Knack.",
    )
    parser.add_argument(
        "--inspect-field-options",
        action="store_true",
        help="Print each GitHub issue field and its options, then exit.",
    )
    return parser.parse_args(argv)


def write_knack_capture(issues):
    payload = [issue.data for issue in issues]
    text = json.dumps(payload, indent=2) + "\n"
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    path = CAPTURE_DIR / f"{datetime.now().strftime('%Y%m%dT%H%M%S')}{CAPTURE_SUFFIX}"
    path.write_text(text)
    print(text, end="")
    print(f"Wrote {path}")
    return path


def latest_capture_path():
    paths = sorted(CAPTURE_DIR.glob(f"*{CAPTURE_SUFFIX}"))
    if not paths:
        raise SystemExit(f"No Knack captures found in {CAPTURE_DIR}/")
    return paths[-1]


def records_from_capture(app, view, payload):
    """Build knackpy records from a saved payload, skipping the view query."""
    container = app._find_container(view)
    container_key = container.obj or container.view
    app.data[container_key] = payload
    return app._records(container_key)


def load_latest_capture(app, view):
    path = latest_capture_path()
    logging.info(f"Using capture {path}")
    payload = json.loads(path.read_text())
    return records_from_capture(app, view, payload)


def main(
    capture=False,
    use_capture=False,
    no_send_to_github=False,
    inspect_field_options=False,
):
    issue_fields = fetch_issue_fields()

    if inspect_field_options:
        print_issue_field_options(issue_fields)
        return 0

    if not capture:
        logging.info("Starting...")
    view = KNACK_APP["api_view"]["view"]
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)

    if use_capture:
        issues = load_latest_capture(app, view)
    else:
        issues = app.get(view)

    if capture:
        write_knack_capture(issues)
        return 0

    if not issues:
        logging.info("No issues to process.")
        return 0

    prepared = []

    for issue in issues:
        # turn knack issues into github issues
        github_issue = map_issue(issue, FIELDS)
        github_issue = format_title(github_issue)
        if not github_issue["assignee"]:
            # fallback when field_1122 is empty; on issue creation an email will
            # be sent to the transportation.data inbox, to be handled by the service desk
            github_issue["assignee"] = ["atdservicebot"]
        prepared.append(github_issue)

    if no_send_to_github:
        print(json.dumps(prepared, indent=2))
        logging.info(f"{len(prepared)} issues prepared; not sent to GitHub.")
        return 0

    token = get_token(
        KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME,
        KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD,
        KNACK_APP_ID,
    )

    responses = []

    for issue in prepared:
        logging.info(issue)

        github_payload = {
            "title": issue["title"],
            "labels": issue.get("labels"),
            "assignees": issue.get("assignee"),
            "body": issue["description"],
            "type": ISSUE_TYPE,
        }
        result = create_github_issue(github_payload)

        field_values = [
            single_select_field_assignment(issue_fields, field_name, option_name)
            for field_name, option_name in issue.get("issue_fields", {}).items()
        ]
        if field_values:
            add_issue_field_values(result["number"], field_values)

        knack_payload = {
            "id": issue["knack_id"],
            "field_394": result.get("number"),  # github issue number
            "field_395": issue["repo"],  # repo
            "field_1125": "SENT",  # knack triage status
        }

        # update knack record as "Sent" using form API, which will
        # trigger an email notification if warranted
        response = form_submit(
            token,
            KNACK_APP_ID,
            KNACK_APP["api_form"]["scene"],
            KNACK_APP["api_form"]["view"],
            knack_payload,
        )

        responses.append(response)

    logging.info(f"{len(responses)} issues processed.")


if __name__ == "__main__":
    # airflow needs this to see logs from the DockerOperator
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    args = parse_args()
    main(
        capture=args.capture,
        use_capture=args.use_capture,
        no_send_to_github=args.no_send_to_github,
        inspect_field_options=args.inspect_field_options,
    )

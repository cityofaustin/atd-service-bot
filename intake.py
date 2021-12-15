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
import logging
import os
import sys

from github import Github
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


def map_issue(issue, fields):

    github_issue = {
        "description": "",
        "labels": [],
        "title": "",
        "github_url": None,
        "knack_id": None,
        "repo": REPO,  # hardcoded since we switched to a monorepo
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

            value = issue[knack_field_id]

            if field.get("format") == "quote_text":
                label = f"> {knack_field_label}\n\n"
                value = f"{value}\n\n"

                new_value = f"{old_value}{label}{value}"

            elif field.get("format") == "quote_text_hidden":
                label = f"<!-- {knack_field_label} -->\n"
                value = f"<!-- {value} -->\n\n"

                new_value = f"{label}{value}{old_value}"

            else:
                new_value = f"{old_value}{knack_field_label}: {value}\n\n"

            github_issue[field["github"]] = new_value

        elif field["method"] == "transform_merge":

            untransformed = issue[knack_field_id]

            # get the transform function
            transform_func = getattr(_transforms, field["transform"])
            transformed_value = transform_func(untransformed)

            # now merge
            old_value = github_issue[field["github"]]

            if field.get("rename"):

                knack_field_label = field.get("rename")

            if field.get("format") == "no_label":
                new_value = f"{old_value}{transformed_value}\n\n"

            elif field.get("format") == "quote_text":
                label = f"> {knack_field_label}\n"

                value = f"{transformed_value}\n\n"

                new_value = f"{old_value}{label}{value}"

            else:
                new_value = f"{old_value}{knack_field_label}: {transformed_value}\n\n"

            github_issue[field["github"]] = new_value

        elif field["method"] == "map_append":

            val_mapped = field["map"].get(knack_field_value)

            if val_mapped:
                github_issue[field["github"]].append(val_mapped)

        elif field["method"] == "copy":
            github_issue[field["github"]] = knack_field_value

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


def get_repo(g, repo, org="cityofaustin"):
    return g.get_repo(f"{org}/{repo}")


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


def main():
    logging.info("Starting...")
    view = KNACK_APP["api_view"]["view"]
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)

    issues = app.get(view)

    if not issues:
        logging.info("No issues to process.")
        return 0

    prepared = []

    for issue in issues:
        # turn knack issues into github issues
        github_issue = map_issue(issue, FIELDS)
        github_issue = format_title(github_issue)
        # all issues are assigned to the service bot. on issue creation an email will
        # be sent to the transportation.data inbox, to be handled by the service desk
        github_issue["assignee"] = ["atdservicebot"]
        prepared.append(github_issue)

    g = Github(GITHUB_ACCESS_TOKEN)
    repo = get_repo(g, REPO)

    token = get_token(
        KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME,
        KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD,
        KNACK_APP_ID,
    )

    responses = []

    for issue in prepared:
        result = repo.create_issue(
            title=issue["title"],
            labels=issue.get("labels"),
            assignees=issue.get("assignee"),
            body=issue["description"],
        )

        knack_payload = {
            "id": issue["knack_id"],
            "field_394": result.number,  # github issue number
            "field_395": issue["repo"],  # repo
            "field_392": "Sent",  # github transmission status
        }

        # update knack record as "Sent" using form API, which will
        # trigger an email notificaiton if warranted
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
    main()

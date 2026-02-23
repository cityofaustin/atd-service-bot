#!/usr/bin/env python3
"""
Fetch Github issues and publish to open data portal
"""
import datetime
import logging
import os
import sys
import re

from github import Github
import sodapy

REPO = {"id": 140626918, "name": "cityofaustin/atd-data-tech"}
WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
SOCRATA_RESOURCE_ID = os.environ["SOCRATA_RESOURCE_ID"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
SOCRATA_ENDPOINT = os.environ["SOCRATA_ENDPOINT"]
SOCRATA_API_KEY_ID = os.environ["SOCRATA_API_KEY_ID"]
SOCRATA_API_KEY_SECRET = os.environ["SOCRATA_API_KEY_SECRET"]
SOCRATA_APP_TOKEN = os.environ["SOCRATA_APP_TOKEN"]


def extract_workgroups_from_labels(labels):
    """Extract a comma-separated list of workgroup names from "Workgroup: Xyz" labels"""
    workgroup_labels = list(
        set([label.name for label in labels if label.name.startswith("Workgroup:")])
    )
    workgroup_labels_no_prefix = [
        label.replace("Workgroup:", "").strip() for label in workgroup_labels
    ]
    return ", ".join(workgroup_labels_no_prefix) or None


def has_child_issues(issue_raw_data):
    """Return True if total in sub_issues_summary from issue_raw_data is greater than 0 """
    subissue_summary = issue_raw_data.get("sub_issues_summary")
    if subissue_summary and subissue_summary["total"] > 0:
        return True
    return False


def get_github_issues(repo_name, github_access_token, state="all"):
    g = Github(github_access_token)
    repo = g.get_repo(repo_name)
    issues_metadata = repo.get_issues(state=state)
    return [issue for issue in issues_metadata]


def remove_html_comments(text):
    if not isinstance(text, str):
        return text  # Return as-is if not a string
    # Remove HTML comments using regular expression
    return re.sub(r"<!--(.*?)-->", "", text, flags=re.DOTALL)


def issue_to_dict(issue):
    """breakdown pygithub classes into dicts"""
    issue_dict = {}

    issue_dict["workgroups"] = extract_workgroups_from_labels(issue.labels)

    issue_dict["labels"] = ", ".join([label.name for label in issue.labels])

    issue_dict["assignee_ids"] = ", ".join([str(user.id) for user in issue.assignees])

    issue_dict["milestone"] = (
        None if not getattr(issue, "milestone") else issue.milestone.title
    )

    issue_dict["has_child_issues"] = has_child_issues(issue.raw_data)

    for attr in [
        "title",
        "body",
        "closed_at",
        "created_at",
        "updated_at",
        "state",
        "number",
        "id",
        "url",
    ]:
        issue_dict[attr] = getattr(issue, attr)

    # Preprocess issue description using the new function
    issue_dict["body"] = remove_html_comments(issue_dict["body"])

    # temporary placeholder for estimate
    issue_dict["estimate"] = None

    # set pipeline for closed issues, otherwise temporarily set as none
    issue_dict["pipeline"] = (
            "Closed" if issue_dict["state"] == "closed" else None
        )
    return issue_dict


def convert_timestamps(issues):
    for issue in issues:
        for key, val in issue.items():
            if isinstance(val, datetime.datetime):
                issue[key] = val.isoformat()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main():
    logging.info("Fetching github issues...")
    issues_gh = get_github_issues(REPO["name"], GITHUB_ACCESS_TOKEN)
    issues = [issue_to_dict(issue) for issue in issues_gh]

    logging.info("Converting timestamps...")
    convert_timestamps(issues)

    client = sodapy.Socrata(
        SOCRATA_ENDPOINT,
        SOCRATA_APP_TOKEN,
        username=SOCRATA_API_KEY_ID,
        password=SOCRATA_API_KEY_SECRET,
        timeout=60,
    )

    logging.info(f"Uploading to Socrata...")
    first_chunk = True
    count_processed = 0
    for chunk in chunks(issues, 1000):
        if first_chunk:
            # completely replace dataset to ensure deleted issues are flushed
            client.replace(SOCRATA_RESOURCE_ID, issues)
            first_chunk = False
        client.upsert(SOCRATA_RESOURCE_ID, issues)
        count_processed += len(chunk)
        logging.info(f"{count_processed} processed of {len(issues)}")
    logging.info(f"Done uploading issues to Socrata")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

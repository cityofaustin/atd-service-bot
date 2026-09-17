#!/usr/bin/env python3
"""
Fetch Github issues and publish them to open data portal
"""
from datetime import datetime
import logging
import os
import sys
import argparse
import requests
import sodapy

from utils.utils import remove_html_comments
from config.config import ISSUE_FIELDS_MAPPING

REPO = {"id": 140626918, "name": "cityofaustin/atd-data-tech"}
SOCRATA_RESOURCE_ID = os.environ["SOCRATA_RESOURCE_ID"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
SOCRATA_ENDPOINT = os.environ["SOCRATA_ENDPOINT"]
SOCRATA_API_KEY_ID = os.environ["SOCRATA_API_KEY_ID"]
SOCRATA_API_KEY_SECRET = os.environ["SOCRATA_API_KEY_SECRET"]
SOCRATA_APP_TOKEN = os.environ["SOCRATA_APP_TOKEN"]
GITHUB_ENDPOINT = "https://api.github.com/graphql"


def extract_workgroups_from_labels(labels):
    """Extract a comma-separated list of workgroup names from "Workgroup: Xyz" labels"""
    workgroup_labels = list(
        set(
            [
                label.get("name")
                for label in labels
                if label.get("name").startswith("Workgroup:")
            ]
        )
    )
    workgroup_labels_no_prefix = [
        label.replace("Workgroup:", "").strip() for label in workgroup_labels
    ]
    return ", ".join(workgroup_labels_no_prefix) or None


def has_child_issues(subissue_summary):
    """Return True if total in sub_issues_summary from issue_raw_data is greater than 0"""
    if subissue_summary and subissue_summary["total"] > 0:
        return True
    return False


def get_github_issues(github_access_token, limit):
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json",
    }
    per_page = limit if limit < 100 else 100
    params = {"state": "all", "per_page": per_page}

    issues = []
    while url and len(issues) < limit:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def format_gh_issues(issue):
    """Format github issue dictionary into fields expected in the ODP"""
    issue_dict = {}

    # will be divisions in the future
    issue_dict["workgroups"] = extract_workgroups_from_labels(issue.get("labels"))

    issue_dict["labels"] = ", ".join(
        [label.get("name") for label in issue.get("labels")]
    )

    issue_dict["assignee_ids"] = ", ".join(
        [str(user.get("id")) for user in issue.get("assignees")]
    )

    for attr in [
        "title",
        "body",
        "state",
        "number",
        "id",
        "url",
    ]:
        issue_dict[attr] = issue.get(attr)

    # convert timestamps
    for attr in [
        "closed_at",
        "created_at",
        "updated_at",
    ]:
        issue_dict[attr] = convert_timestamp(issue.get(attr))

    # Preprocess issue description using the new function
    issue_dict["body"] = remove_html_comments(issue_dict["body"])

    # Get issue type
    issue_dict["type"] = issue.get("type").get("name") if issue.get("type") else None

    issue_dict["estimate"] = None  # estimate is issue_field 5181

    if issue.get("issue_field_values"):
        for field in issue["issue_field_values"]:
            issue_field_socrata = ISSUE_FIELDS_MAPPING.get(field["issue_field_id"])
            if issue_field_socrata:
                if field.get("single_select_option"):
                    issue_dict[issue_field_socrata["socrata_name"]] = field.get(
                        "single_select_option"
                    ).get("name")
                else:
                    issue_dict[issue_field_socrata["socrata_name"]] = field["value"]

    return issue_dict


def convert_timestamp(date_string):
    if date_string:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").isoformat()
    return None


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main(args):
    logging.info("Fetching github issues...")
    request_limit = args.limit if args.limit else 999999
    issues_gh = get_github_issues(GITHUB_ACCESS_TOKEN, request_limit)
    issues = [format_gh_issues(issue) for issue in issues_gh]

    # Will remove after I get confirmation that the DTS statuses are being updated
    # since the DTS status should then be closed if the issue is closed
    logging.info("Processing statuses...")
    for issue in issues:
        if issue["state"] == "closed":
            issue["pipeline"] = "Closed"

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
    parser = argparse.ArgumentParser(
        description="Take github issues from atd-data-tech repo and upload to Socrata"
    )

    parser.add_argument(
        "--limit", type=int, required=False, help="Issue query limit, optional"
    )
    args = parser.parse_args()
    main(args)

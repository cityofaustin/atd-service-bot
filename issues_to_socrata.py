#!/usr/bin/env python3
"""
Fetch Github issues and publish them to open data portal
"""
from datetime import datetime
import logging
import os
import sys

import requests
import sodapy

from queries import all_project_issues_ghp
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


def get_github_issues(github_access_token):
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json",
    }
    params = {"state": "all", "per_page": 100}

    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def format_gh_issues(issue):
    """Format github issue dictionary into fields expected in the ODP"""
    issue_dict = {}

    issue_dict["workgroups"] = extract_workgroups_from_labels(issue.get("labels"))

    issue_dict["labels"] = ", ".join(
        [label.get("name") for label in issue.get("labels")]
    )

    issue_dict["assignee_ids"] = ", ".join(
        [str(user.get("id")) for user in issue.get("assignees")]
    )

    issue_dict["is_epic"] = has_child_issues(issue.get("sub_issues_summary"))

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

    issue_dict["estimate"] = None # estimate is issue_field 5181

    if issue.get("issue_field_values"):
        for field in issue["issue_field_values"]:
            issue_field = ISSUE_FIELDS_MAPPING.get(field["issue_field_id"])
            if issue_field:
                issue_dict[issue_field["socrata_name"]] = field["value"]

    return issue_dict


def convert_timestamp(date_string):
    if date_string:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").isoformat()
    return None


# retrieves all issues from DTS Project Portfolio github project board
def get_project_portfolio_issues(*, query, endpoint, admin_secret):
    request_variables = {}
    headers = {"Authorization": f"Bearer {admin_secret}"}
    issues = []

    end_cursor = ""
    has_next_page = True
    while has_next_page:
        request_variables["cursor"] = end_cursor
        payload = {"query": query, "variables": request_variables}
        res = requests.post(endpoint, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        try:
            has_next_page = data["data"]["organization"]["projectV2"]["items"][
                "pageInfo"
            ]["hasNextPage"]
            end_cursor = data["data"]["organization"]["projectV2"]["items"]["pageInfo"][
                "endCursor"
            ]
            issues = (
                issues + data["data"]["organization"]["projectV2"]["items"]["nodes"]
            )
        except KeyError:
            raise ValueError(data)

    return issues


def make_project_issue_lookup(project_issues):
    """Returns dictionary where keys are issue numbers and value is their status"""
    project_issue_lookup = {}
    for issue in project_issues:
        # skip any items in project that do not have issue content
        if not issue["content"]:
            continue
        try:
            project_issue_lookup[issue["content"]["number"]] = issue.get(
                "status", {}
            ).get("name")
        except AttributeError:
            logging.info(
                f'Error getting issue status, Issue {issue["content"]["number"]} status is: {issue.get("status")}'
            )
    return project_issue_lookup


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main():
    logging.info("Fetching github issues...")
    issues_gh = get_github_issues(GITHUB_ACCESS_TOKEN)
    issues = [format_gh_issues(issue) for issue in issues_gh]

    logging.info("Fetching Project Porfolio data...")
    project_portfolio_issues = get_project_portfolio_issues(
        query=all_project_issues_ghp,
        endpoint=GITHUB_ENDPOINT,
        admin_secret=GITHUB_ACCESS_TOKEN,
    )

    portfolio_issues_dict = make_project_issue_lookup(project_portfolio_issues)

    logging.info("Processing statuses...")
    for issue in issues:
        if issue["state"] == "closed":
            issue["pipeline"] = "Closed"
        else:
            # if issue is not in the portfolio issues dictionary, the pipeline is None
            # this is temporary until we get issue fields
            issue["pipeline"] = portfolio_issues_dict.get(issue["number"])

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

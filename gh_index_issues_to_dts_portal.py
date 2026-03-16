#!/usr/bin/env python3

"""Create or update "Index" issues in the DTS Portal from Github.

We use the DTS portal to track our project (aka "Index" issue) scoring. This
script keeps the issue titles in the DTS portal in sync with Github by fetching these
issues from the atd-data-tech repo and either creating new project records in the DTS
portal or updating existing project records if their title or pipeline status does
not match the title of the issue on Github."""

import logging
import html
import os
import re
import sys

import knackpy
import markdown
import requests

from utils.utils import remove_html_comments

KNACK_API_KEY = os.environ["KNACK_API_KEY"]
KNACK_APP_ID = os.environ["KNACK_APP_ID"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
KNACK_OBJ = "object_30"
KNACK_TITLE_FIELD = "field_538"
KNACK_ISSUE_NUMBER_FIELD = "field_492"
KNACK_PIPELINE_FIELD = "field_649"  # production
KNACK_COMMENT_FIELD = "field_674"
KNACK_COMMENT_DATE_FIELD = "field_676"
KNACK_ISSUE_ASSIGNEE = "field_675"

# KNACK_COMMENT_FIELD = "field_688"  # staging field
# KNACK_COMMENT_DATE_FIELD = "field_689"  # staging field
# KNACK_ISSUE_ASSIGNEE = "field_690"  # staging field

headers = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def find_knack_record_by_issue(knack_records, issue_number):
    """
    Find a knack record by issue number.
    Return None if none found.
    """
    for record in knack_records:
        if record[KNACK_ISSUE_NUMBER_FIELD] == issue_number:
            return record
    return None


def get_project_index_issues():
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    params = {"state": "all", "labels": ["Project Index"], "per_page": 100}

    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues





def get_last_comment(issue_comment_url):
    try:
        r = requests.get(issue_comment_url, headers=headers)
        r.raise_for_status()
        comments = r.json()
    except Exception as err:
        print(f"An error occurred: {err}")

    last_comment = comments[-1]
    last_comment_body = last_comment.get("body")
    # convert comment to html
    last_comment_body = markdown.markdown(last_comment_body)
    # remove html comments from comment, which knack will remove
    last_comment_body = remove_html_comments(last_comment_body)
    # unescape character encodings, which knack will will also do
    last_comment_body = html.unescape(last_comment_body)
    last_comment_date = last_comment.get("created_at")

    return last_comment_body, last_comment_date


def build_payload(project_records, project_issues):
    """
    Build a payload to update knack records based on github issues.
    Take care to create the payload for each issue so that it will work as a create or
    update call depending on if the record already exists in the Knack app.
    """

    payload = []
    for issue in project_issues:  # iterate over gh issues
        # temporarily setting pipeline as None until we get issue fields
        pipeline = None
        last_comment_body = None
        last_comment_date = None
        # comments is a field that equals the number of comments on an issue
        if issue.get("comments") > 0:
            last_comment_body, last_comment_date = get_last_comment(
                issue.get("comments_url")
            )

        # an issue often has more than one assignee, this returns the list of users assigned to the issue
        assignees = issue.get("assignees")
        assignees_logins = [user.get("login") for user in assignees]
        assignees_string = " ".join(assignees_logins)

        # Until we get issue fields, the only pipeline we will update is if the issue has been closed
        if issue.get("state") == "closed":
            pipeline = "Closed"

        issue_title = issue.get("title")
        issue_number = issue.get("number")

        knack_record = find_knack_record_by_issue(project_records, issue_number)

        if knack_record:
            update_record = False
            issue_payload = {"id": knack_record["id"]}
            title_knack = knack_record[KNACK_TITLE_FIELD]
            pipeline_knack = knack_record[KNACK_PIPELINE_FIELD]
            last_comment_knack = knack_record[KNACK_COMMENT_FIELD]
            assignee_knack = (
                knack_record[KNACK_ISSUE_ASSIGNEE]
                if knack_record[KNACK_ISSUE_ASSIGNEE]
                else ""
            )

            if title_knack != issue_title:
                issue_payload[KNACK_TITLE_FIELD] = issue_title
                update_record = True
            if pipeline and pipeline_knack != pipeline:
                issue_payload[KNACK_PIPELINE_FIELD] = pipeline
                update_record = True
            if last_comment_knack != last_comment_body:
                issue_payload[KNACK_COMMENT_FIELD] = last_comment_body
                issue_payload[KNACK_COMMENT_DATE_FIELD] = str(last_comment_date)
                update_record = True
            if assignee_knack != assignees_string:
                issue_payload[KNACK_ISSUE_ASSIGNEE] = assignees_string
                update_record = True
            if update_record:
                payload.append(issue_payload)

        else:
            issue_payload = {
                KNACK_ISSUE_NUMBER_FIELD: issue_number,
                KNACK_TITLE_FIELD: issue_title,
                KNACK_ISSUE_ASSIGNEE: assignees_string,
            }
            if pipeline is not None:
                issue_payload[KNACK_PIPELINE_FIELD] = pipeline
            if last_comment_body is not None:
                issue_payload[KNACK_COMMENT_FIELD] = last_comment_body
                issue_payload[KNACK_COMMENT_DATE_FIELD] = str(last_comment_date)

            payload.append(issue_payload)
    return payload


def main():
    logging.info("Starting...")

    # setup and get the knack records
    logging.info("Downloading records from Knack")
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    project_records = app.get(KNACK_OBJ)

    logging.info("Downloading issues from github")
    project_issues = get_project_index_issues()

    # build the payload out of the github and knack state of the data
    logging.info("Building payload...")
    knack_payload = build_payload(
        project_records,
        project_issues,
    )

    # iterate over the payload issuing an update or create as needed per issue
    # into knack. Report the status to be logged in airflow.
    logging.info(f"Creating/updating {len(knack_payload)} issues")
    for record in knack_payload:
        method = "update" if record.get("id") else "create"
        app.record(data=record, method=method, obj=KNACK_OBJ)
    logging.info(f"{len(knack_payload)} records processed.")


if __name__ == "__main__":
    # airflow needs this to see logs from the DockerOperator
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

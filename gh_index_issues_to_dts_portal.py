#!/usr/bin/env python3

""" Create or update "Index" issues in the DTS Portal from Github.

We use the DTS portal to track our project (aka "Index" issue) scoring. This
script keeps the issue titles in the DTS portal in sync with Github by fetching these
issues from the atd-data-tech repo and either creating new project records in the DTS
portal or updating existing project records if their title or pipeline status does 
not match the title of the issue on Github."""

import logging
import os
import sys

from github import Github
import requests
import knackpy


ZENHUB_REPO = {"id": 140626918, "name": "cityofaustin/atd-data-tech"}
WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
ZENHUB_ACCESS_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]
KNACK_API_KEY = os.environ["KNACK_API_KEY"]
KNACK_APP_ID = os.environ["KNACK_APP_ID"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
REPO = "cityofaustin/atd-data-tech"
KNACK_OBJ = "object_30"
KNACK_TITLE_FIELD = "field_538"
KNACK_ISSUE_NUMBER_FIELD = "field_492"
KNACK_PIPELINE_FIELD = "field_649"  # production
KNACK_COMMENT_FIELD = "field_688"  # staging field
KNACK_COMMENT_DATE_FIELD = "field_689"  # staging field
KNACK_ISSUE_ASSIGNEE = "field_690"  # staging field


def get_zenhub_metadata(workspace_id, token, repo_id, timeout=60):
    """
    Fetch Zenhub metadata for a given repo.
    """
    url = f"https://api.zenhub.com/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
    params = {"access_token": token}
    res = requests.get(url, params=params, timeout=timeout)
    res.raise_for_status()
    return res.json()


def find_pipeline_by_issue(data, issue_number):
    """
    Find the pipeline for a given issue number in the Zenhub metadata.
    Return None if none found.
    """
    for pipeline in data["pipelines"]:
        for issue in pipeline["issues"]:
            if issue["issue_number"] == issue_number:
                return pipeline["name"]
    return None


def find_knack_record_by_issue(knack_records, issue_number):
    """
    Find a knack record by issue number.
    Return None if none found.
    """
    for record in knack_records:
        if record[KNACK_ISSUE_NUMBER_FIELD] == issue_number:
            return record
    return None


def are_timestamps_different(knack_timestamp, issue_timestamp):
    """
    Returns true if the stored comment timestamp in knack differs from the issues timestamp
    """
    if not knack_timestamp:
        if issue_timestamp:
            return True
        else:
            return False
    return knack_timestamp["date"] != issue_timestamp.strftime("%m/%d/%Y")


def build_payload(project_records, project_issues):
    """
    Build a payload to update knack records based on github issues and Zenhub metadata.
    Take care to create the payload for each issue so that it will work as a create or
    update call depending on if the record already exists in the Knack app.
    """
    zenhub_metadata = get_zenhub_metadata(
        WORKSPACE_ID, ZENHUB_ACCESS_TOKEN, ZENHUB_REPO["id"]
    )

    payload = []
    for issue in project_issues:  # iterate over gh issues
        pipeline = find_pipeline_by_issue(zenhub_metadata, issue.number)

        last_comment_body = None
        last_comment_date = None
        comments = issue.get_comments()
        # an issue often has more than one assignee, this returns the list of users assigned to the issue
        assignees = issue.assignees
        assignees_logins = [user.login for user in assignees]
        assignees_string = " ".join(assignees_logins)
        comments_list = [comment for comment in comments]
        if len(comments_list) > 0:
            last_comment = comments_list[-1]
            last_comment_body = last_comment.body
            last_comment_date = last_comment.created_at

        # ZH metadata does not include closed issues
        if issue.state == "closed":
            pipeline = "Closed"

        knack_record = find_knack_record_by_issue(project_records, issue.number)

        if knack_record:
            update_record = False
            issue_payload = {"id": knack_record["id"]}
            title_knack = knack_record[KNACK_TITLE_FIELD]
            pipeline_knack = knack_record[KNACK_PIPELINE_FIELD]
            last_comment_date_knack = knack_record[KNACK_COMMENT_DATE_FIELD]
            assignee_knack = (
                knack_record[KNACK_ISSUE_ASSIGNEE]
                if knack_record[KNACK_ISSUE_ASSIGNEE]
                else ""
            )

            if title_knack != issue.title:
                issue_payload[KNACK_TITLE_FIELD] = issue.title
                update_record = True
            if pipeline_knack != pipeline:
                issue_payload[KNACK_PIPELINE_FIELD] = pipeline
                update_record = True
            if are_timestamps_different(last_comment_date_knack, last_comment_date):
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
                KNACK_ISSUE_NUMBER_FIELD: issue.number,
                KNACK_TITLE_FIELD: issue.title,
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

    # setup an instance of our github client
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(REPO)

    # iterate over the github client's issues and build our working data
    logging.info("Downloading issues from github")
    project_issues_paginator = repo.get_issues(state="all", labels=["Project Index"])
    project_issues = [issue for issue in project_issues_paginator]

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

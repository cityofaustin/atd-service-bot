#!/usr/bin/env python3
""" Create or update "Index" issues in the DTS Portal from Github.

We use the DTS portal to track our project (aka "Index" issue) scoring. This
script keeps the issue titles in the DTS portal in sync with Github by fetching these
issues from the atd-data-tech repo and either creating new project records in the DTS
portal or updating existing project records if their title does not match the title of
the issue on Github."""
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
KNACK_PIPELINE_FIELD = "field_584"  # development
# KNACK_PIPELINE_FIELD = "field_649"  # production


def get_zenhub_metadata(workspace_id, token, repo_id, timeout=60):
    url = f"https://api.zenhub.com/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
    params = {"access_token": token}
    res = requests.get(url, params=params, timeout=timeout)
    res.raise_for_status()
    return res.json()


def find_pipeline_by_issue(data, issue_number):
    for pipeline in data["pipelines"]:
        for issue in pipeline["issues"]:
            if issue["issue_number"] == issue_number:
                return pipeline["name"]
    return None


def build_payload(
    project_records, project_issues, title_field, issue_number_field, pipeline_field
):
    zenhub_metadata = get_zenhub_metadata(
        WORKSPACE_ID, ZENHUB_ACCESS_TOKEN, ZENHUB_REPO["id"]
    )

    payload = []
    for issue in project_issues:
        pipeline = find_pipeline_by_issue(zenhub_metadata, issue.number)
        # print(f"Pipeline for issue {issue.number}: {pipeline}")

        # search for a corresponding Knack record for each project issue
        for record in project_records:
            issue_number_knack = record[issue_number_field]
            if not issue_number_knack or issue_number_knack != issue.number:
                continue

            title_knack = record[title_field]
            pipeline_knack = record[pipeline_field]

            issue_payload = {issue_number_field: issue.number}
            if title_knack != issue.title:
                issue_payload[title_field] = issue.title
            if pipeline_knack != pipeline:
                issue_payload[pipeline_field] = pipeline
            if title_knack != issue.title or pipeline_knack != pipeline:
                payload.append(issue_payload)
        else:
            # this issue needs a new project record created in Knack
            issue_payload = {issue_number_field: issue.number, title_field: issue.title}
            if pipeline is not None:
                issue_payload[pipeline_field] = pipeline
            payload.append(issue_payload)

    return payload


def main():
    logging.info("Starting...")

    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    project_records = app.get(KNACK_OBJ)

    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(REPO)

    project_issues_paginator = repo.get_issues(state="all", labels=["Project Index"])
    project_issues = [issue for issue in project_issues_paginator]

    knack_payload = build_payload(
        project_records,
        project_issues,
        KNACK_TITLE_FIELD,
        KNACK_ISSUE_NUMBER_FIELD,
        KNACK_PIPELINE_FIELD,
    )

    logging.info(f"Creating/updating {len(knack_payload)} issues")

    for record in knack_payload:
        method = "update" if record.get("id") else "create"
        print(f"Data: {record}, Method: {method}, Obj: {KNACK_OBJ}")

        # this is 400'ing because the private api doesn't have the
        # pipeline field in it, I think. I need to check with Karo
        # & Christina

        # app.record(data=record, method=method, obj=KNACK_OBJ)

    logging.info(f"{len(knack_payload)} records processed.")


if __name__ == "__main__":
    # airflow needs this to see logs from the DockerOperator
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

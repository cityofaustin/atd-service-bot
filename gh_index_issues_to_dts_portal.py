#!/usr/bin/env python3
import logging
import os
import sys

from github import Github
import knackpy


def build_payload(project_records, project_issues, title_field, issue_number_field):
    payload = []
    for issue in project_issues:
        # search for a corresponding Knack record for each project issue
        matched = False
        for record in project_records:
            issue_number_knack = record[issue_number_field]
            if not issue_number_knack:
                continue
            if issue_number_knack == issue.number:
                matched = True
                # matching Knack record found, so check if the titles match
                title_knack = record[title_field]
                if title_knack != issue.title:
                    # records without matching title will be updated with github issue
                    # title
                    payload.append({"id": record["id"], title_field: issue.title})
                    break
        if not matched:
            # this issue needs a new project record created in Knack
            payload.append({issue_number_field: issue.number, title_field: issue.title})
    return payload


def main():
    logging.info("Starting...")
    KNACK_API_KEY = os.environ["KNACK_API_KEY"]
    KNACK_APP_ID = os.environ["KNACK_APP_ID"]
    GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
    REPO = "cityofaustin/atd-data-tech"
    KNACK_OBJ = "object_30"
    KNACK_TITLE_FIELD = "field_538"
    KNACK_ISSUE_NUMBER_FIELD = "field_492"

    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    project_records = app.get(KNACK_OBJ)

    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(REPO)

    project_issues_paginator = repo.get_issues(state="all", labels=["Index"])
    project_issues = [issue for issue in project_issues_paginator]

    knack_payload = build_payload(
        project_records, project_issues, KNACK_TITLE_FIELD, KNACK_ISSUE_NUMBER_FIELD
    )

    logging.info(f"Creating/updating {len(knack_payload)} issues")

    for record in knack_payload:
        method = "update" if record.get("id") else "create"
        app.record(data=record, method=method, obj=KNACK_OBJ)

    logging.info(f"Creating/updating {len(knack_payload)} processed.")


if __name__ == "__main__":
    # airflow needs this to see logs from the DockerOperator
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

"""
Get issues tagged with Geo from Zenhub
get estimate and pipeline
add that data to github projects
same for closed issues
"""

import logging
import os
import sys
import json
import requests
from field_ids import zenhub_pipeline_ids
from queries import (
    zenhub_labeled_pipeline_query,
    all_issues_github_project_board,
    closed_zenhub_issues,
)

WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
ZENHUB_ENDPOINT = "https://api.zenhub.com/public/graphql"
ZENHUB_GRAPHQL_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]
GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

# This will search zenhub for only the issues with this label present
SEARCH_LABEL = "Service: Geo"
# This will only get github projects for a particular board ID
# Taken from the URL such as 6 here for Geo
# https://github.com/orgs/cityofaustin/projects/6/views/1
BOARD_ID = 6


def zenhub_paginated_graph_ql_query(
    query, endpoint, headers, request_variables, operation_name
):
    issues = []
    end_cursor = ""
    has_next_page = True
    while has_next_page:
        request_variables["endCursor"] = end_cursor
        payload = {"query": query, "variables": request_variables}
        res = requests.post(endpoint, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        has_next_page = data["data"][operation_name]["pageInfo"]["hasNextPage"]
        end_cursor = data["data"][operation_name]["pageInfo"]["endCursor"]
        issues = issues + data["data"][operation_name]["nodes"]

    return issues


def get_closed_zenhub_issues(endpoint, admin_secret):
    """
    Return all closed zenhub issues
    """
    headers = {"Authorization": f"Bearer {admin_secret}"}
    request_variables = {
        "workspaceId": WORKSPACE_ID,
        "label": SEARCH_LABEL,
    }
    issues = zenhub_paginated_graph_ql_query(
        query=closed_zenhub_issues,
        endpoint=endpoint,
        headers=headers,
        request_variables=request_variables,
        operation_name="searchClosedIssues",
    )
    # The pipeline returned always was the last pipeline the issue was in, not closed?
    for issue in issues:
        if len(issue["pipelineIssues"]["nodes"]) > 0:
            issue["pipelineIssues"]["nodes"][0]["pipeline"]["name"] = "Closed"
        else:
            issue["pipelineIssues"]["nodes"].append({"pipeline": {"name": "Closed"}})
    return issues


def get_zenhub_issues_by_pipeline(query, pipeline_id, endpoint, admin_secret):
    """
    Returns all the zenhub issues for a particular pipeline
    """
    headers = {"Authorization": f"Bearer {admin_secret}"}
    request_variables = {
        "pipelineId": pipeline_id,
        "label": SEARCH_LABEL,
    }
    issues = zenhub_paginated_graph_ql_query(
        query=query,
        endpoint=endpoint,
        headers=headers,
        request_variables=request_variables,
        operation_name="searchIssuesByPipeline",
    )
    return issues


# retrieves all issues from a github project board
def get_github_project_issues(*, query, endpoint, admin_secret):
    request_variables = {"boardId": BOARD_ID}
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


def main():
    zenhub_issues = []

    for pipeline in zenhub_pipeline_ids:
        logging.info(pipeline)
        response = get_zenhub_issues_by_pipeline(
            query=zenhub_labeled_pipeline_query,
            pipeline_id=pipeline["id"],
            endpoint=ZENHUB_ENDPOINT,
            admin_secret=ZENHUB_GRAPHQL_TOKEN,
        )
        pipeline_issues = []
        for issue in response:
            assert len(issue["pipelineIssues"]["nodes"]) == 1
            pipeline_issues.append(issue)
        zenhub_issues = zenhub_issues + pipeline_issues

    closed_issues = get_closed_zenhub_issues(ZENHUB_ENDPOINT, ZENHUB_GRAPHQL_TOKEN)
    # open_issues = [issue["number"] for issue in zenhub_issues]
    # for closed_issue in closed_issues:
    #     assert closed_issue["number"] not in open_issues
    zenhub_issues = zenhub_issues + closed_issues

    # Cleaning up zenhub issues
    cleaned_zenhub_issues = []
    for issue in zenhub_issues:
        entry = {
            "zenhub_id": issue["id"],
            "title": issue["title"],
            "issue_number": issue["number"],
            "pipeline": issue["pipelineIssues"]["nodes"][0]["pipeline"]["name"],
        }
        if issue["estimate"]:
            entry["estimate"] = issue["estimate"]["value"]
        else:
            entry["estimate"] = None
        cleaned_zenhub_issues.append(entry)
    zenhub_issues = cleaned_zenhub_issues

    with open("geo_issues.json", "w", encoding="utf-8") as f:
        json.dump(zenhub_issues, f, ensure_ascii=False, indent=4)

    github_project_issues = get_github_project_issues(
        query=all_issues_github_project_board,
        endpoint=GITHUB_ENDPOINT,
        admin_secret=GITHUB_ACCESS_TOKEN,
    )
    github_project_issues_cleaned = []
    for issue in github_project_issues:
        entry = {
            "github_project_id": issue["id"],
            "title": issue["content"]["title"],
            "issue_number": issue["content"]["number"],
            "pipeline": issue["status"]["name"],
        }
        if issue["estimate"]:
            entry["estimate"] = issue["estimate"]["number"]
        else:
            entry["estimate"] = None
        github_project_issues_cleaned.append(entry)

    github_project_issues = github_project_issues_cleaned

    with open("ghp_issues.json", "w", encoding="utf-8") as f:
        json.dump(github_project_issues, f, ensure_ascii=False, indent=4)
    github_project_issues

    zenhub_issue_numbers = [issue["issue_number"] for issue in zenhub_issues]
    github_issue_numbers = [issue["issue_number"] for issue in github_project_issues]

    for issue in github_project_issues:
        if issue["issue_number"] not in zenhub_issue_numbers:
            # These are likely issues inside the board but without the appropriate 'Service: ' label.
            logging.info(f"{issue['issue_number']} not found in zenhub with pipeline: {issue['pipeline']}")
        else:
            for zenhub_issue in zenhub_issues:
                if zenhub_issue["issue_number"] == issue["issue_number"]:
                    issue["zenhub_id"] = zenhub_issue["zenhub_id"]
                    issue["zenhub_estimate"] = zenhub_issue["estimate"]
                    issue["zenhub_pipeline"] = zenhub_issue["pipeline"]
                    # issue["zenhub_data"] = zenhub_issue
                    break

    for issue in zenhub_issues:
        if issue["issue_number"] not in github_issue_numbers:
            # These are issues that have not been migrated to the appropriate project board for whatever reason.
            logging.info(f"{issue['issue_number']} not found in zenhub with pipeline: {issue['pipeline']}")

    # optional for exporting to csv
    # import pandas as pd
    # df = pd.DataFrame(github_project_issues)
    # df.to_csv("ghp_issues.csv", index=False)
    github_project_issues


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

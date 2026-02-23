"""
Get issues tagged with Geo from Zenhub
get estimate and pipeline
add that data to github projects
same for closed issues
"""

import logging
import time
import os
import sys
import json
import requests
from field_ids import zenhub_pipeline_ids, github_project_board_ids
from queries import (
    zenhub_labeled_pipeline_query,
    all_issues_github_project_board,
    closed_zenhub_issues,
    gh_projects_fields_query,
    add_issue_to_github_project_mutation,
    github_project_field_value_mutation,
    get_github_node_id,
    get_project_item_query,
    github_project_update_pipeline_estimate,
    github_project_update_pipeline
)

WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
ZENHUB_ENDPOINT = "https://api.zenhub.com/public/graphql"
ZENHUB_GRAPHQL_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]
GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

TEAM = "Dev"
# This will search zenhub for only the issues with this label present
SEARCH_LABEL = f"Service: {TEAM}"
# This will only get github projects for a particular board ID
BOARD_ID = github_project_board_ids[TEAM]["board_id"]
BOARD_NODE_ID = github_project_board_ids[TEAM]["board_node_id"]
ESTIMATE_FIELD_ID = github_project_board_ids[TEAM]["estimate_field_id"]
PIPELINE_FIELD_ID = github_project_board_ids[TEAM]["pipeline_field_id"]["field_id"]
PIPELINE_OPTIONS = github_project_board_ids[TEAM]["pipeline_field_id"]["options"]


# query for finding github project board and field IDs
# request_variables = {}
# headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
# payload = {"query": gh_projects_fields_query, "variables": request_variables}
# res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
# res.raise_for_status()
# data = res.json()
# data


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


def get_issue_node_id(issue_number):
    request_variables = {
        "owner": "cityofaustin",
        "repo": "atd-data-tech",
        "issueNumber": issue_number,
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": get_github_node_id, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"]["repository"]["issue"]["id"]


def add_issue_to_github_project(contentId):
    request_variables = {
        "projectId": BOARD_NODE_ID,
        "contentId": contentId,
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": add_issue_to_github_project_mutation, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    if "errors" in data:
        # For whatever reason I get these errors every now and again. Sleep 15 seconds and try again.
        logging.error(data["errors"])
        if data["errors"][0]["message"] == ('Your attempt to move this item created a temporary conflict. Please try '
                                            'again.'):
            time.sleep(15)
            item_id = add_issue_to_github_project(contentId)
            return item_id
    else:
        return data["data"]["addProjectV2ItemById"]["item"]["id"]


def add_estimate_to_github_project(itemId, estimate):
    request_variables = {
        "projectId": BOARD_NODE_ID,
        "itemId": itemId,
        "fieldId": ESTIMATE_FIELD_ID,
        "value": estimate,
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": github_project_field_value_mutation, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"]["updateProjectV2ItemFieldValue"]["projectV2Item"]["id"]


def update_github_project_estimate_and_pipeline(itemId, estimate, pipeline):
    request_variables = {
        "projectId": BOARD_NODE_ID,
        "itemId": itemId,
        "estimateFieldId": ESTIMATE_FIELD_ID,
        "estimateValue": estimate,
        "statusFieldId": PIPELINE_FIELD_ID,
        "statusOptionId": PIPELINE_OPTIONS[pipeline],
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": github_project_update_pipeline_estimate, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"]["updateStatus"]["projectV2Item"]["id"]


def update_github_project_pipeline(itemId, pipeline):
    request_variables = {
      "projectId": BOARD_NODE_ID,
      "itemId": itemId,
      "fieldId": PIPELINE_FIELD_ID,
      "optionId": PIPELINE_OPTIONS[pipeline],
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": github_project_update_pipeline, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"]["updateProjectV2ItemFieldValue"]["projectV2Item"]["id"]


def get_project_item_id(issue_number):
    request_variables = {
        "owner": "cityofaustin",
        "repo": "atd-data-tech",
        "issueNumber": issue_number,
    }
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
    payload = {"query": get_project_item_query, "variables": request_variables}
    res = requests.post(GITHUB_ENDPOINT, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    boards = data["data"]["repository"]["issue"]["projectItems"]["nodes"]
    if len(boards) == 1:
        return boards[0]["id"]
    else:
        for board in boards:
            if board["project"]["id"] == BOARD_NODE_ID:
                return board["id"]


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
    other_repo_issues = []
    for issue in zenhub_issues:
        # Some issues are zenhub-only issues and do not already belong to the atd-data-tech repo.
        if issue["repository"]["name"] == "atd-data-tech":
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
        else:
            other_repo_issues.append(issue)
            logging.info(
                f"Zenhub Issue {issue['number']} not found in the atd-data-tech repository, is present in: {issue['repository']['name']}")
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

    github_estimates_to_update = []
    for issue in github_project_issues:
        if issue["issue_number"] not in zenhub_issue_numbers:
            # These are likely issues inside the board but without the appropriate 'Service: ' label.
            logging.info(
                f"{issue['issue_number']} not found in zenhub with pipeline: {issue['pipeline']}"
            )
        else:
            for zenhub_issue in zenhub_issues:
                if zenhub_issue["issue_number"] == issue["issue_number"]:
                    issue["zenhub_id"] = zenhub_issue["zenhub_id"]
                    issue["zenhub_estimate"] = zenhub_issue["estimate"]
                    issue["zenhub_pipeline"] = zenhub_issue["pipeline"]
                    if not issue["estimate"] and zenhub_issue["estimate"]:
                        github_estimates_to_update.append(issue)
                    break

    issues_to_migrate = []
    for issue in zenhub_issues:
        if issue["issue_number"] not in github_issue_numbers:
            if issue['pipeline'] == "Closed":
                issues_to_migrate.append(issue)
            # These are issues that have not been migrated to the appropriate project board.
            # if issue['pipeline'] != "Closed":
            #     logging.info(
            #         f"{issue['issue_number']} not found in github projects with pipeline: {issue['pipeline']}"
            #     )

    for issue in issues_to_migrate:
        issue_node_id = get_issue_node_id(issue["issue_number"])
        item_id = add_issue_to_github_project(issue_node_id)
        logging.info(f"Successfully added issue #{issue['issue_number']} to github projects.")
        if issue["estimate"]:
            item_id = add_estimate_to_github_project(item_id, issue["estimate"])
            logging.info(
                f"Successfully updated issue #{issue['issue_number']}'s estimate github projects. \n")
            # item_id = update_github_project_estimate_and_pipeline(item_id, issue["estimate"], issue["pipeline"])
            # logging.info(f"Successfully updated issue #{issue['issue_number']}'s estimate and pipeline github projects. \n")
        else:
            # item_id = update_github_project_pipeline(item_id, issue["pipeline"])
            # logging.info(f"Issue #{issue['issue_number']}'s has no estimate, just updated pipeline. \n ")
            logging.info(f"Issue #{issue['issue_number']}'s has no estimate. \n ")

    # for issue in github_estimates_to_update:
    #     est = issue["zenhub_estimate"]
    #     if est:
    #         item_id = get_project_item_id(issue["issue_number"])
    #         item_id = add_estimate_to_github_project(item_id, est)
    #         logging.info(f"Successfully updated issue #{issue['issue_number']}'s estimate in github projects. \n")

    # optional for exporting to csv
    # import pandas as pd
    # df = pd.DataFrame(github_project_issues)
    # df.to_csv("ghp_issues.csv", index=False)
    github_project_issues


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

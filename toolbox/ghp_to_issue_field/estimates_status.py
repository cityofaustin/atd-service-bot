import requests
import logging
import sys
import os

from queries import issue_estimates_status_query

GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}


def get_issues_from_ghp_board(query, endpoint, board_id):
    issues = []
    request_variables = {"boardID": board_id}
    end_cursor = ""
    has_next_page = True
    while has_next_page:
        request_variables["cursor"] = end_cursor
        payload = {"query": query, "variables": request_variables}
        res = requests.post(endpoint, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        has_next_page = data["data"]["organization"]["projectV2"]["items"]["pageInfo"][
            "hasNextPage"
        ]
        end_cursor = data["data"]["organization"]["projectV2"]["items"]["pageInfo"][
            "endCursor"
        ]
        issues = issues + data["data"]["organization"]["projectV2"]["items"]["nodes"]

    return issues


def update_issue_fields(issue_number, estimate, status):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}/issue-field-values"
    issue_field_values = []
    if estimate:
        issue_field_values.append({"field_id": 5181, "value": estimate})
    if status:
        issue_field_values.append({"field_id": 10226, "value": status})
    res = requests.post(
        endpoint, json={"issue_field_values": issue_field_values}, headers=headers
    )
    res.raise_for_status()
    logging.info(res)


def main():
    # gets issues with estimates and status from GHP board
    ghp_board_issues = get_issues_from_ghp_board(
        issue_estimates_status_query, GITHUB_ENDPOINT, 23
    )
    issues_cleaned = []
    for issue in ghp_board_issues:
        issue_number = issue["content"]["number"]
        issue_type = (
            issue.get("content").get("issueType").get("name")
            if issue["content"]["issueType"]
            else None
        )
        issue_estimate = (
            issue.get("estimate").get("number") if issue.get("estimate") else None
        )
        issue_status = issue.get("status").get("name") if issue.get("status") else None
        issues_cleaned.append(
            {
                "id": issue["id"],
                "number": issue_number,
                "estimate": issue_estimate,
                "status": issue_status,
                "type": issue_type,
            }
        )

    to_update = []
    for issue in issues_cleaned:
        if issue["type"] == "[Product Team] Task":
            if issue["estimate"] or issue["status"]:
                to_update.append(issue)

    for i in to_update:
        # for the most part, the statuses in the Status Issue Field matches the statuses in the github project
        # except for Closed/Complete. GHP board status Closed maps to Complete in the Issue Fields
        issue_field_status = i["status"] if i["status"] != "Closed" else "Complete"
        update_issue_fields(i["number"], i["estimate"], issue_field_status)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

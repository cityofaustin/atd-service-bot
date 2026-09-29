import requests
import logging
import sys
import os
import argparse

from queries import issue_estimates_status_query

GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "GraphQL-Features": "issue_fields",
}

project_boards = {
    "Product": 23,
    "Amanda": 22,  # ECM
    "Tech Services": 21,
    "Dev": 25,
    "Operations": 20,
    "Apps": 16,
    "Data Science": 19,
    "Geo": 6,
    "Maximo": 18,
    "Portfolio": 27,
}


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


def main(args):
    # board_number = args.board
    board_number = 25
    # gets issues with estimates and status from GHP board
    ghp_board_issues = get_issues_from_ghp_board(
        issue_estimates_status_query, GITHUB_ENDPOINT, board_number
    )
    # TODO: i need to check if the estimate or status is already defined, and if so skip it.
    for issue in ghp_board_issues:
        issue_number = issue["content"]["number"]
        issue_estimate = (
            issue.get("estimate").get("number") if issue.get("estimate") else None
        )
        issue_status = issue.get("status").get("name") if issue.get("status") else None
        if issue_estimate or issue_status:
            update_issue_fields(issue_number, issue_estimate, issue_status)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Check estimates and statuses from project board and update fields"
    )
    # parser.add_argument("--board", required=True, help="name of team board")
    args = parser.parse_args()
    main(args)

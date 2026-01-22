#!/usr/bin/env python3
"""
Fetch all open Zenhub issues and save metadata to json
"""
import logging
import os
import sys
import json
import requests

from zenhub_to_github.queries import zh_estimates_query

WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
ZENHUB_ENDPOINT = "https://api.zenhub.com/public/graphql"
ZENHUB_GRAPHQL_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]


def make_graphql_request(*, query, endpoint, admin_secret):
    request_variables = {
        "workspaceId": WORKSPACE_ID,
    }
    headers = {"Authorization": f"Bearer {admin_secret}"}
    issues = []
    end_cursor = ""
    has_next_page = True
    while has_next_page:
        logging.info("has next page...")
        request_variables["after"] = end_cursor
        payload = {"query": query, "variables": request_variables}
        res = requests.post(endpoint, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        try:
            has_next_page = data["data"]["workspace"]["issues"]["pageInfo"][
                "hasNextPage"
            ]
            end_cursor = data["data"]["workspace"]["issues"]["pageInfo"]["endCursor"]
            issues = issues + data["data"]["workspace"]["issues"]["nodes"]
        except KeyError:
            raise ValueError(data)

    return issues


def main():
    logging.info("Fetching issues from zenhub...")
    issues = make_graphql_request(
        query=zh_estimates_query,
        endpoint=ZENHUB_ENDPOINT,
        admin_secret=ZENHUB_GRAPHQL_TOKEN,
    )

    with open("issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=4)

    # with open('issues.json') as saved_issues:
    #     issues = json.load(saved_issues)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

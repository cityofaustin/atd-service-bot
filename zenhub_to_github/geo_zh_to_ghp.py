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
from queries import geo_pipeline_query, all_geo_issues_ghp

WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
ZENHUB_ENDPOINT = "https://api.zenhub.com/public/graphql"
ZENHUB_GRAPHQL_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]
GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]


def get_geo_issue_by_pipeline_request(*, query, pipeline_id, endpoint, admin_secret):
    request_variables = {
        "pipelineId": pipeline_id,
    }
    headers = {"Authorization": f"Bearer {admin_secret}"}
    issues = []

    payload = {"query": query, "variables": request_variables}
    res = requests.post(endpoint, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()
    logging.info(data["data"]["searchIssuesByPipeline"]["totalCount"])
    try:
        issues = data["data"]["searchIssuesByPipeline"]["nodes"]
    except KeyError:
        raise ValueError(data)

    return issues


def get_geo_ghp_issues(*, query, endpoint, admin_secret):
    request_variables = {}
    headers = {"Authorization": f"Bearer {admin_secret}"}
    issues = []

    end_cursor = ""
    has_next_page = True
    while has_next_page:
        logging.info(end_cursor)
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
    geo_issues = []

    # TODO: also get the estimate from closed issues
    for pipeline in zenhub_pipeline_ids:
        logging.info(pipeline)
        pipeline_issues = get_geo_issue_by_pipeline_request(
            query=geo_pipeline_query,
            pipeline_id=pipeline["id"],
            endpoint=ZENHUB_ENDPOINT,
            admin_secret=ZENHUB_GRAPHQL_TOKEN,
        )
        geo_issues = geo_issues + pipeline_issues

    # loop through the issues and assign to ghp

    with open("geo_issues.json", "w", encoding="utf-8") as f:
        json.dump(geo_issues, f, ensure_ascii=False, indent=4)

    # ghp_issues = get_geo_ghp_issues(
    #     query=all_geo_issues_ghp,
    #     endpoint=GITHUB_ENDPOINT,
    #     admin_secret=GITHUB_ACCESS_TOKEN,
    # )

    # with open("ghp_issues.json", "w", encoding="utf-8") as f:
    #     json.dump(ghp_issues, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

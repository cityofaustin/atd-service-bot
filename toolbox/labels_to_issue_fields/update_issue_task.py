import requests
import logging
import sys
import os
import json

from secrets import GITHUB_ACCESS_TOKEN

GITHUB_ENDPOINT = "https://api.github.com/graphql"
# GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}", "Accept": "application/vnd.github+json"}


def get_all_github_issues():
    url = f'https://api.github.com/repos/cityofaustin/atd-data-tech/issues'
    params = {"per_page": 100, "state": "all"}
    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def main():
    all_issues = get_all_github_issues()
    logging.info(f"Total issues: {len(all_issues)}")

    missing_type = 0
    has_type = 0
    pull_request = 0
    task_added = []

    for issue in all_issues:
        if issue.get("pull_request"):
            logging.info(f"issue {issue.get('number')} is pull request, skipping type")
            pull_request += 1
            continue
        issue_type = issue.get("type").get("name") if issue.get("type") else None
        if not issue_type:
            missing_type += 1
            task_added.append(issue.get("number"))
        else:
            has_type += 1

    with open("issues_assigned_task.json", "w", encoding="utf-8") as f:
        json.dump(task_added, f, ensure_ascii=False, indent=4)

    logging.info(f"Issues alredy typed: {has_type}")
    logging.info(f"Pull requests: {pull_request}")
    logging.info(f"Issues without type, now with type Task: {missing_type}")




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

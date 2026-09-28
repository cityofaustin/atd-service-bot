"""
Gets atd-data-tech issues that lack a type and set type Task

https://github.com/cityofaustin/atd-data-tech/issues/28739

"""
import requests
import logging
import sys
import os

from secrets import GITHUB_ACCESS_TOKEN

GITHUB_ENDPOINT = "https://api.github.com/graphql"
# GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}", "Accept": "application/vnd.github+json"}


def update_issue_type_to_task(issue_number, task_added):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}"
    res = requests.post(
        endpoint, json={"type": "Task"}, headers=headers
    )
    logging.info(f"adding type to {issue_number}")
    if res.status_code == 200:
        task_added.append(issue_number)
        return True
    if res.status_code in (403, 429):
        # Rate limited (primary or secondary)
        logging.info(res.headers)
        retry_after = res.headers.get("Retry-After")
        limit_reset = res.headers.get("x-ratelimit-reset")
        if retry_after:
            logging.info(f"rate limited, wait {retry_after}")
        if limit_reset:
            logging.info(f"reset is at {limit_reset} ")
        return False
    # something else happened. log and return true so the script keeps going
    logging.info(issue_number, res.status_code)
    return True


def get_all_github_issues():
    url = f'https://api.github.com/repos/cityofaustin/atd-data-tech/issues'
    # remove type none to get all the issues
    params = {"per_page": 100, "state": "all", "type": "none"}
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
        issue_number = issue.get('number')
        if issue_number in [4189, 5692]:
            continue
        if issue.get("pull_request"):
            logging.info(f"issue {issue_number} is pull request, skipping type")
            pull_request += 1
            continue
        issue_type = issue.get("type").get("name") if issue.get("type") else None
        if not issue_type:
            missing_type += 1
            update_success = update_issue_type_to_task(issue_number, task_added)
            if not update_success:
                break
        else:
            has_type += 1

    logging.info(f"Issues alredy typed: {has_type}")
    logging.info(f"Pull requests: {pull_request}")
    logging.info(f"Issues without type, now with type Task: {missing_type}")




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

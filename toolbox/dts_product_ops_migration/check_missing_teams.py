"""
I was curious why my estimate for issues with more than one team was so off, so i used this
to see how many issues in our repo are lacking a team entirely. 

There were 777 issues

"""

import requests
import logging
import sys
import json
import csv

from secrets import GITHUB_ACCESS_TOKEN

GITHUB_ENDPOINT = "https://api.github.com/graphql"
# GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}

teams = [
    "Team: Geo",
    "Team: DTS Operations",
    "Team: Tech Services",
    "Team: Data Science",
    "Team: Maximo",
    "Team: AMANDA",
    "Team: Apps",
    "Team: Dev",
    "Team: Product",
]


def get_all_issues():
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    params = {"per_page": 100, "state": "all", "type": "task"}
    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def check_missing_team(issue):
    all_labels = issue.get("labels")
    for label in all_labels:
        if label.get("name") in teams:
            return False
    return True


def check_missing_team_issue_field(issue):
    if issue.get("issue_field_values"):
        field_values = issue.get("issue_field_values")
        for field in field_values:
            if field.get("issue_field_id") == 6520:
                return False
    return True


def main():
    # all_issues = get_all_issues()

    # with open("ALL_task_issues.json", "w", encoding="utf-8") as f:
    #     json.dump(all_issues, f, ensure_ascii=False, indent=4)

    with open("ALL_task_issues.json", "r") as f:
        all_issues = json.load(f)

    logging.info(f"Total task issues: {len(all_issues)}")

    missing_teams = []
    missing_issue_field = []
    output = []

    check = []

    for issue in all_issues:
        issue_number = issue.get("number")
        if check_missing_team(issue):
            missing_teams.append(issue)
        if check_missing_team_issue_field(issue):
            missing_issue_field.append(issue_number)

    for issue in missing_teams:
        issue_number = issue.get("number")
        if issue_number not in missing_issue_field:
            continue
        if len(issue["assignees"]) > 1:
            assignees = [a["login"] for a in issue["assignees"]]
        else:
            assignees = ""
        if len(issue["labels"]) > 1:
            labels = [l["name"] for l in issue["labels"]]
        else:
            labels = ""
        output.append(
            {
                "number": issue_number,
                "title": issue["title"],
                "date_created": issue["created_at"],
                "author": issue["user"]["login"],
                "assignees": assignees,
                "labels": labels,
                "status": issue["state"],
                "date_closed": issue["closed_at"],
                "url": issue["html_url"],
            }
        )

    # for number in missing_issue_field:
    #     if number not in missing_teams:
    #         check.append(number)

    logging.info(len(missing_teams))

    logging.info(check)

    keys = output[0].keys()
    with open(
        f"missing_labels.csv", "w", newline=""
    ) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

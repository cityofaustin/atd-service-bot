"""
Updates the DTS Teams issue field for Epics in atd-data-tech based on the Team labels

Github issue: https://github.com/cityofaustin/atd-data-tech/issues/28739

"""

import requests
import logging
import sys
import os
import json
import csv

from queries import issue_team_label_query
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


def get_all_task_issues_of_team(team_label):
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    params = {"per_page": 100, "state": "all", "type": "task", "labels": team_label}
    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def has_team_github_field(issue):
    if issue.get("issue_field_values"):
        field_values = issue.get("issue_field_values")
        for field in field_values:
            if field.get("issue_field_id") == 6520:
                logging.info(f"{issue['number']} is already team {field.get('single_select_option').get('name')}")
                return True
    return False


def check_team_labels(issue, other_teams):
    all_labels = issue.get("labels")
    for label in all_labels:
        if label.get("name") in other_teams:
            # logging.info(f"duplicate {issue.get('number')}: {label['name']}")
            return False
    return True


def update_issue_field_team(issue_number):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}/issue-field-values"
    issue_field_values = []
    # TODO: we can use the text/name, update
    issue_field_values.append({"field_id": 6520, "value": 8057})
    res = requests.post(
        endpoint, json={"issue_field_values": issue_field_values}, headers=headers
    )
    res.raise_for_status()
    # logging.info(res)


def main():
    # this should be a parameter
    team_name = "Team: DTS Operations"
    all_issues = get_all_task_issues_of_team(team_name)
    logging.info(f"Total task issues of {team_name}: {len(all_issues)}")
    # with open("all_task_issues.json", "w", encoding="utf-8") as f:
    #     json.dump(all_issues, f, ensure_ascii=False, indent=4)
    # with open('prodlabelissues.json', 'r') as file:
    #     all_issues = json.load(file)

    extra_teams = []

    for issue in all_issues:
        issue_number = issue.get("number")
        # if we already have the team issue field, just skip it
        if has_team_github_field(issue):
            continue
        other_teams = [name for name in teams if name != team_name]
        one_team = check_team_labels(issue, other_teams)
        if one_team:
            # assign the team here
            # logging.info(issue_number)
            continue
        else:
            if len(issue["assignees"]) > 1:
                assignees = [a["login"] for a in issue["assignees"]]
            else:
                assignees = ""
            if len(issue["labels"]) > 1:
                labels = [l["name"] for l in issue["labels"]]
            else:
                labels=""
            extra_teams.append({
                "number": issue_number,
                "title": issue["title"],
                "date_created": issue["created_at"],
                "author": issue["user"]["login"],
                "assignees": assignees,
                "labels": labels,
                "status": issue["state"],
                "date_closed": issue["closed_at"],
                "url": issue["html_url"]
            })

            # extra_teams.append(issue)

    logging.info(f"total issues with duplicate teams {len(extra_teams)}")
    with open("oper_extras.json", "w", encoding="utf-8") as f:
        json.dump(extra_teams, f, ensure_ascii=False, indent=4)

    keys = extra_teams[0].keys()
    with open('clean_up_oper.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(extra_teams)



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

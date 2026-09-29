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
import argparse

# from secrets import GITHUB_ACCESS_TOKEN

GITHUB_ENDPOINT = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
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

label_to_issue_field_mapping = {
    "Team: Geo": "Geo",
    "Team: DTS Operations": "Operations",
    "Team: Tech Services": "Tech Services",
    "Team: Data Science": "Data Science",
    "Team: Maximo": "Maximo",
    "Team: AMANDA": "ECM",
    "Team: Apps" : "Apps",
    "Team: Dev": "Dev",
    "Team: Product": "Product",
}


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
    """
    Checks if issue has issue_field_values defined, loops through the fields defined to see if the DTS Team field is set
    returns True if there is already a team set
    """
    if issue.get("issue_field_values"):
        field_values = issue.get("issue_field_values")
        for field in field_values:
            if field.get("issue_field_id") == 6520:
                logging.info(f"{issue['number']} is already team {field.get('single_select_option').get('name')}")
                return True
    return False


def check_team_labels(issue, other_teams):
    """
    Checks if issue has one of the other teams in their labels. Task issues should only have one team associated,
    return False if there is more than one team on an issue
    """
    all_labels = issue.get("labels")
    for label in all_labels:
        if label.get("name") in other_teams:
            # logging.info(f"duplicate {issue.get('number')}: {label['name']}")
            return False
    return True


def update_issue_field_team(issue_number, team_name):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}/issue-field-values"
    issue_field_values = []
    issue_field_values.append({"field_id": 6520, "value": team_name})
    res = requests.post(
        endpoint, json={"issue_field_values": issue_field_values}, headers=headers
    )
    res.raise_for_status()


def main(args):
    # this should be a parameter
    # logging.info(args.team)
    # team_name = args.team
    team_name = "Team: DTS Operations"
    if team_name not in teams:
        raise ValueError(f"Team {team_name} not official team name.")
    issue_field_team_name = label_to_issue_field_mapping[team_name]
    all_issues = get_all_task_issues_of_team(team_name)
    logging.info(f"Total task issues of {team_name}: {len(all_issues)}")

    extra_teams = []

    for issue in all_issues:
        issue_number = issue.get("number")
        # if we already have the team issue field defined, just skip it
        if has_team_github_field(issue):
            continue
        other_teams = [name for name in teams if name != team_name]
        one_team = check_team_labels(issue, other_teams)
        if one_team:
            # assign the team here
            # update_issue_field_team(issue_number, issue_field_team_name)
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


    logging.info(f"total issues with duplicate teams {len(extra_teams)}")

    keys = extra_teams[0].keys()
    with open(f"clean_up_{label_to_issue_field_mapping[team_name]}.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(extra_teams)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch-update GitHub team issue field.")
    # parser.add_argument("--team", required=True, help="Team we are updating")
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    args = parser.parse_args()
    main(args)

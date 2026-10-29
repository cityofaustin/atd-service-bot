"""

Updates the DTS Teams issue field for Epics in atd-data-tech based on the Team labels

Github issue: https://github.com/cityofaustin/atd-data-tech/issues/28739

"""
import requests
import logging
import sys
import os

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


def get_all_epics():
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    params = {"per_page": 100, "state": "closed", "type": "epic"}
    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def has_teams_github_field(issue):
    if issue.get("issue_field_values"):
        field_values = issue.get("issue_field_values")
        for field in field_values:
            if field.get("issue_field_id") == 45472131:
                logging.info(f"- {issue['number']} is already team {field.get('value')}")
                return True
    return False


def get_list_of_team_labels(issue):
    all_labels = issue.get("labels")
    teams_on_issue = []
    for label in all_labels:
        label_name = label.get("name")
        if label_name in teams:
            teams_on_issue.append(label_to_issue_field_mapping[label_name])
    return teams_on_issue


def update_issue_field_teams(issue_number, teams):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}/issue-field-values"
    issue_field_values = []
    issue_field_values.append({"field_id": 45472131, "value": teams})
    res = requests.post(
        endpoint, json={"issue_field_values": issue_field_values}, headers=headers
    )
    res.raise_for_status()
    # logging.info(res)


def main():
    all_epics = get_all_epics()
    logging.info(f"Total epics: {len(all_epics)}")

    updated = 0

    for issue in all_epics:
        issue_number = issue.get("number")
        # if we already have the team issue field, just skip it
        if has_teams_github_field(issue):
            continue
        teams = get_list_of_team_labels(issue)
        logging.info(f"{issue_number}: {teams}")
        if teams:
            updated += 1
            update_issue_field_teams(issue_number, teams)


    logging.info(updated)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()

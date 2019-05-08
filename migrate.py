#TODO:
# validator/checker
# assignments
# update knack issue with github link
# udpate knack issue with migration status

import pdb
from pprint import pprint as print

from knackpy import Knack

from config.config import *
from config.secrets import API_KEY

kn = Knack(
  scene=KNACK_APP['scene'],
  view=KNACK_APP['view'],
  app_id=KNACK_APP['app_id'],
  api_key=API_KEY,
  ref_obj=KNACK_APP['ref_obj']
)

prepared = []

for row in kn.data:
    github_issue = {
        "description" : "",
        "labels" : [],
        "title" : ""
    }
    
    description = ''

    for field in KNACK_FIELDS.keys():
        if KNACK_FIELDS[field]['handle'] == 'merge_with_description':
            # add field values to issue description
            try:
                description = f"{description}\n{field}: {row[field]}\n"

            except KeyError:
                continue

        elif KNACK_FIELDS[field]['handle'] == 'url_in_description':
            # special url handler
            description = f"{description}\nDTS URL: https://atd.knack.com/dts#service-requests/view-issue-details/{row[field]}\n"

        elif "MAP_LABELS" in KNACK_FIELDS[field]['handle']:
            # lookup the cooresponding label
            label_name = KNACK_FIELDS[field]['handle'].split("LABELS_")[1]

            try:
                github_issue['labels'].append(
                    LABEL_MAPS[label_name][row[field]]
                )

            except KeyError:
                continue
        
        elif "MAP_REPOS" in KNACK_FIELDS[field]['handle']:
            # map the app name to a repo where the issue will be created
            try:
                if row[field]:
                    app_name = row[field]

            except KeyError:
                continue

            github_issue['repo'] = REPOS[app_name]

        elif "MAP_ASSIGNEES" in KNACK_FIELDS[field]['handle']:
            # map the assignee to github username
            try:
                if row[field]:
                    assignee = row[field]

            except KeyError:
                continue

            github_issue['assignee'] = ASSIGNEES[assignee]

        else:
            # send the "handle" value as a key in the issue dict
            try:
                github_issue[KNACK_FIELDS[field]['handle']] = row[field]
            
            except KeyError:
                continue

    github_issue['description'] = description

    prepared.append(github_issue)

pdb.set_trace()


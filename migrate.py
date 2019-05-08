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

        else:
            # send the "handle" value as a key in the issue dict
            try:
                github_issue[KNACK_FIELDS[field]['handle']] = row[field]
            
            except KeyError:
                continue


    github_issue['description'] = description

    pdb.set_trace()

pdb.set_trace()


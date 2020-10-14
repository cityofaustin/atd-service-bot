# atd-service-bot
A bot that creates github issues from our Knack-based intake form.

## Get it going

1. Configure these environmental variables, which you can grab from Airflow:
- KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME
- KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD
- KNACK_API_KEY
- KNACK_APP_ID
- GITHUB_ACCESS_TOKEN

2. Pull the docker image (`atddocker/atd-service-bot`) or install the package dependencies: `pip install -r requirements.txt`

3. Run `python intake.py`

## How it works

The bot runs on Airflow and fetches new service requests from our Knack app. It geneterates a github issue and applies labels and assignees based on the definitions in `config/config.py`. With the github issue successfully created, the bot submits an "edit record" form in Knack, which sets the record's `github_transmission_status` to `sent`. The form submit also triggers email notifications to the requester and to our staff.

## How not to break the bot

Keeping our bot happy is contingent on not changing the information our bot expects to process.

You must update `config/config.py` if you change any of these things in the DTS Knack app:
- Workgroup names
- Any pre-defined choice-list options (impact, need, application, workgroup, etc)

...or if you change any of these things on github:
- repo names
- labels
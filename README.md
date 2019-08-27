# atd-service-bot
A bot that creates github issues from our Knack-based intake form.

## Get it going

1. Add a file called `secrets.py` to the `config` directory following the `config/secrets_template.py` template.

2. Install the package dependencies: `pip install -r requirements.txt`

3. Run it once, or schedule as a cron job: `python intake.py`

## How it works

The bot runs on a cron schedule and fetches new service requests from our Knack app. It geneterates a github issue and applies labels and assignees based on the definitions in `config/config.py`. With the github issue successfully created, the bot submits an "edit record" form in Knack, which sets the record's `github_transmission_status` to `sent`. The form submit also triggers email notifications to the requester and to our staff.

## How not to break the bot

Keeping our bot happy is contingent on not changing the information our bot expects to process.

You must update `config/config.py` if you change any of these things in the DTS Knack app:
- Workgroup names
- Any pre-defined choice-list options (impact, need, application, workgroup, etc)

...or if you change any of these things on github:
- repo names
- labels
# atd-service-bot

A bot that creates github issues from our Knack-based intake form.

## Get it going

Place the following environment variables in `.env`, which you can grab from 1Password:

- KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME
- KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD
- KNACK_API_KEY
- KNACK_APP_ID
- GITHUB_ACCESS_TOKEN
- ZENHUB_ACCESS_TOKEN
- SOCRATA_ENDPOINT
- SOCRATA_API_KEY_ID
- SOCRATA_API_KEY_SECRET
- SOCRATA_APP_TOKEN
- SOCRATA_RESOURCE_ID (of the Socrata dataset for issues)

* Run this command to build the docker container:

```bash
docker compose build
```

- Run this command to be dropped into a development environment that simulates the
  the environment that the docker container / program will be in when it's kicked off by
  airflow.

```bash
docker compose run service-bot
```

- While inside the shell provided by the container, you can run the scripts, and you
  are able to continue to edit them outside of the container because they are bind-mounted in.

## How it works

The bot runs on Airflow and fetches new service requests from our Knack app. It generates a github issue and applies labels and assignees based on the definitions in `config/config.py`. With the github issue successfully created, the bot submits an "edit record" form in Knack, which sets the record's `github_transmission_status` to `sent`. The form submit also triggers email notifications to the requester and to our staff.

## How not to break the bot

Keeping our bot happy is contingent on not changing the information our bot expects to process.

You must update `config/config.py` if you change any of these things in the DTS Knack app:

- Workgroup names
- Any pre-defined choice-list options (impact, need, application, workgroup, etc)

...or if you change any of these things on github:

- repo names
- labels

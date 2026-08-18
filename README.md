# atd-service-bot

This repository contains scripts that manage DTS's github issues from our Knack-based service request intake form.
- `intake.py` houses the bot that creates [issues](https://github.com/cityofaustin/atd-data-tech/issues/) from the Knack DTS Portal.
- `issues_to_socrata.py` publishes information from the issues to the [Open Data Portal](https://data.austintexas.gov) [dataset](https://datahub.austintexas.gov/Transportation-and-Mobility/Transportation-Public-Works-Data-Tech-Services-Iss/rzwg-fyv8/about_data)
- `gh_index_issues_to_dts_portal.py` creates or updates "Index" issues in the DTS Portal from Github.


## Get it going

Place the following environment variables in `.env`, which you can grab from 1Password. There is a blank template in `env_template`.

- KNACK_DTS_PORTAL_SERVICE_BOT_USERNAME
- KNACK_DTS_PORTAL_SERVICE_BOT_PASSWORD
- KNACK_API_KEY
- KNACK_APP_ID
- GITHUB_ACCESS_TOKEN
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
docker compose run --rm service-bot
```

- While inside the shell provided by the container, you can run the scripts, and you
  are able to continue to edit them outside of the container because they are bind-mounted in.

- `issues_to_socrata.py` takes a few optional flags that are helpful for local development and testing with the [staging dataset](https://datahub.austintexas.gov/Transportation-and-Mobility/Test-Transportation-and-Public-Works-Data-and-Tech/93ru-6p6e/about_data):
  - `--limit` — limit the number of issues requested from GitHub
  - `--dry-run` / `-n` — fetch and process issues without uploading to Socrata
  - `--verbose` / `-v` — log the shape of payloads as they move through the script; `-vv` also dumps the full records

```bash
python issues_to_socrata.py --dry-run --limit 10 -v
python issues_to_socrata.py -n --limit 5 -vv
```

## How it works

The intake script runs on [Airflow](https://github.com/cityofaustin/atd-airflow) and fetches new service requests from our Knack app. It generates a github issue and applies labels and assignees based on the definitions in `config/config.py`. With the github issue successfully created, the bot submits an "edit record" form in Knack, which sets the record's `github_transmission_status` to `sent`. The form submit also triggers email notifications to the requester and to our staff.

## How not to break the bot

Keeping our bot happy is contingent on not changing the information our bot expects to process.

You must update `config/config.py` if you change any of these things in the DTS Knack app:

- Workgroup names
- Any pre-defined choice-list options (impact, need, application, workgroup, etc)

...or if you change any of these things on github:

- repo names
- labels

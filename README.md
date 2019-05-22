# atd-service-bot
A bot that creates github issues from 3rd-party form submissions

## Get It Going

Right now, the bot only knows how to migrate service requests on an ad-hoc basis. To do so:

1. Visit the DTS portal and set the `Github Migration Status` of your SR(s) as `Migrate to Github`.

2. Ready your Python environment:

- Use Python 3.6+ 

- Install the packages specified in `requirements.txt` with

```bash
$ pip install -r requirements.txt
```

3. Create a file named `secrets.py` following the template in `/config/secrets_template.py`

4. Migrate the service requests to Github:

```bash
$ python migrate_comments.py
```

This script will copy the service requests from the DTS portal as Github issues. The script will attempt to find an appropriate repository based on the `Application` information in the DTS portal. If no repo is found, issues will be created in the `atd-data-tech` repo. Labels will also be applied according to workgroup and service group. See `/config/config.py` for the complete field mapping.

The script will also update each DTS portal issue with a URL to the Github issue, and it will update the DTS issue with `Github Migration Result` as `successful`.

5. Migrate the service request notes to Github:
```bash
$ python migrate_comments.py
```

Each SR note will be added to as a comment to the corresponding Github issue as comments.

6. These scripts are idempotent, you can run then over and over again and any issue or comment that was successfully migrated will be ignored.

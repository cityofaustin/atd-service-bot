# Development tools

Local helpers for working on the Knack-to-GitHub intake bot. Run them from the repository root, with the same `.env` values used by the main scripts.

## `capture_knack.py`

Fetches the Knack records that `intake.py` would process and saves them as a timestamped JSON file.

```bash
python toolbox/development_tools/capture_knack.py
```

The script prints the payload and writes it to `captures/<timestamp>_knack_payload.json`. Replay the latest capture through intake without querying Knack again:

```bash
python intake.py --use-capture
```

Add `--dry-run` to print the issues intake would create without opening GitHub issues or updating Knack.

Requires `KNACK_API_KEY` and `KNACK_APP_ID`.

## `inspect_field_options.py`

Prints each GitHub issue field on `cityofaustin/atd-data-tech`, including its type and dropdown options with their GraphQL IDs.

```bash
python toolbox/development_tools/inspect_field_options.py
```

Use this when issue-field choices change on GitHub and `config/config.py` needs to be updated to match.

Requires `GITHUB_ACCESS_TOKEN`.

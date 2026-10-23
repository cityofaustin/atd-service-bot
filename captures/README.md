# Captures

Local snapshots of Knack records for developing `intake.py`. This file stays in the repository so the directory is not empty. Payload files do not.

`toolbox/development_tools/capture_knack.py` writes timestamped files here:

```text
captures/<timestamp>_knack_payload.json
```

Each file is the JSON array of records from the Knack view that intake processes. Replay the newest one without querying Knack:

```bash
python intake.py --use-capture
```

`intake.py` loads only files whose names end in `_knack_payload.json`. This README is not a capture.

These payloads can contain service-request data, so they are gitignored. After the Knack app changes, delete the old `*_knack_payload.json` files and capture a fresh one. A stale file will not match the updated app. Leave this README in place.

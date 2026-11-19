#!/usr/bin/env python3
"""
Write the Knack records that intake.py would process to a timestamped capture file.

Run from the repository root:

    python toolbox/development_tools/capture_knack.py

The payload is printed and written to ./captures/<timestamp>_knack_payload.json.
Replay the latest capture through intake with:

    python intake.py --use-capture
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import knackpy

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.config import KNACK_APP

KNACK_API_KEY = os.getenv("KNACK_API_KEY")
KNACK_APP_ID = os.getenv("KNACK_APP_ID")

# Must match CAPTURE_DIR / CAPTURE_SUFFIX in intake.py so --use-capture finds these files.
CAPTURE_DIR = REPO_ROOT / "captures"
CAPTURE_SUFFIX = "_knack_payload.json"


def write_knack_capture(issues):
    payload = [issue.data for issue in issues]
    text = json.dumps(payload, indent=2) + "\n"
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    path = CAPTURE_DIR / f"{datetime.now().strftime('%Y%m%dT%H%M%S')}{CAPTURE_SUFFIX}"
    path.write_text(text)
    print(text, end="")
    print(f"Wrote {path}")
    return path


def main():
    view = KNACK_APP["api_view"]["view"]
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    issues = app.get(view)
    write_knack_capture(issues)


if __name__ == "__main__":
    main()

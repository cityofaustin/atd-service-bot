from datetime import datetime
import math


def knack_issue_url(record_id, request_id=None):
    url = f"https://atd.knack.com/dts#manage-service-requests/triage-service-request/{record_id}/"
    label = request_id or record_id
    return f"[DTS Service Request Details - {label}]({url})"


def parse_attachment_url(_obj):
    return "Attachments available in Knack"


def parse_email(email_addr):
    """
    Extract `<First name> <Last intial>.` from email address
    """
    try:
        first, last = email_addr.split("@")[0].split(".")

        last = last[0]
        return f"{first} {last}.".title()

    except:
        # probably a ValueError/ maybe a malformed email address.
        # but we don't want to break the script if we can't parse the email.
        return "Error :("

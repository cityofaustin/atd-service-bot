from datetime import datetime
import math


def mills_to_timestamp(mills):
    return datetime.fromtimestamp(mills / 1000)


def app_url(record_id):
    return f"https://atd.knack.com/dts#service-requests/view-issue-details/{record_id}"


# courtesy of https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("b", "kb", "mb", "gb", "tb", "pb", "eb", "zb", "yb")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[i]}"


def parse_attachment_url(obj):
    url = obj.get("url")
    size = convert_size(obj.get("size"))

    # format as markdown
    return f"[Attachment]({url}) ({size})"


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

from datetime import datetime

def mills_to_timestamp(mills):
    return datetime.fromtimestamp(mills / 1000)


def app_url(record_id):
    return f"https://atd.knack.com/dts#service-requests/view-issue-details/{record_id}"
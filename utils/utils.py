import re

def remove_html_comments(text):
    if not isinstance(text, str):
        return text  # Return as-is if not a string
    # Remove HTML comments using regular expression
    return re.sub(r"<!--(.*?)-->", "", text, flags=re.DOTALL)

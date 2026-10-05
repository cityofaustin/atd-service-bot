KNACK_APP = {
    "api_view": {"scene": "scene_127", "view": "view_248", "ref_obj": ["object_24"]},
    "api_form": {"scene": "scene_131", "view": "view_252"},
}


FIELDS = [
    {
        "knack": "field_407",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # name
    {
        "knack": "field_400",
        "github": "title",
        "method": "copy",
        "format": "none",
    },  # Describe the problem (duplicated because this goes into the title and description body)
    {
        "knack": "field_1131",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    }, # App name
    {
        "knack": "field_400",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe the problem (duplicated because this goes into the title and description body)
    {
        "knack": "field_414",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Solution in mind
    {
        "knack": "field_415",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # How will we know that our solution is successful?
    {
        "knack": "field_417",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
        # users
    },
    {
        "knack": "field_418",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # stakeholders
    {
        "knack": "field_419",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # sponsors
    {
        "knack": "field_420",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # sd23
    {
        "knack": "field_421",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # asmp
    {
        "knack": "field_411",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe an outcome you'd like to see
    {
        "knack": "field_412",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe workarounds
    {
        "knack": "field_1101",  # Division
        "github": "issue_fields",
        "method": "map_issue_field_by_description",
        "field_name": "TPW Divisions",
    },
    {
        "knack": "field_404",  # Impact
        "github": "labels",
        "method": "map_append",
        "map": {
            "Severe — cannot perform work, no workaround": "Impact: 1-Severe",
            "Major — can only perform work using a workaround": "Impact: 2-Major",
            "Minor — can perform work, but could be easier or faster": "Impact: 3-Minor",
        },
    },
    {
        "knack": "field_413",  # Need Rating
        "github": "labels",
        "method": "map_append",
        "map": {
            "Must have — The application is illegal, unsafe, or not functional without it.": "Need: 1-Must Have",
            "Should have — This is important but not vital functionality or there is a temporary workaround. ": "Need: 2-Should Have",
            "Could have — We want this but there are more important requests.": "Need: 3-Could Have",
        },
    },
    {
        "knack": "field_410",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # How soon do you need this?
    {
        "knack": "field_405",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Anything else we should know?
    {
        "knack": "field_416",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # How have other divisions/departments/cities addressed similar challenges?
    {
        "knack": "field_398",  # What do you need help with?
        "github": "labels",
        "method": "map_append",
        "map": {
            "Bug Report — Something is not working": "Type: Bug Report",
            "Feature or Enhancement — An application I use could be improved": "Type: Enhancement",
            "Geospatial Services (GIS, Maps, etc.)": "Team: Geo",
            "New Project — My needs are not met by the technology & data available to me": "Type: New Application",
            "IT Support — Help with licenses, accounts, hardware, etc.": "Type: IT Support",
            "Something Else": "Type: Other",
        },
    },
    {
        "knack": "field_641",  # What do you need?
        "github": "labels",
        "method": "map_append_all",
        "map": {
            "Map": ["Team: Geo", "Type: Map Request"],
            "GIS Data": ["Team: Geo", "Type: Data"],
            "ArcGIS Training": ["Team: Geo", "Type: Training"],
            "ArcGIS Online Access": ["Team: Geo", "Type: IT Support"],
            "ArcGIS Online Support": ["Team: Geo", "Type: Data"],
            "ArcGIS Pro Support": ["Team: Geo", "Type: Data"],
            "ArcGIS Pro Installation": ["Team: Geo", "Type: IT Support"],
        },
    },
    {
        "knack": "field_1101",
        "github": "description",
        "method": "merge",
        "rename": "Workgroup",
    }, # Workgroup
    {
        "knack": "field_1099",  # DTS Service Group
        "github": "issue_fields",
        "method": "map_issue_field",
        "field_name": "DTS Team",
        "map": {
            "Team: Apps": "Apps",
            "Team: Geo": "Geo",
            "Team: Dev": "Dev",
            "Team: Product": "Product",
            "Team: Maximo": "Maximo",
            "Team: Amanda": "ECM",
            "Team: Data Science": "Data Science",
            "Team: DTS Operations": "Operations",
            "Team: Tech Services": "Tech Services",
        },
    },
    {
        "knack": "field_401",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # url
    {"knack": "field_403", "github": "description", "method": "merge"},  # Browser
    {
        "knack": "field_406",
        "github": "description",
        "method": "transform_merge",
        "transform": "parse_email",
        "format": "quote_text",
        "rename": "Requested By",
    },  # email > user name
    {
        "knack": "field_402",
        "github": "description",
        "method": "transform_merge",
        "transform": "parse_attachment_url",
        "format": "quote_text",
        "rename": "Attachments",
    }, # Attachments indicator
    {"knack": "id", "github": "knack_id", "method": "copy", "format": "none"},
    {
        "knack": "field_1122",
        "github": "assignee",
        "method": "split_append",
    },  # github usernames (comma-delimited) for assignees
    {
        "knack": "field_1133",
        "github": "labels",
        "method": "append",
    }, # application label
    {
        "knack": "id",
        "github": "description",
        "method": "transform_merge",
        "transform": "knack_issue_url",
        "rename": "Knack link to issue",
    }, # Link back to the knack issue
]

# key: fullDatabaseId
ISSUE_FIELDS_MAPPING = {
    5181: {"socrata_name": "estimate"},
    43035842: {"socrata_name": "description"},
    # 10226 is the status issue field, it is called pipeline in ODP and atd-product code
    10226: {"socrata_name": "pipeline", "data_type": "single_select"}
}

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
        "github": "labels",
        "method": "map_append",
        "format": "quote_text",
        "map": {
            "Active Transportation & Street Design": "Workgroup: ATSD",
            "Arterial Management": "Workgroup: AMD",
            "Community Relations & Outreach Program": "Workgroup: CRO",
            "Community Services": "Workgroup: CSD",
            "Corridor Program Development Program": "Workgroup: CPO",
            "Data & Technology Services": "Workgroup: DTS",
            "District Maintenance": "Workgroup: District Maintenance",
            "Emergency Management": "Workgroup: Emergency Management",
            "Enforcement Services": "Workgroup: Enforcement Services",
            "Finance": "Workgroup: Finance",
            "Human Resources": "Workgroup: HR",
            "Land Development Engineering": "Workgroup: Land Development Engineering",
            "Logistics": "Workgroup: Logistics",
            "Mobility Services": "Workgroup: Mobility Services",
            "Office of Performance Management": "Workgroup: OPM",
            "Office of Special Events": "Workgroup: OSE",
            "Office of the City Engineer": "Workgroup: OCE",
            "Office of the Director": "Workgroup: OOD",
            "Parking Services": "Workgroup: Parking Services",
            "Pavement Operations": "Workgroup: Pavement Operations",
            "Project Delivery": "Workgroup: PDD",
            "Public Information Office": "Workgroup: PIO",
            "Right of Way Management": "Workgroup: ROW",
            "Shared Mobility Services": "Workgroup: SMS",
            "Sidewalk & Urban Trails": "Workgroup: SUTD",
            "Signs & Markings": "Workgroup: SMD",
            "Smart Mobility Office": "Workgroup: SMO",
            "Strategic Projects Program": "Workgroup: SPP",
            "Street & Bridge Operations": "Workgroup: SBO",
            "Systems Development": "Workgroup: SDD",
            "Transportation Development Services": "Workgroup: TDS",
            "Transportation Engineering": "Workgroup: TED",
            "Urban Forestry": "Workgroup: Urban Forestry",
            "Utilities & Structures": "Workgroup: Utilities & Structures",
            "Vision Zero": "Workgroup: VZ",
            "Other": "Workgroup: Other"
        },
    }, # add Division to labels
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
        "github": "labels",
        "method": "map_append",
        "map": {
            "Team: Apps": "Team: Apps",
            "Team: Geo": "Team: Geo",
            "Team: Dev": "Team: Dev",
            "Team: Product": "Team: Product",
            "Team: Maximo": "Team: Maximo",
            "Team: Amanda": "Team: AMANDA",
            "Team: Data Science": "Team: Data Science",
            "Team: DTS Operations": "Team: DTS Operations",
            "Team: Tech Services": "Team: Tech Services",
            "[Team] :rotating_light: MISSING": "[Team] :rotating_light: MISSING",
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
        "knack": "field_1129",
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

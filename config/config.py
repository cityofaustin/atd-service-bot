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
        "knack": "field_406",
        "github": "description",
        "method": "merge",
        "format": "quote_text_hidden",
    },  # email
    {
        "knack": "field_400",
        "github": "title",
        "method": "copy",
        "format": "none",
    },  # Describe the problem (duplicated because this goes into the title and decsription body)
    {
        "knack": "field_399",  # App name
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },
    {
        "knack": "field_400",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe the problem (duplicated because this goes into the title and decsription body)
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
        "knack": "field_390",  # Division
        "github": "labels",
        "method": "map_append",
        "format": "quote_text",
        "map": {
            "Active Transportation & Street Design": "Workgroup: ATSD",
            "Arterial Management": "Workgroup: AMD",
            "Data & Technology Services": "Workgroup: DTS",
            "Finance & Administration": "Workgroup: Finance",
            "Human Resources": "Workgroup: HR",
            "Office of the Director": "Workgroup: OOD",
            "Office of Special Events": "Workgroup: OSE",
            "Parking Enterprise": "Workgroup: PE",
            "Parking Meters": "Workgroup: PE",
            "Public Information Office": "Workgroup: PIO",
            "Right-of-Way": "Workgroup: ROW",
            "Signs & Markings": "Workgroup: SMB",
            "Smart Mobility": "Workgroup: SM",
            "Systems Development": "Workgroup: SDD",
            "Transportation Engineering": "Workgroup: TE",
            "Vision Zero": "Workgroup: VZ",
            "Other": "Workgroup: Other",
        },
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
            "GIS or Maps": "Service: Geo",
            "New Project — My needs are not met by the technology & data available to me": "Type: New Application",
            "IT Support — Help with licenses, accounts, hardware, etc.": "Type: IT Support",
            "Something Else": "Type: Other",
        },
    },
    {
        "knack": "field_399",
        "github": "repo",
        "method": "map",
        "default": "atd-data-tech",
        "map": {
            "AMANDA": "atd-amanda",
            "Data Tracker": "atd-knack-data-tracker",
            "Finance & Purchasing": "atd-knack-finance-purchasing",
            "Street Banners": "atd-knack-street-banner",
            "Signs & Markings Operations": "atd-knack-signs-markings",
            "ArcGIS": "atd-geospatial",
            "Vision Zero (Editor)": "atd-vz-data",
            "Vision Zero (Viewer)": "atd-vz-data",
            "Other / Not Sure": "atd-data-tech",
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
        "knack": "field_402",
        "github": "description",
        "method": "transform_merge",
        "transform": "parse_attachment_url",
        "format": "no_label",
    },
    {"knack": "id", "github": "knack_id", "method": "copy", "format": "none"},
    {"knack": "field_388", "github": "description", "method": "merge"},  # request ID
]

ASSIGNEES = {
    # Any atd-geospatial issue assigned to Jaime
    # Any atd-amanda issue assigned to Tracy
    # New Project (aka, New Application) and "Something Else" issues to amenity & tracy
    # Severe/urgent issues assigned to amenity & tracy
    # everything else to amenity
    "severe_urgent": ["TracyLinder", "amenity"],
    "amanda": ["TracyLinder"],
    "gis": ["jaime-mckeown"],
    "new_projects": ["TracyLinder", "amenity"],
    "type_other": ["TracyLinder", "amenity"],
    "catch_all": ["amenity"],
}

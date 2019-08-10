
KNACK_APP = {
    "app_id": "595d00ebd315cc4cb98daff4",
    "api_view" : {
        "scene": "scene_127",
        "view": "view_248",
        "ref_obj": ["object_24"],
    },
    "api_form" : {
        "scene" : "scene_131",
        "view" : "view_252"
    }
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
        "format": "quote_text",
    },  # email
    {
        "knack": "field_400",
        "github": "title",
        "method": "copy",
    },  # Describe the problem
    {
        "knack": "field_412",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe workarounds
    {
        "knack": "field_411",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Describe an outcome you'd like to see
    {
        "knack": "field_390",  # Division
        "github": "labels",
        "method": "map_append",
        "format": "quote_text",
        "map": {
            "Active Transportation & Street Design": "Workgroup: ATSD",
            "Arterial Management": "Workgroup: AMD",
            "Data and Technology Services": "Workgroup: DTS",
            "Finance and Administration": "Workgroup: Finance",
            "Human Resources (Hr)": "Workgroup: HR",
            "Office of the Director": "Workgroup: OOD",
            "Office of Special Events": "Workgroup: OSE",
            "Parking Enterprise": "Workgroup: PE",
            "Parking Meters": "Workgroup: PE",
            "PIO": "Workgroup: PIO",
            "Right-of-Way (ROW)": "Workgroup: ROW",
            "Signs and Markings": "Workgroup: SMB",
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
            "Unsure" : ""
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
    },  # How soon do you need this?
    {
        "knack": "field_405",
        "github": "description",
        "method": "merge",
        "format": "quote_text",
    },  # Anything else we should know?
    {
        "knack": "field_398",  # What do you need help with?
        "github": "labels",
        "method": "map_append",
        "map": {
            "Bug Report — Something is not working": "Type: Bug Report",
            "Feature or Enhancement — An application I use could be improved": "Type: Enhancement",
            "GIS or Maps": "Type: Map Request",
            "New Project — My needs are not met by the technology & data available to me": "Type: New Application",
            "IT Support - Help with licenses, accounts, hardware, etc." : "Type: IT Support"
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
            "Other": "atd-data-tech",
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
        "knack": "id",
        "github": "description",
        "method": "transform_merge",
        "rename": "DTS URL",
        "transform": "app_url",
    },
    {
        "knack": "field_402",
        "github": "description",
        "method": "transform_merge",
        "transform": "parse_attachment_url",
        "format": "no_label",
    },
    {"knack": "id", "github": "knack_id", "method": "copy", "format" : "none"},
    {
        "knack": "field_388",  # request ID
        "github": "description",
        "method": "merge",
    },
    {
        "knack": "field_382",  # request date
        "github": "description",
        "method": "transform_merge",
        "transform": "mills_to_timestamp",
    },
]

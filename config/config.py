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
            "Project Delivery": "Workgroup: PDD",
            "Public Information Office": "Workgroup: PIO",
            "Right-of-Way": "Workgroup: ROW",
            "Signs & Markings": "Workgroup: SMD",
            "Smart Mobility Office": "Workgroup: SMO",
            "Shared Mobility Services": "Workgroup: SMS",
            "Systems Development": "Workgroup: SDD",
            "Transportation Engineering": "Workgroup: TED",
            "Transportation Development Services (TDS)": "Workgroup: TDS",
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
        "github": "labels",
        "method": "map_append",
        "map": {
            "AMANDA": "Product: AMANDA",
            "Data Tracker": "Product: AMD Data Tracker",
            "Finance & Purchasing": "Product: Finance & Purchasing",
            "Moped": "Product: Moped",
            "Street Banners": "Product: Banners",
            "Signs & Markings Operations": "Product: Signs & Markings",
            "ArcGIS": "Service: Geo",
            "Vision Zero in Action": "Product: Vision Zero in Action",
            "Vision Zero (Editor)": "Product: Vision Zero Crash Data System",
            "Vision Zero (Viewer)": "Product: Vision Zero Viewer",
            "Transportation Development Services (TDS)": "Product: TDS Portal",
            "Parking Enterprise Portal": "Product: Parking Enterprise Portal",
            "Human Resources": "Product: Human Resources",
            "Shared Mobility Operations": "Product: Shared Mobility Operations",
            "Right-of-Way (ROW) Portal": "Product: ROW Portal",
            "Residential Parking Permits (RPP)": "Product: Residential Parking Permits (RPP)",
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
        "format": "no_label",
    },
    {"knack": "id", "github": "knack_id", "method": "copy", "format": "none"},
    {"knack": "field_388", "github": "description", "method": "merge"},  # request ID
]

ASSIGNEES = {
    "severe_urgent": [
        "TracyLinder",
        "amenity",
        "dianamartin",
        "SurbhiBakshi",
        "Nadin-Nader",
    ],
    "amanda": ["TracyLinder", "Nadin-Nader"],
    "gis": ["jaime-mckeown", "alan-deanda"],
    "new_projects": ["TracyLinder", "amenity"],
    "type_other": ["TracyLinder", "amenity", "dianamartin", "SurbhiBakshi"],
    "catch_all": ["amenity", "dianamartin", "SurbhiBakshi"],
}

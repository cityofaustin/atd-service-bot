'''
schema dict of the issueFields we have configured on atd-data-tech repo
used as reference
'''
issue_fields = {
	"data": {
		"repository": {
			"issueFields": {
				"nodes": [
					{
						"__typename": "IssueFieldDate",
						"description": "The date when work on project or epic will begin",
						"id": "IFD_kgDNFCo",
						"name": "DTS Start Date",
						"fullDatabaseId": "5162"
					},
					{
						"__typename": "IssueFieldDate",
						"description": "The expected completion date for this project or epic",
						"id": "IFD_kgDNFCs",
						"name": "DTS End Date",
						"fullDatabaseId": "5163"
					},
					{
						"__typename": "IssueFieldNumber",
						"name": "DTS Estimate-1 2 3 5 8 13",
						"description": "1, 2, 3, 5, 8, or 13 - represents the level of effort based upon complexity, certainty, and time ",
						"dataType": "NUMBER",
						"id": "IFN_kgDNFD0",
						"fullDatabaseId": "5181"
					},
					{
						"__typename": "IssueFieldSingleSelect",
						"id": "IFSS_kgDNGXg",
						"description": "The primary Data and Technology Services team executing this task or supporting this service",
						"name": "DTS Team",
						"fullDatabaseId": "6520",
						"options": [
							{
								"id": "IFSSO_kgDNH3M",
								"name": "Apps",
								"databaseId": 8051,
								"fullDatabaseId": "8051"
							},
							{
								"id": "IFSSO_kgDNH3Q",
								"name": "Data Science",
								"databaseId": 8052,
								"fullDatabaseId": "8052"
							},
							{
								"id": "IFSSO_kgDNH3U",
								"name": "Dev",
								"databaseId": 8053,
								"fullDatabaseId": "8053"
							},
							{
								"id": "IFSSO_kgDNH3Y",
								"name": "ECM",
								"databaseId": 8054,
								"fullDatabaseId": "8054"
							},
							{
								"id": "IFSSO_kgDNH3c",
								"name": "Geo",
								"databaseId": 8055,
								"fullDatabaseId": "8055"
							},
							{
								"id": "IFSSO_kgDNH3g",
								"name": "Maximo",
								"databaseId": 8056,
								"fullDatabaseId": "8056"
							},
							{
								"id": "IFSSO_kgDNH3k",
								"name": "Product",
								"databaseId": 8057,
								"fullDatabaseId": "8057"
							},
							{
								"id": "IFSSO_kgDNH3o",
								"name": "Tech Services",
								"databaseId": 8058,
								"fullDatabaseId": "8058"
							},
							{
								"id": "IFSSO_kgDNH3s",
								"name": "Operations",
								"databaseId": 8059,
								"fullDatabaseId": "8059"
							}
						]
					},
					{
						"__typename": "IssueFieldSingleSelect",
						"id": "IFSS_kgDNJ_I",
						"description": "The status of the task, project, or epic — \"Ongoing\" for products and services",
						"name": "DTS Status",
						"fullDatabaseId": "10226",
						"options": [
							{
								"id": "IFSSO_kgDNOPE",
								"name": "New",
								"databaseId": 14577,
								"fullDatabaseId": "14577"
							},
							{
								"id": "IFSSO_kgDNOPM",
								"name": "Needs Scoping",
								"databaseId": 14579,
								"fullDatabaseId": "14579"
							},
							{
								"id": "IFSSO_kgDNOPQ",
								"name": "Backlog",
								"databaseId": 14580,
								"fullDatabaseId": "14580"
							},
							{
								"id": "IFSSO_kgDNOPU",
								"name": "On Deck",
								"databaseId": 14581,
								"fullDatabaseId": "14581"
							},
							{
								"id": "IFSSO_kgDNOPY",
								"name": "In Progress",
								"databaseId": 14582,
								"fullDatabaseId": "14582"
							},
							{
								"id": "IFSSO_kgDNOPg",
								"name": "Review/QA",
								"databaseId": 14584,
								"fullDatabaseId": "14584"
							},
							{
								"id": "IFSSO_kgDNOPc",
								"name": "Blocked",
								"databaseId": 14583,
								"fullDatabaseId": "14583"
							},
							{
								"id": "IFSSO_kgDOBJ2T6g",
								"name": "Closed",
								"databaseId": 77435882,
								"fullDatabaseId": "77435882"
							},
							{
								"id": "IFSSO_kgDOBGoLHg",
								"name": "Ongoing",
								"databaseId": 74058526,
								"fullDatabaseId": "74058526"
							},
							{
								"id": "IFSSO_kgDNOPI",
								"name": "Icebox",
								"databaseId": 14578,
								"fullDatabaseId": "14578"
							}
						]
					},
					{
						"__typename": "IssueFieldText",
						"name": "DTS Description",
						"id": "IFT_kgDOApCswg",
						"description": "The high-level explanation of a product, project, or service",
						"fullDatabaseId": "43035842"
					},
					{
						"__typename": "IssueFieldText",
						"name": "DTS Application URL",
						"id": "IFT_kgDOAqM5cg",
						"description": "The end-user web address for a DTS application — will be rendered as a hyperlink",
						"fullDatabaseId": "44251506"
					},
					{
						"__typename": "IssueFieldMultiSelect",
						"description": "The Transportation and Public Works divisions served by this product, project, or service",
						"name": "TPW Divisions",
						"id": "IFMS_kgDOAqhdUg",
						"fullDatabaseId": "44588370",
						"options": [
							{
								"id": "IFSSO_kgDOBKa-ug",
								"name": "Admin",
								"databaseId": 78036666,
								"fullDatabaseId": "78036666",
								"description": "Administration"
							},
							{
								"id": "IFSSO_kgDOBKdv-g",
								"name": "AMD",
								"databaseId": 78082042,
								"fullDatabaseId": "78082042",
								"description": "Arterial Management"
							},
							{
								"id": "IFSSO_kgDOBKdv-w",
								"name": "ATSD",
								"databaseId": 78082043,
								"fullDatabaseId": "78082043",
								"description": "Active Transportation & Street Design"
							},
							{
								"id": "IFSSO_kgDOBKdv_A",
								"name": "CCG",
								"databaseId": 78082044,
								"fullDatabaseId": "78082044",
								"description": "Construction Coordination Group"
							},
							{
								"id": "IFSSO_kgDOBKdv_Q",
								"name": "CSD",
								"databaseId": 78082045,
								"fullDatabaseId": "78082045",
								"description": "Community Services"
							},
							{
								"id": "IFSSO_kgDOBKdv_g",
								"name": "DM",
								"databaseId": 78082046,
								"fullDatabaseId": "78082046",
								"description": "District Maintenance"
							},
							{
								"id": "IFSSO_kgDOBKdv_w",
								"name": "DTS",
								"databaseId": 78082047,
								"fullDatabaseId": "78082047",
								"description": "Data & Technology Services"
							},
							{
								"id": "IFSSO_kgDOBKdwAA",
								"name": "EM",
								"databaseId": 78082048,
								"fullDatabaseId": "78082048",
								"description": "Emergency Management"
							},
							{
								"id": "IFSSO_kgDOBKdwAQ",
								"name": "Equity",
								"databaseId": 78082049,
								"fullDatabaseId": "78082049",
								"description": "Equity"
							},
							{
								"id": "IFSSO_kgDOBKdwAg",
								"name": "Finance",
								"databaseId": 78082050,
								"fullDatabaseId": "78082050",
								"description": "Finance"
							},
							{
								"id": "IFSSO_kgDOBKdwAw",
								"name": "HR",
								"databaseId": 78082051,
								"fullDatabaseId": "78082051",
								"description": "Human Resources"
							},
							{
								"id": "IFSSO_kgDOBKdwBA",
								"name": "LA",
								"databaseId": 78082052,
								"fullDatabaseId": "78082052",
								"description": "Legislative Affairs"
							},
							{
								"id": "IFSSO_kgDOBKdwBg",
								"name": "LDE",
								"databaseId": 78082054,
								"fullDatabaseId": "78082054",
								"description": "Land Development Engineering"
							},
							{
								"id": "IFSSO_kgDOBKdwCA",
								"name": "Logistics",
								"databaseId": 78082056,
								"fullDatabaseId": "78082056",
								"description": "Logistics"
							},
							{
								"id": "IFSSO_kgDOBKdwCg",
								"name": "OCE",
								"databaseId": 78082058,
								"fullDatabaseId": "78082058",
								"description": "Office of the City Engineer"
							},
							{
								"id": "IFSSO_kgDOBKdwDA",
								"name": "OPM",
								"databaseId": 78082060,
								"fullDatabaseId": "78082060",
								"description": "Office of Performance Management"
							},
							{
								"id": "IFSSO_kgDOBKdwDQ",
								"name": "OSE",
								"databaseId": 78082061,
								"fullDatabaseId": "78082061",
								"description": "Office of Special Events"
							},
							{
								"id": "IFSSO_kgDOBKdwDg",
								"name": "PD",
								"databaseId": 78082062,
								"fullDatabaseId": "78082062",
								"description": "Project Delivery"
							},
							{
								"id": "IFSSO_kgDOBKdwDw",
								"name": "PE",
								"databaseId": 78082063,
								"fullDatabaseId": "78082063",
								"description": "Parking Enterprise"
							},
							{
								"id": "IFSSO_kgDOBKdwEA",
								"name": "PIO",
								"databaseId": 78082064,
								"fullDatabaseId": "78082064",
								"description": "Public Information Office"
							},
							{
								"id": "IFSSO_kgDOBKdwEQ",
								"name": "PO",
								"databaseId": 78082065,
								"fullDatabaseId": "78082065",
								"description": "Pavement Operations"
							},
							{
								"id": "IFSSO_kgDOBKdwEw",
								"name": "ROW",
								"databaseId": 78082067,
								"fullDatabaseId": "78082067",
								"description": "Right-of-Way Management"
							},
							{
								"id": "IFSSO_kgDOBKdwFQ",
								"name": "SBO",
								"databaseId": 78082069,
								"fullDatabaseId": "78082069",
								"description": "Infrastructure Operations"
							},
							{
								"id": "IFSSO_kgDOBKdwFw",
								"name": "SDD",
								"databaseId": 78082071,
								"fullDatabaseId": "78082071",
								"description": "Systems Development"
							},
							{
								"id": "IFSSO_kgDOBKdwGA",
								"name": "SMD",
								"databaseId": 78082072,
								"fullDatabaseId": "78082072",
								"description": "Signs & Markings"
							},
							{
								"id": "IFSSO_kgDOBKdwGQ",
								"name": "SMP",
								"databaseId": 78082073,
								"fullDatabaseId": "78082073",
								"description": "Strategic Mobility Projects"
							},
							{
								"id": "IFSSO_kgDOBKdwGg",
								"name": "SP",
								"databaseId": 78082074,
								"fullDatabaseId": "78082074",
								"description": "Strategic Projects"
							},
							{
								"id": "IFSSO_kgDOBKdwGw",
								"name": "SUTD",
								"databaseId": 78082075,
								"fullDatabaseId": "78082075",
								"description": "Sidewalks & Urban Trails Division"
							},
							{
								"id": "IFSSO_kgDOBKdwHA",
								"name": "TDS",
								"databaseId": 78082076,
								"fullDatabaseId": "78082076",
								"description": "Transportation Development Services"
							},
							{
								"id": "IFSSO_kgDOBKdwHQ",
								"name": "TED",
								"databaseId": 78082077,
								"fullDatabaseId": "78082077",
								"description": "Transportation Engineering"
							},
							{
								"id": "IFSSO_kgDOBKdwHg",
								"name": "UF",
								"databaseId": 78082078,
								"fullDatabaseId": "78082078",
								"description": "Urban Forestry"
							},
							{
								"id": "IFSSO_kgDOBKdwHw",
								"name": "US",
								"databaseId": 78082079,
								"fullDatabaseId": "78082079",
								"description": "Utilities & Structures"
							},
							{
								"id": "IFSSO_kgDOBKdwIA",
								"name": "VZ",
								"databaseId": 78082080,
								"fullDatabaseId": "78082080",
								"description": "Vision Zero"
							},
							{
								"id": "IFSSO_kgDOBKdwIQ",
								"name": "TPW",
								"databaseId": 78082081,
								"fullDatabaseId": "78082081",
								"description": "Transportation Public Works"
							}
						]
					},
					{
						"__typename": "IssueFieldSingleSelect",
						"id": "IFSS_kgDOAqww1g",
						"description": "The product's primary type of technology platform",
						"name": "DTS Solution Type",
						"fullDatabaseId": "44839126",
						"options": [
							{
								"id": "IFSSO_kgDOBK115g",
								"name": "Esri",
								"databaseId": 78476774,
								"fullDatabaseId": "78476774"
							},
							{
								"id": "IFSSO_kgDOBK115w",
								"name": "Custom",
								"databaseId": 78476775,
								"fullDatabaseId": "78476775"
							},
							{
								"id": "IFSSO_kgDOBK116A",
								"name": "Knack",
								"databaseId": 78476776,
								"fullDatabaseId": "78476776"
							},
							{
								"id": "IFSSO_kgDOBK116Q",
								"name": "PowerBI",
								"databaseId": 78476777,
								"fullDatabaseId": "78476777"
							},
							{
								"id": "IFSSO_kgDOBK116g",
								"name": "Other",
								"databaseId": 78476778,
								"fullDatabaseId": "78476778"
							}
						]
					},
					{
						"__typename": "IssueFieldMultiSelect",
						"description": "The Data and Technology Services teams supporting this product, project, or epic",
						"name": "DTS Teams",
						"id": "IFMS_kgDOArXZgw",
						"fullDatabaseId": "45472131",
						"options": [
							{
								"id": "IFSSO_kgDOBL5stA",
								"name": "Apps",
								"databaseId": 79588532,
								"fullDatabaseId": "79588532",
								"description": "Application Solutions"
							},
							{
								"id": "IFSSO_kgDOBL5stQ",
								"name": "Data Science",
								"databaseId": 79588533,
								"fullDatabaseId": "79588533",
								"description": "Data Science Solutions"
							},
							{
								"id": "IFSSO_kgDOBL5stg",
								"name": "Dev",
								"databaseId": 79588534,
								"fullDatabaseId": "79588534",
								"description": "Software Engineering"
							},
							{
								"id": "IFSSO_kgDOBL5stw",
								"name": "ECM",
								"databaseId": 79588535,
								"fullDatabaseId": "79588535",
								"description": "Enterprise Case Management"
							},
							{
								"id": "IFSSO_kgDOBL5suA",
								"name": "Geo",
								"databaseId": 79588536,
								"fullDatabaseId": "79588536",
								"description": "Geospatial Solutions"
							},
							{
								"id": "IFSSO_kgDOBL5suQ",
								"name": "Maximo",
								"databaseId": 79588537,
								"fullDatabaseId": "79588537",
								"description": "Maximo"
							},
							{
								"id": "IFSSO_kgDOBL5sug",
								"name": "Product",
								"databaseId": 79588538,
								"fullDatabaseId": "79588538",
								"description": "Product Managment"
							},
							{
								"id": "IFSSO_kgDOBL5suw",
								"name": "Tech Services",
								"databaseId": 79588539,
								"fullDatabaseId": "79588539",
								"description": "Technology Services"
							},
							{
								"id": "IFSSO_kgDOBL5svA",
								"name": "Operations",
								"databaseId": 79588540,
								"fullDatabaseId": "79588540",
								"description": "Administrative work including budgeting, team management, departmental reporting"
							}
						]
					}
				]
			}
		}
	}
}

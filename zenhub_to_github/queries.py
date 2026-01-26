# paginated request to get all issues from our zenhub workspace, with their labels, estimate and pipeline position
zh_estimates_query = """
  query workspaceIssues($workspaceId: ID!, $after: String) {
      workspace(id: $workspaceId) { 
        issues(after: $after) {
              totalCount
              nodes {
                  id
                  number
                  title
                  labels {
                    nodes {
                      name
                      id
                    }
                  }
                  estimate {
                      value
                  }
                  pipelineIssue(workspaceId:$workspaceId){
                      pipeline {
                          id
                          name
                      }
                  }
              }
              pageInfo {
                  hasNextPage
                  endCursor
              }
          }
      }
  }
"""

# gets the fields from only the geo project board
gh_geo_fields_query = """
  query GeoIssues {
    organization(login: "cityofaustin") {
      projectV2(number: 6) {
        id
        title
        fields(first:20) {
          totalCount
          nodes {
            ... on ProjectV2Field {
              id
              name
              dataType
            }
            ... on ProjectV2IterationField {
              id
              name
              dataType
            }
            ... on ProjectV2SingleSelectField {
              id
              name
              dataType
              options {
                id
                name
                color
              }
            }					
          }
        }
      }
    }
  }

"""

# gets all field ids from all github projects under our organization
gh_projects_fields_query = """
query ProjectsFields {
	organization(login: "cityofaustin") {
		projectsV2(first:20) {
			totalCount
			nodes {
			id
			closed
			title
			fields(first:20) {
				totalCount
				nodes {
          ... on ProjectV2Field {
            id
            name
            dataType
          }
          ... on ProjectV2IterationField {
            id
            name
            dataType
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            dataType
            options {
              id
              name
              color
            }
          }					
				}
			}
		}
	}
}
}
"""

# zenhub - gets all issues labeled with "service: geo" by pipeline
# i dont know why you can only filter by label in the searchIssuesByPipeline query
geo_pipeline_query = """
  query workspaceIssues($pipelineId: ID!) {
    searchIssuesByPipeline(
      pipelineId: $pipelineId,
      filters: {
        labels: { in: ["Service: Geo"]}
      }
    ) { 
      totalCount
      nodes {
        id
        title
        number
        estimate {
          id
          value
        }
        pipelineIssues {
          nodes {
            pipeline {
              name
              id
            }
          }
			  }
      }
    }
  }
"""

all_geo_issues_ghp = """
  query GeoIssues($cursor: String) {
    organization(login: "cityofaustin") {
      projectV2(number: 6) {
        items(after: $cursor) {
          totalCount
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            content {
              ... on Issue {
                url
                title
                number
                id
                updatedAt
              }
            }
            estimate: fieldValueByName(name: "Estimate") {
              ... on ProjectV2ItemFieldNumberValue {
                number
              }
            }
            status: fieldValueByName(name: "Status") {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                description
              }
            }
          }
        }
      }
    }
  }
"""

# update_field_value_mutation = """
# mutation { updateProjectV2ItemFieldValue(input: {
#       projectId: "PVT_kwDOAEpV4M4BBib3", # geo board
#       itemId: "I_kwDOCGHL5s7IhSUr"
#       fieldId: "PVTF_lADOAEpV4M4BBib3zg0A61c" # field id for estimate on geo board
#       value: {
#         number: 4
#       }
#     }) { clientMutationId } }"
#   }'


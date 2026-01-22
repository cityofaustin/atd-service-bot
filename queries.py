# paginated request to get all issues from our workspace, with their labels, estimate and pipeline position
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

# zenhub
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

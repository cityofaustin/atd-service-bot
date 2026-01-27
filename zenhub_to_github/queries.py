zenhub_labeled_pipeline_query = """
query workspaceIssues($pipelineId: ID!, $label: String!, $endCursor: String) {
  searchIssuesByPipeline(
    pipelineId: $pipelineId,
    filters: {
      labels: { in: [$label]}
    },
    first: 100,
    after: $endCursor
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
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

closed_zenhub_issues = """
query workspaceClosedIssues($workspaceId: ID!, $label: String!, $endCursor: String) {
  searchClosedIssues(
    workspaceId: $workspaceId,
    filters: {
      labels: { in: [$label]}
    },
    first: 100,
    after: $endCursor
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
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


all_issues_github_project_board = """
  query GeoIssues($cursor: String, $boardId: Int!) {
    organization(login: "cityofaustin") {
      projectV2(number: $boardId) {
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

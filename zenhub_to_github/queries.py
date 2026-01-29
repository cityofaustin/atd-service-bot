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
      repository {
        id
        name
        ghId
      }
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
      repository {
        id
        name
        ghId
      }
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

get_github_node_id = """
query GetIssueNodeId($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      id
      number
      title
      state
    }
  }
}
"""


add_issue_to_github_project_mutation = """
mutation AddProjectItem($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item {
      id
    }
  }
}
"""


github_project_field_value_mutation = """
mutation UpdateProjectItemField($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: Float!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: {
      number: $value
    }
  }) {
    projectV2Item {
      id
    }
  }
}
"""




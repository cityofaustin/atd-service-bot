issue_estimates_status_query = """
query ProjectIssues($boardID: Int!, $cursor: String) {
  organization(login: "cityofaustin") {
    projectV2(number: $boardID) {
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
              title
              number
              issueType {
								id
								name
              }
          issueFieldValues(first: 5) {
                nodes {
                  __typename
                  ... on IssueFieldSingleSelectValue {
                    name
                    field {
                      ... on IssueFieldSingleSelect {
                        name
                        id
                        fullDatabaseId
                      }
                    }
                  }
                  ... on IssueFieldNumberValue {
                    field {
                      ... on IssueFieldNumber {
                        name
                        id
                        fullDatabaseId
                      }
                    }
                  }
                }
              }
            }
          }
          status: fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
              description
            }
          }
				 estimate: fieldValueByName(name: "Estimate") {
					... on ProjectV2ItemFieldNumberValue {
						id
						number
					}
				}
        }
      }
    }
  }
}
"""

issue_team_label_query = """
query($searchQuery: String!, $first: Int!, $cursor:String) {
  search(query: $searchQuery, type: ISSUE, first: $first, after: $cursor) {
    issueCount
    pageInfo {
			hasNextPage
			endCursor
		}
    nodes {
      ... on Issue {
        number
				id
        title
        url
        state
        labels(first: 10) {
          nodes {
            name
          }
        }
      }
    }
  }
}
"""

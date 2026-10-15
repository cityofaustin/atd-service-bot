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
            ... on PullRequest {
              title
              isPullRequest: title
              number
              merged
              closed
            }
            ... on Issue {
              title
              number
              closed
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
                    value
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
				 estimate: fieldValueByName(name: "Estimate - 1, 2, 3, 5, 8, or 13") {
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

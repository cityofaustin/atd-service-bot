all_project_issues_ghp = """
  query ProjectIssues($cursor: String) {
    organization(login: "cityofaustin") {
      projectV2(number: 11) {
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

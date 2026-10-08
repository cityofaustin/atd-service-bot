ISSUE_FIELDS_QUERY = """
{
  repository(owner: "cityofaustin", name: "atd-data-tech") {
    issueFields(first: 25) {
      nodes {
        __typename
        ... on IssueFieldNumber {
          name
          description
          dataType
          id
          fullDatabaseId
        }
        ... on IssueFieldMultiSelect {
          description
          name
          id
          fullDatabaseId
          options {
            id
            name
            databaseId
            fullDatabaseId
            description
          }
        }
        ... on IssueFieldDate {
          description
          id
          name
          fullDatabaseId
        }
        ... on IssueFieldSingleSelect {
          id
          description
          name
          fullDatabaseId
          options {
            id
            name
            databaseId
            fullDatabaseId
          }
        }
        ... on IssueFieldText {
          name
          id
          description
          fullDatabaseId
        }
      }
    }
  }
}
"""

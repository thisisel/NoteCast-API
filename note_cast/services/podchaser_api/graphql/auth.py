from python_graphql_client import GraphqlClient
from . import base_graphql_path
# Create your query or mutation.
access_token_query = """
mutation {
    requestAccessToken(
        input: {
            grant_type: CLIENT_CREDENTIALS
            client_id: "YOUR_ID"
            client_secret: "YOUR_SECRET"
        }
    ) {
        access_token
    }
}
"""

# Execute the GraphQL call using our API's endpoint and your query.
response = GraphqlClient(endpoint=base_graphql_path).execute(query=access_token_query)

# Access the returned data.
access_token = response['data']['requestAccessToken']['access_token']
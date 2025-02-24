### 1. **Create an OpenSearch Domain**
OpenSearch is used to store and index log data for fast querying and search capabilities.

- Go to the AWS Console → Services → OpenSearch Service.
- Click Create Domain.
- Choose Domain Type: Select Development and testing for small-scale use.
- Domain Name: log-analysis
- Version: Choose the latest available version (e.g., 2.x).
- Cluster Configuration: Select a single-node configuration for small-scale testing.
- Set up Access: 
  - Access Policy: Select Allow open access (for testing purposes).
  - For production, use IAM policies or VPC-based access.
- Click Create Domain.

- Note: After creation, you'll get the Domain Endpoint URL like: https://your-opensearch-domain-name.us-west-2.es.amazonaws.com.


### 2. **Create an Index in OpenSearch**

- Open OpenSearch Dashboards via the Domain Endpoint.
- In the Dev Tools section, run the following command to create an index:

```bash
PUT /logs-index
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "user_id": { "type": "keyword" },
      "action": { "type": "keyword" },
      "page": { "type": "keyword" },
      "status_code": { "type": "integer" },
      "amount_spent": { "type": "float" }
    }
  }
}
```

This creates an index named logs-index, with fields such as timestamp, user_id, action, etc.

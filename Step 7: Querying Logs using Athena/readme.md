### **Clone the Repo Locally**

1.	Set Up Athena:
  - Go to AWS Console → Athena.
  - Query Result Location: Set it to an S3 bucket, e.g., s3://your-athena-results/.
  - Choose the log-database created in Glue.

2.	Run SQL Query:
  - In the Query Editor, select the logs_table from the Glue Catalog.
  - Run a sample query:

3.	SELECT * FROM logs_table WHERE action = 'purchase';


### **Expected Output:**
```bash
timestamp              | user_id | action   | page       | status_code | amount_spent
---------------------- | ------- | -------- | ---------- | ----------- | ------------
2025-02-16T10:20:30Z  | U123    | purchase | checkout   | 200         | 29.99
```

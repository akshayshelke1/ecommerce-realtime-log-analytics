### **AWS Glue setup**
Glue is used to create a catalog for the raw logs in S3, so they can be easily queried using Athena.

**1. Create a Glue Crawler**

1.	Go to the AWS Console → Services → Glue → Crawlers.
2.	Click Add Crawler.
3.	Crawler Name: log-crawler.
4.	Data Store: Choose S3 and specify the path where logs are stored, e.g., s3://my-log-bucket/.
5.	IAM Role: Create a new role or choose an existing one with the necessary Glue permissions.
6.	Choose Run On Demand for testing purposes.
7.	Output Database: Choose or create a new database (e.g., log-database).
8.	Click Next and Finish.

After the crawler runs, it creates metadata tables in the Glue Catalog.

**2. Check Glue Catalog**

1.	Go to AWS Glue → Databases → log-database.
2.	You should see a table like logs_table, representing the raw log files in S3.

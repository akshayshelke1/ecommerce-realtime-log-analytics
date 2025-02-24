### **Set Up S3 for Data Storage**

**Create an S3 Bucket:**

- Go to the AWS S3 Console: S3 Console.
- Click Create Bucket.
- Name your bucket (e.g., my-build-bucket) and choose a region.
- Leave the other settings as default and click Create.
- Upload Sample Data.

**Test Input (Sample Log File):**

Upload some sample log files (e.g., .log, .csv, or .json) to the bucket.

```bash
timestamp,user_id,action,page,status_code,amount_spent
2025-02-16T10:15:30Z,U123,view,homepage,200,0
2025-02-16T10:20:30Z,U123,purchase,checkout,200,29.99
```

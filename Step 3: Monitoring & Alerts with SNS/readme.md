### **Create SNS Topic**
📍 AWS Console → SNS
- Create Topic: log-pipeline-alerts
- Subscribe: Email/SMS
- Attach to CodePipeline & Lambda: 
  - In CodePipeline → Edit → Add Notification Rule.
  - In CloudWatch → Alarms for Lambda errors → Attach SNS Topic.

### **Create SNS Topic**

SNS is used to send notifications for pipeline status and Lambda errors.

📍 AWS Console → SNS


- Create Topic: log-pipeline-alerts
- Subscribe: Email/SMS
- Attach to CodePipeline & Lambda: 
  - In CodePipeline → Edit → Add Notification Rule.
  - In CloudWatch → Alarms for Lambda errors → Attach SNS Topic.

-----------------------------------


### **Create an SNS Topic**

1.	Go to AWS Console → Services → SNS → Topics → Create Topic.
2.	Type: Choose Standard.
3.	Topic Name: log-pipeline-alerts.
4.	Click Create Topic.
   
### **Subscribe to the SNS Topic**

1.	Click on the newly created log-pipeline-alerts topic.
2.	Create Subscription.
3.	Choose the protocol: Email or SMS.
4.	Enter your email address or phone number.
5.	Click Create Subscription.
6.	Confirm the subscription by clicking the link in the email or responding to the SMS.

### **Attach SNS to Lambda or CodePipeline**

To trigger SNS notifications on pipeline failure or Lambda errors:

- Attach SNS to CodePipeline
1.	Go to AWS Console → Services → CodePipeline.
2.	Edit your pipeline and go to the Edit Notification Rule.
3.	Select Failed/Successful pipeline notifications.
4.	Choose the SNS topic log-pipeline-alerts.

- Attach SNS to Lambda Errors
1.	Go to CloudWatch → Alarms → Create Alarm.
2.	Choose the Lambda function metric (e.g., Errors).
3.	Set the condition (e.g., when errors exceed 1).
4.	Select the SNS topic log-pipeline-alerts.
5.	Click Create Alarm.

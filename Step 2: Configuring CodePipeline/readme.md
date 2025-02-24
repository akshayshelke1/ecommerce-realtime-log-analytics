### 1. **Create Build Specification (buildspec.yml)**

CodeBuild uses this to:
- Install dependencies inside the deployment package
- Package the Lambda function

```bash
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
    commands:
      - echo Installing dependencies...
      - pip install boto3 opensearch-py -t .

  build:
    commands:
      - echo Packaging the Lambda function...
      - zip -r deployment.zip . 

artifacts:
  files:
    - deployment.zip
  discard-paths: yes
  base-directory: .
```

### 2. **Create Deployment Specification (appspec.yml)**

CodeDeploy uses this to:
- Deploy the Lambda function with a blue/green strategy

```bash
version: 0.0
Resources:
  - myLambdaFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: process-log-lambda
        Alias: live
        CurrentVersion: 1
        TargetVersion: 2
```

### 3. **Push Code to GitHub**

```bash
git add .
git commit -m "Initial commit with Lambda, buildspec, and appspec"
git push origin main
```

### 4. **Create CodePipeline**

📍 AWS Console → CodePipeline → Create Pipeline

- Pipeline Name: ecommerce-log-pipeline
- Service Role: Create a new role or use an existing one with permissions: 
o	AmazonS3FullAccess
o	AWSCodePipelineFullAccess
o	AWSCodeBuildAdminAccess
o	AWSCodeDeployFullAccess
- Artifact Store: Use a new S3 bucket or select an existing one.

### 5. **Source Stage: GitHub**

- Source Provider: GitHub (Version 2)
- Repository: ecommerce-log-pipeline
- Branch: main
- Trigger: GitHub Webhook (Triggers on code push)

### 6. **Build Stage: CodeBuild**

📍 AWS Console → CodeBuild → Create Project 
- Name: ecommerce-log-build
- Environment: 
o	OS: Ubuntu
o	Runtime: Standard: 6.0
o	Buildspec: Use buildspec.yml in the repo
- Artifacts: 
o	Type: S3
o	Bucket: my-build-bucket


### 7. **Deploy Stage: CodeDeploy**

- Deploy Provider: AWS CodeDeploy
- Application Name: ecommerce-log-app
- Deployment Group: ecommerce-log-deployment-group
- Service Role: Attach the AWSLambdaFullAccess policy.

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

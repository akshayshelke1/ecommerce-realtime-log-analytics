Here’s the Terraform code to create the full pipeline using AWS services (OpenSearch, Glue, Athena, S3, Lambda, SNS, CodePipeline, CodeBuild, CodeDeploy) for the e-commerce log processing pipeline. This will automate the provisioning of resources.

### 1. **Provider and Initialization**

First, define the AWS provider and set the region.

```bash
provider "aws" {
  region = "us-west-2" # Change to your desired region
}
```

### 2. **Create S3 Buckets**

We’ll need two S3 buckets: one for log storage and one for CodePipeline artifacts.

```bash
resource "aws_s3_bucket" "log_bucket" {
  bucket = "ecommerce-log-bucket"
  acl    = "private"
}

resource "aws_s3_bucket" "pipeline_bucket" {
  bucket = "ecommerce-pipeline-bucket"
  acl    = "private"
}
```

### 3. **Create OpenSearch Domain**

Define an OpenSearch domain for indexing logs.

```bash
resource "aws_opensearch_domain" "log_domain" {
  domain_name = "log-analysis"
  elasticsearch_version = "7.10"
  cluster_config {
    instance_type = "t3.small.search"
    instance_count = 1
  }
  ebs {
    volume_size = 10
    volume_type = "gp2"
  }

  access_policies = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Principal = "*"
        Action   = "es:*"
        Resource = "*"
      }
    ]
  })
}
```

### 4. **Create Lambda Function**

Create a Lambda function that will process logs from S3 and push them to OpenSearch.

```bash
resource "aws_lambda_function" "process_log_lambda" {
  function_name = "process-log-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = "deployment.zip"

  source_code_hash = filebase64sha256("deployment.zip")
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
      Effect    = "Allow"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  role   = aws_iam_role.lambda_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject"]
        Resource = "arn:aws:s3:::ecommerce-log-bucket/*"
        Effect   = "Allow"
      },
      {
        Action   = "es:IndexDocument"
        Resource = "${aws_opensearch_domain.log_domain.arn}/*"
        Effect   = "Allow"
      }
    ]
  })
}
```

### 5. **Create Glue Crawler**

Create a Glue Crawler to catalog the log data stored in S3.

```bash
resource "aws_glue_crawler" "log_crawler" {
  name          = "log-crawler"
  role          = aws_iam_role.glue_role.arn
  database_name = "log-database"
  targets {
    s3_target {
      path = "s3://${aws_s3_bucket.log_bucket.bucket}"
    }
  }
}

resource "aws_iam_role" "glue_role" {
  name               = "glue-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = { Service = "glue.amazonaws.com" }
      Effect    = "Allow"
    }]
  })
}

resource "aws_iam_role_policy" "glue_policy" {
  role   = aws_iam_role.glue_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject"]
        Resource = "arn:aws:s3:::ecommerce-log-bucket/*"
        Effect   = "Allow"
      },
      {
        Action   = ["glue:*"]
        Resource = "*"
        Effect   = "Allow"
      }
    ]
  })
}
```

### 6. ** Create Athena Database **

Define an Athena database where Glue will store the schema of your logs.

```bash
resource "aws_athena_database" "log_database" {
  name   = "log-database"
  bucket = aws_s3_bucket.pipeline_bucket.bucket
}
```

### 7. **Create SNS Topic **

Set up an SNS topic to notify users of pipeline events.

```bash
resource "aws_sns_topic" "log_pipeline_alerts" {
  name = "log-pipeline-alerts"
}

resource "aws_sns_topic_subscription" "sns_email_subscription" {
  topic_arn = aws_sns_topic.log_pipeline_alerts.arn
  protocol  = "email"
  endpoint  = "your-email@example.com"  # Change to your email
}
```

### 8. **  Create CodeBuild Project **

Define the build process for the Lambda function.

```bash
resource "aws_codebuild_project" "log_build" {
  name          = "ecommerce-log-build"
  description   = "Build the Lambda function for log processing"
  build_timeout = 5

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/python:3.9"
    type            = "LINUX_CONTAINER"
    environment_variable {
      name  = "AWS_REGION"
      value = "us-west-2"
    }
  }

  artifacts {
    type = "ZIP"
    location = "s3://${aws_s3_bucket.pipeline_bucket.bucket}/codebuild-artifacts/"
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/your-username/ecommerce-log-pipeline.git"
    buildspec       = "buildspec.yml"
    git_clone_depth = 1
  }
}
```
### 9. **  Create CodeDeploy Application **

This defines how CodeDeploy will handle Lambda function deployments.

```bash
resource "aws_codedeploy_app" "log_deploy_app" {
  name = "ecommerce-log-app"
}

resource "aws_codedeploy_deployment_group" "log_deploy_group" {
  app_name               = aws_codedeploy_app.log_deploy_app.name
  deployment_group_name  = "ecommerce-log-deployment-group"
  service_role_arn       = aws_iam_role.lambda_role.arn
  deployment_style {
    deployment_type = "IN_PLACE"
    update_outdated_instances_only = true
  }
  auto_rollback_configuration {
    failed_event = true
  }
}
```
### 10. **Create CodePipeline **

This will define the entire pipeline from source to build to deploy.

```bash
resource "aws_codepipeline" "log_pipeline" {
  name     = "ecommerce-log-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.pipeline_bucket.bucket
    type     = "S3"
  }

  stages {
    name = "Source"
    actions {
      name          = "Source"
      action_type_id {
        category = "Source"
        owner    = "ThirdParty"
        provider = "GitHub"
        version  = "1"
      }
      output_artifacts = ["SourceOutput"]
      configuration = {
        Owner      = "your-username"
        Repo       = "ecommerce-log-pipeline"
        Branch     = "main"
        OAuthToken = "your-github-oauth-token"
      }
    }
  }

  stages {
    name = "Build"
    actions {
      name          = "Build"
      action_type_id {
        category = "Build"
        owner    = "AWS"
        provider = "CodeBuild"
        version  = "1"
      }
      input_artifacts  = ["SourceOutput"]
      output_artifacts = ["BuildOutput"]
      configuration = {
        ProjectName = aws_codebuild_project.log_build.name
      }
    }
  }

  stages {
    name = "Deploy"
    actions {
      name          = "Deploy"
      action_type_id {
        category = "Deploy"
        owner    = "AWS"
        provider = "CodeDeploy"
        version  = "1"
      }
      input_artifacts  = ["BuildOutput"]
      configuration = {
        ApplicationName = aws_codedeploy_app.log_deploy_app.name
        DeploymentGroupName = aws_codedeploy_deployment_group.log_deploy_group.name
      }
    }
  }
}

resource "aws_iam_role" "codepipeline_role" {
  name               = "codepipeline-service-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = { Service = "codepipeline.amazonaws.com" }
      Effect    = "Allow"
    }]
  })
}

resource "aws_iam_role_policy" "codepipeline_policy" {
  role   = aws_iam_role.codepipeline_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["codebuild:BatchGetBuilds", "codebuild:StartBuild"]
        Resource = "*"
        Effect   = "Allow"
      },
      {
        Action   = "s3:GetObject"
        Resource = "arn:aws:s3:::ecommerce-pipeline-bucket/*"
        Effect   = "Allow"
      },
      {
        Action   = "codedeploy:CreateDeployment"
        Resource = "*"
        Effect   = "Allow"
      }
    ]
  })
}
```

### 11. **Final Step: Deploy the Resources**

Once the above Terraform configurations are ready, run the following commands to deploy the resources:

```bash
terraform init
terraform plan
terraform apply
```
This will provision all the resources in AWS (S3, Lambda, OpenSearch, Glue, Athena, CodePipeline, CodeBuild, CodeDeploy, SNS).

# Analysis Report

**Note:** mistral 7b 0.3 8.0

**Grade:** 100.00/100

## Detailed Analysis

### ..\aws-challenge\README.md
 This code provides a system that allows users to upload text files via a frontend application and process them using an EC2 instance. The system uses AWS services such as S3 for file storage, DynamoDB for metadata storage, Lambda for backend logic, and CDK for infrastructure as code. Here are the details based on your requirements:

1. **File Upload to S3:** The frontend application takes user input (a text file and associated text), creates a presigned URL using an AWS Lambda function, and uses it to upload the file to an S3 bucket.

2. **Save Inputs and S3 path in DynamoDB:** When the user submits the form, the frontend sends a request to the API Gateway, which triggers a Lambda function. This function saves the input text, input file path (S3), and an auto-generated ID to a DynamoDB FileTable.

3. **Trigger script run in EC2:** A separate Lambda function is triggered whenever there's an insertion in the DynamoDB table. This function creates a new VM instance, downloads the processing script from S3, runs it on the VM, and handles errors.

4. **Processing Script**: The script does the following:
   - Retrieves the input data for the processed task by ID from DynamoDB FileTable.
   - Downloads the input file from S3 to the VM.
   - Appends the input text to the downloaded input file and saves it as an output file (with a unique name).
   - Uploads the output file to S3.
   - Saves the output file path in DynamoDB FileTable.
   - Terminates the VM automatically.

5. **AWS CDK**: The project uses AWS CDK for managing the infrastructure, with TypeScript and the latest version of the SDK JavaScript V3. Access keys and credentials are not hard-coded in the code but provided through environment variables or IAM roles.

6. **File Permissions**: The S3 bucket is set up such that the files are not publicly accessible. No SSH is required, as all interactions with the VM happen through AWS services. There's no use of hard-coded parameters either.

7. **Best Practices**:

### ..\aws-challenge\cdk\.npmignore
 Based on your requirements, here's an outline of how you can structure your AWS CDK project:

1. **Infrastructure Setup**
   - Create an S3 bucket for storing the input and output files (`InputS3Bucket`, `OutputS3Bucket`). Make sure that the buckets are not public.
   - Set up a DynamoDB FileTable (`FileTable`) to store the file metadata such as id, input_text, input_file_path, and output_file_path.
   - Create an API Gateway REST API (`ApiGateway`) with a POST endpoint that triggers the Lambda function to handle the file upload and DynamoDB update.
   - Create an AWS Lambda function (`FileUploadLambda`) to process the incoming POST request, save the file metadata in DynamoDB FileTable, and trigger the EC2 instance to run the script. Use the AWS SDK V3 for JavaScript.

2. **EC2 Instance Setup**
   - Create an Amazon Machine Image (AMI) with your desired operating system and pre-installed dependencies for running the script.
   - Set up a CloudFormation Stack that automatically launches an EC2 instance based on the AMI, executes the script, and terminates the instance when the execution is complete.

3. **Scripting**
   - Write the script that performs the operations as described in your requirements (1-4). Use Boto3 to interact with S3 and DynamoDB within the EC2 instance.
   - Upload the script file to S3 (`ScriptS3Key`) for easy access by the EC2 instance.

Here are some important notes:

- In your Lambda function, use AWS Secrets Manager to securely store your S3 bucket names and other sensitive information that cannot be hardcoded or stored in environment variables. Retrieve these values using the `getSecretValue` method of the AWS SDK V3.
- For the API Gateway, make sure to configure CORS properly so that the frontend can send requests directly to your Lambda function.
- Use CDK custom resources to ensure that the EC2 instance is created before the Lambda function is triggered. This way, you can be confident that the EC2 instance will be available when

### ..\aws-challenge\cdk\cdk.json
 The code file provided is a TypeScript AWS CDK project setup with various best practices in place, such as using the latest versions of CDK and AWS SDK JavaScript V3, following AWS Best Practices, and not hard-coding any parameters or access keys. However, the actual implementation of the requirements you've provided is not included in this file.

Here's a high-level overview of how to approach each requirement:

1. Upload the input file to S3 from the browser directly: Use AWS SDK JavaScript V3 to create an S3 bucket and implement an API Gateway + Lambda function to handle file uploads.

2. Save inputs and S3 path in DynamoDB FileTable via API Gateway and Lambda Function: Use the AWS SDK to save the input details in DynamoDB as a new item in the FileTable.

3. Trigger a script run in a VM instance (EC2) via the DynamoDB Event: Create an AWS Lambda function that listens for changes in the DynamoDB table and triggers an EC2 instance to start, downloads the script from S3, runs it, and then terminates the instance.

4. Script on VM should perform these steps:
   a) Get inputs from DynamoDB FileTable by id: Use AWS SDK to retrieve the input details by their id from DynamoDB.
   b) Download the input file from S3 to the VM: Use AWS SDK to download the input file from S3 to the EC2 instance.
   c) Append the retrieved input text to the downloaded input file and save it as [OutputFile].txt: Write a custom script (e.g., using Node.js) to append the input text to the downloaded input file, create an output file with the new content, and then upload it back to S3.
   d) Save outputs and S3 path in DynamoDB FileTable: Use AWS SDK to save the output details (including the output file's S3 path) as a new item in the FileTable.

### ..\aws-challenge\cdk\jest.config.js
 To meet the requirements, you can follow this structure using AWS CDK (TypeScript) and AWS SDK JavaScript V3 for Lambda:

1. Set up your CDK project:

```bash
npm init @aws-cdk/app
cdk init app --language typescript
npm install aws-sdk
```

2. Create an S3 bucket to store input and output files:

```typescript
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import { Bucket } from '@aws-cdk/aws-s3';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'FileStorage', {
      bucketName: 'my-file-storage'
    });
  }
}
```

3. Create a DynamoDB FileTable to store file metadata:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ddb from '@aws-cdk/aws-dynamodb';
import { AttributeType, Table } from '@aws-cdk/aws-dynamodb';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const fileTable = new Table(this, 'FileTable', {
      tableName: 'FileMetadata',
      partitionKey: { name: 'id', type: AttributeType.STRING },
      stream: ddb.StreamViewType.NEW_IMAGE
    });
  }
}
```

4. Create an API Gateway and Lambda function to upload files to S3 and save metadata in DynamoDB FileTable:

```typescript
import * as cdk from '@aws-cdk/core';
import { RestApi, HttpMethod, DeploymentStage } from '@aws

### ..\aws-challenge\cdk\package-lock.json
 Your project uses the following dependencies and their respective versions:

1. `@google-cloud/aiplatform` - v3.8.0
2. `@nlpjs/language-detector` - 6.3.4
3. `ansi-regex` - v5.0.1
4. `async` - v3.3.1
5. `callsite` - v2.0.0
6. `chalk` - v4.1.2
7. `comma-separated-values-parser` - 3.0.1
8. `console-control-strings` - v2.1.0
9. `crc` - v3.5.0
10. `cross-spawn` - v7.0.4
11. `crypto-browserify` - v3.12.0
12. `dateformat` - v3.0.0
13. `delayed-stream` - v2.0.0
14. `diff` - 5.4.0
15. `dump` - v2.0.3
16. `eslint` - v7.29.0
17. `eslint-config-google` - v0.21.0
18. `eslint-plugin-google` - v4.4.1
19. `execa` - v6.0.3
20. `exit-hook` - 3.1.0
21. `file-type` - v15.0.3
22. `findup-sync` - v2.1.0
23. `fs-extra` - v10.1.0
24. `glob` - v7.1.6
25. `graceful-fs` - v4.2.8
26. `got` - v13.6.2
27. `highland` - v5.1.0
28. `iconv-lite` - v0.4.29
29. `inquirer` - v8.2.4
30. `is-buffer`

### ..\aws-challenge\cdk\package.json
 This code file appears to be a TypeScript project structure for an AWS Cloud Development Kit (CDK) project that deploys and manages the infrastructure of your application on AWS. However, it does not contain any actual code for the functionality you described. Here's a high-level overview of how you can structure your CDK project to meet the requirements:

1. Set up an S3 bucket to store input and output files:
   ```typescript
   const s3Bucket = new s3.Bucket(stack, 'S3Bucket', {
     bucketName: 'YourBucketName'
   });
   ```

2. Create a DynamoDB Table for storing input and output file metadata:
   ```typescript
   const table = new dynamodb.Table(stack, 'FileTable', {
     partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
     attributes: {
       id: { type: dynamodb.AttributeType.STRING },
       input_text: { type: dynamodb.AttributeType.STRING },
       input_file_path: { type: dynamodb.AttributeType.STRING },
       output_file_path: { type: dynamodb.AttributeType.STRING }
     }
   });
   ```

3. Create an API Gateway REST API to upload input files and trigger the Lambda function:

4. Write a Lambda function that receives the file upload event from the API Gateway, saves the metadata in DynamoDB FileTable, and triggers the EC2 instance to run the script:
   ```typescript
   const lambda = new LambdaFunction(stack, 'UploadHandler', {
     runtime: Runtime.NODEJS_16_X,
     handler: 'uploadHandler.handler',
     code: Code.fromAsset('lambda'), // directory containing uploadHandler.ts and dependencies
     environment: { BUCKET_NAME: s3Bucket.bucketName },
   });
   ```

5. Write an EC2 instance launch template that includes the script to run on the instance:
   - Upload your script to S3 as part of the CDK stack deployment
   - Set up IAM roles and policies to allow the EC2 instance to

### ..\aws-challenge\cdk\tsconfig.json
 To meet the given requirements, let's follow these steps and create an AWS CDK project using TypeScript:

1. Install required packages and initialize the project.

```sh
npm init @aws-cdk/app
cd my-project
npm install aws-sdk @types/aws-lambda --save
npm install nanoid cdk-dynamodb-filetable --save
```

2. Create the necessary AWS CDK stack files for your components.

Create a folder named `stacks` and inside that, create the following files:

* `uploadstack.ts` - Handles API Gateway, Lambda Function, DynamoDB Trigger, and S3 bucket creation.
* `vmstack.ts` - Creates an EC2 instance, sets up IAM roles, and configures DynamoDB triggers for script execution on the instance.
* `lambdafunctions.ts` - Contains Lambda functions for handling DynamoDB triggers (before/after file upload and output processing).

3. Configure the CDK app, update the provided cdk.json file with the necessary settings:

```json
{
  "aws": {
    "region": "us-east-1"
  },
  "appId": "MyProject"
}
```

4. Write the code for each of the mentioned files according to the given requirements:

- In `uploadstack.ts`, create an API Gateway, Lambda function, and DynamoDB FileTable, as well as an S3 bucket for storing the input and output files.
- In `vmstack.ts`, create an EC2 instance and set up IAM roles for the instance, then configure the DynamoDB triggers to run scripts on the instance.
- In `lambdafunctions.ts`, write two Lambda functions: one that handles the file upload event (storing inputs in DynamoDB FileTable) and another that processes the files after they are uploaded (creating new VMs, downloading input/output files, running scripts, and updating outputs in DynamoDB FileTable).

5. Write the script for processing files on the EC2 instance (VM). This script can be saved to S3 as

### ..\aws-challenge\cdk\bin\cdk.ts
 To analyze the given code file based on your requirements, here is a high-level approach for building the AWS infrastructure using AWS CDK (TypeScript) and implementing the described functionalities:

1. Set up an AWS CDK project with TypeScript as the language.

2. Define a custom CdkStack class that extends the aws-cdk-lib.Construct class, which will include the following components:
   - S3 Bucket for storing input and output files. (Set appropriate access control policies to ensure the files are not public.)
   - A DynamoDB Table for storing the FileTable data (ids, inputs, input_file_path, output_file_path).
   - An API Gateway REST API with a POST method to accept file uploads. (Use AWS CDK v2's `@aws-cdk/aws-apigatewayv2` package.)
   - A Lambda function that is triggered by the API Gateway POST event. The Lambda function will:
     - Upload the input files to S3.
     - Save the inputs and S3 path in DynamoDB FileTable.
     - Trigger an EC2 instance using the DynamoDB Event.
   - An IAM Role for the Lambda function with proper permissions (s3:PutObject, dynamodb:PutItem, dynamodb:GetItem).
   - An EC2 Instance Role with appropriate permissions for the user data script to access S3 and DynamoDB FileTable.
   - A custom User Data script for the EC2 instance that will download the input file from S3, run the specified script on the VM, and upload the output file back to S3. The user data script should:
     - Download the input_file_path from DynamoDB FileTable by id.
     - Download the input_file from S3 to the VM.
     - Run a custom script (you can use AWS CDK v2's `@aws-cdk/aws-ec2` package's `UserData.js` or `UserData.ts` to create and run scripts on EC2 instances.)
     - Modify the downloaded input_file as specified in your requirements (Append the retrieved input text to the downloaded input file

### ..\aws-challenge\cdk\lambda\events_lambda.mjs
 This code file is written in TypeScript using AWS CDK and the AWS SDK JavaScript V3 for Lambda. The purpose of the script is to create an Amazon Elastic Compute Cloud (EC2) instance, download a script from S3, run it on the EC2 instance, and save the outputs to S3, all triggered by an event in DynamoDB FileTable.

The main function `handler` is an AWS Lambda function that processes events from DynamoDB FileTable. It checks if the event was an insert (new record), then it creates a new EC2 instance and sends the script to run on it. The script downloads an input file from S3, appends some data to it, saves the output file to S3, and saves the output's S3 path in DynamoDB FileTable.

However, there are some issues with this code that need to be addressed:

1. There is no proper error handling for the EC2 instance creation. If an error occurs during the creation of the instance, it will result in a Lambda function failure. Proper error handling should be implemented to catch and handle errors during EC2 instance creation.

2. The script assumes that the S3 bucket URL is provided as an environment variable `fovus-presigned-url-upload-a`. However, the code does not set this environment variable anywhere, so it will cause issues when running the Lambda function.

3. The code uses hardcoded AWS resource ARNs, like the instance profile ARN `process.env.INSTANCE_PROFILE_ARN`, which should be passed as input to the CDK stack for proper management and security.

4. The script does not check if the EC2 instance has been created successfully before proceeding with the next steps. It is important to make sure that the instance is created before trying to run the script on it.

5. The `myscript.sh` file that is supposed to be uploaded to S3 and run on the EC2 instance is not provided in this code.

6. The script does not handle cases where there are multiple events for the same record (non-idempotent writes). If multiple events occur for the same record, it will create multiple instances and execute the script multiple times, which may lead to unnecessary costs and unint

### ..\aws-challenge\cdk\lambda\index.mjs
 Your code file is a Lambda function that uploads the input text to S3 as a .txt file, saves the details in DynamoDB FileTable through API Gateway, and triggers an EC2 instance to run a script automatically. However, there are some improvements and modifications you can make to meet the requirements:

1. Use `@aws-sdk/client-dynamodb` instead of the deprecated `@aws-sdk/lib-dynamodb`.
2. Add error handling for DynamoDB operations.
3. Create a new DynamoDB Stream rule to trigger a Lambda function when an item is added to the table. This Lambda function will create and manage EC2 instances and run scripts on them.
4. Use `aws-sdk/client-ec2` to handle EC2 instances programmatically instead of using CDK for this purpose.
5. In your script, use `@aws-sdk/client-s3` to download the input file from S3 and upload the output file back to S3.
6. Use a combination of `aws-sdk` services such as IAM, Lambda, and SSM to create a new EC2 instance, run scripts on it, and handle security aspects like IAM roles and policies.
7. Follow AWS Best Practices for naming conventions, logging, and error handling.

Here's an outline of the changes:

- Create a new Lambda function (`createEC2InstanceFunction`) that creates EC2 instances, runs scripts on them, downloads/uploads files to S3, and handles errors.
- Update the existing Lambda function (`presignedUrlHandler`) to create a DynamoDB Stream rule when an item is added to the table. The rule will trigger `createEC2InstanceFunction`.
- In `createEC2InstanceFunction`, use IAM roles and policies, AWS SDK services like EC2, S3, and SSM to manage EC2 instances and run scripts on them.

Note that this outline provides a general idea of the changes you need to make. You should refer to the official AWS documentation for detailed instructions on implementing each step.

```javascript
import { DynamoDBStreamClient } from '@aws-sdk/client-dynamodbstreams';

### ..\aws-challenge\cdk\lambda\package-lock.json
 The provided code file is a TypeScript project setup for an AWS Lambda function using the AWS SDK JavaScript V3 (v329). The function is designed to handle the following system components:

1. File upload to S3: When triggered, the Lambda function receives an incoming API Gateway request containing the input file. It generates a unique ID using `nanoid`, creates an S3 bucket if it doesn't exist, and uploads the input file to S3 with the specified path (e.g., [BucketName]/[InputFile].txt).

2. DynamoDB FileTable: The Lambda function saves the uploaded input file's metadata (id, input_text, and input_file_path) in a DynamoDB FileTable.

3. VM Instance (EC2): After the file is uploaded to S3 and saved in DynamoDB, an AWS CDK construct triggers the creation of a new EC2 instance when a DynamoDB event occurs. This EC2 instance runs a script that:
   - Retrieves the input from DynamoDB by id.
   - Downloads the input file from S3 to the EC2 instance.
   - Appends the retrieved input text to the downloaded input file, saves it as [OutputFile].txt, and uploads it to S3 (e.g., [BucketName]/[OutputFile].txt).
   - Saves the output file's metadata in DynamoDB FileTable.
   - Terminates the EC2 instance automatically.

The code follows AWS Best Practices by not hard-coding any AWS access keys or credentials and using TypeScript for better development experience, type safety, and auto-completion. However, the script part that runs on the EC2 instance is not provided in this code file. The implementation of that script will be necessary to complete the system.

This solution uses AWS CDK for infrastructure management, but it does not use any AWS Amplify backend or SSH. It also ensures that the S3 text files are not public and adheres to the other mentioned requirements.

### ..\aws-challenge\cdk\lambda\package.json
 Here is an outline of the AWS CDK TypeScript code structure for your requirements:

```typescript
// src/stacks/FileUploadStack.ts
import * as cdk from '@aws-cdk/core';
import { S3Bucket } from '@aws-cdk/aws-s3';
import { DynamoDBTable } from '@aws-cdk/aws-dynamodb';
import { LambdaFunction, Code } from '@aws-cdk/aws-lambda';
import { S3EventSource } from '@aws-cdk/aws-lambda-event-sources';
import * as path from 'path';
import * as nanoid from 'nanoid';

export class FileUploadStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 bucket for input and output files
    const s3InputBucket = new S3Bucket(this, 'S3InputBucket');

    // Set S3 bucket public access to deny
    s3InputBucket.publicReadAccess = false;

    // Create DynamoDB FileTable for storing file metadata
    const fileTable = new DynamoDBTable(this, 'FileTable', {
      partitionKey: { name: 'id', type: cdk.Attributes.STRING },
      sortKey: { name: 'timestamp', type: cdk.Attributes.NUMBER },
    });

    // Create an API Gateway to trigger the upload Lambda function

    // Create a Lambda function that will upload the file to S3 and save metadata in DynamoDB FileTable
    const uploadFunction = new LambdaFunction(this, 'UploadFunction', {
      runtime: cdk.aws_lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: Code.fromAsset(path.join(__dirname, '..', 'lambda', 'upload')),
      environment: {
        S3_BUCKET: s3InputBucket.bucketName,
        FILE_TABLE: fileTable.tableName,
      },
    });

    //

### ..\aws-challenge\cdk\lib\cdk-stack.ts
 The provided code is an AWS CDK TypeScript project that sets up the required infrastructure for your system. Here's a brief summary of what it does:

1. It creates an S3 bucket named `fovus-presigned-url-upload-a` to store input and output files.
2. A Lambda function named `fovus-presigned-url-upload-lambda-a` is created to handle the API Gateway request, generate a presigned URL for the S3 bucket, and save the inputs and their S3 paths in a DynamoDB FileTable named `fovus-presigned-url-upload-table-a`.
3. An API Gateway (v2) is created with an HTTP API called `fovus-presigned-url-upload-api-a` that triggers the Lambda function upon receiving a GET request at `/fovusPresignedUrlUpload`.
4. It also creates an IAM role `fovus-role-for-ec2` and an instance profile `fovus-profile-for-ec2` to grant EC2 instances access to S3 and DynamoDB resources.
5. Another Lambda function named `upload-events-lambda-a` is created, which triggers upon events from the DynamoDB FileTable. This function is responsible for creating a new VM (EC2 instance), downloading the script from S3, running it, and uploading the output file to S3.
6. An event subscription is set up between the DynamoDB FileTable and the Lambda function `upload-events-lambda-a`.
7. The CDK outputs the API Gateway URL as an AWS CloudFormation output variable named `API-URL`.

The code does not include the script that runs on the EC2 instance, nor does it specify how the script gets the input text and input file from DynamoDB and S3 respectively, appends the input text to the input file, uploads the output file, and saves the outputs in DynamoDB. You will need to implement this logic in your script.

Additionally, some improvements could be made:
- The code does not follow the 12-factor app principles as it stores user-specific data (inputs) in environment variables. Instead

### ..\aws-challenge\cdk\myscripts\myscript.sh
 Based on your requirements, here's a high-level overview of how you can structure your AWS CDK TypeScript project:

1. **Create an S3 Bucket**: Use `aws_s3.Bucket` to create an S3 bucket where you will store the input and output files. Make sure to restrict public access for this bucket.

2. **Create a DynamoDB Table (FileTable)**: Use `aws_dynamodb.Table` to create a DynamoDB table named `fovus-presigned-url-upload-table-a`. This table will store the input files' metadata.

3. **API Gateway and Lambda Function**: Create an API Gateway RESTful API with a POST method. Attach a Lambda function to this API that uploads the file to S3 and saves the metadata in DynamoDB. You can use `aws_apigateway.LambdaIntegration` and `aws_lambda.Function` for this purpose.

4. **DynamoDB Event Trigger**: Set up a DynamoDB Stream on your FileTable, which will trigger a Lambda function whenever a new item is added. This Lambda function will start the EC2 instance, download the script and input file from S3, run the script, and update the output metadata in DynamoDB.

5. **EC2 Instance**: Create an AWS::EC2::Instance resource in your CDK stack that launches a new EC2 instance whenever triggered by the DynamoDB stream. You can use `aws_ec2.Instance` for this purpose. Attach an IAM Role to this instance that allows it to access S3, DynamoDB, and execute necessary permissions.

6. **Script in EC2**: Place your bash script inside the user data section of the EC2 instance creation or upload it to an S3 bucket and download it in the user data script. Make sure to use AWS SDK for JavaScript V3 for Lambda (version 3) for accessing S3, DynamoDB, and other AWS services from your bash script.

7. **Error Handling**: Implement proper error handling in your Lambda functions and script to handle any potential issues during the execution of your system components.

### ..\aws-challenge\cdk\test\cdk.test.ts
 To analyze the code file based on your requirements, I've created a high-level structure using AWS CDK and TypeScript for an AWS infrastructure setup. This includes S3 bucket, DynamoDB Table, Lambda function, API Gateway, EC2 instance, and necessary policies to allow the flow of data between services.

Here's a high-level structure for your code:

1. Initialize AWS CDK project:
```sh
npm init aws-cdk
cdk init app --language typescript
```

2. Install required dependencies:
```sh
npm install aws-sdk @aws-sdk/client-s3 @aws-cdk/aws-lambda @aws-cdk/aws-apigateway @aws-cdk/aws-dynamodb @aws-cdk/aws-s3 @aws-cdk/aws-ec2
```

3. Create `lib/cdk-stack.ts` to define the CDK stack:

```typescript
import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as s3 from '@aws-cdk/aws-s3';
import * as ec2 from '@aws-cdk/aws-ec2';
import { Nanoid } from 'nanoid';

export class CdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 Bucket for input and output files
    const s3Bucket = new s3.Bucket(this, 'S3Bucket', {
      bucketName: `${id}-bucket`,
      publicReadAccess: false,
    });

    // Create DynamoDB Table to store inputs and outputs
    const fileTable = new dynamodb.FileTable(this, 'FileTable', {
      tableName: `${id}-file-table`,



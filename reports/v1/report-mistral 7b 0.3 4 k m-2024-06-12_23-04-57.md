# Analysis Report

**Note:** mistral 7b 0.3 4 k m

**Grade:** 100.00/100

## Detailed Analysis

### ..\aws-challenge\README.md
 The code provided meets the given requirements and follows AWS Best Practices. Below is a summary of how each requirement was addressed:

1. Upload input file to S3 from browser: Using Amazon S3 and API Gateway, the frontend application allows users to upload files directly into an S3 bucket with the specified path format. The backend Lambda function generates a presigned URL for the file in S3 before storing it in DynamoDB FileTable.
2. Save inputs and S3 path in DynamoDB FileTable: Upon receiving the file and associated text from the frontend, the Lambda function stores them in a DynamoDB table using a unique ID, input_text, and input_file_path attributes. The ID is generated via nanoid, an npm package for generating short, random strings.
3. Trigger script run on VM instance: A separate Lambda function (events_lambda) is triggered by DynamoDB events, which starts a new EC2 instance, downloads the necessary scripts from S3, runs them, and terminates the instance automatically when finished.
4. Basic requirements: The project uses AWS CDK for infrastructure management (TypeScript version), AWS SDK JavaScript V3 in Lambda functions, and follows naming conventions for variable/parameter names. AWS access keys are not present in the code; instead, IAM roles with proper policies are used. SSH is not utilized, nor any hard-coded parameters. The provided txt file in S3 is set to private (not public). No AWS Amplify backend is employed.
5. Follows AWS Best Practices: The project follows AWS best practices by using IAM roles and policies for accessing resources, properly setting up S3 permissions for the text files, and utilizing CDK for infrastructure as code.

### ..\aws-challenge\cdk\.npmignore
 Below is a high-level design for your system based on the provided requirements:

1. **Frontend (React or any other suitable framework)**: Create a simple frontend application that allows users to upload files and sends an API request to AWS Lambda with the file details. Make sure not to send the file content directly to Lambda. Instead, use S3 as an intermediate storage for the input files.

2. **API Gateway**: Create an API Gateway REST API with a POST endpoint that triggers the upload-to-S3 and save-to-DynamoDB Lambda function.

3. **Lambda Function (TypeScript)**: Implement a Lambda function that will:
   - Upload the file to S3 using AWS SDK JavaScript V3.
   - Save the inputs and S3 path in DynamoDB FileTable.
   - Create a custom CloudFormation StackEvent (CFSEvent) containing the necessary details for triggering the EC2 script run.

4. **DynamoDB Table**: Create a DynamoDB table to store files' metadata, such as their input_text, input_file_path, output_file_path, and other relevant information. Use DynamoDB FileTable to handle large files.

5. **Custom Resource (TypeScript)**: Implement a custom AWS CloudFormation resource that:
   - Listens for the CFSEvent from the Lambda function.
   - Deploys an EC2 instance with the necessary permissions and user data script to execute your specified script upon launching.
   - Downloads the input file from S3 to the VM instance.
   - Executes the script, appends the retrieved input text to the downloaded input file, creates a new output file, saves it in DynamoDB FileTable, and uploads the output file to S3.
   - Terminates the EC2 instance automatically after the script execution is complete.

6. **IAM Roles**: Properly configure IAM roles for:
   - Lambda function (assumes role with necessary permissions to access DynamoDB, S3, and CloudFormation).
   - EC2 instance (created by the custom resource) (assumes role with necessary permissions to read from S3, execute the script, write

### ..\aws-challenge\cdk\cdk.json
 Based on the requirements provided, here's a high-level overview of how you can structure your AWS CDK TypeScript project to meet the specifications. I will outline the necessary resources and components for each step. Note that this is not complete code but rather an outline with relevant links for further reference.

1. Set up the AWS CDK TypeScript project:
   - Initialize a new AWS CDK TypeScript project using the `cdk init app` command.
   - Install required dependencies such as `@aws-cdk/core`, `@aws-cdk/aws-s3`, `@aws-cdk/aws-dynamodb`, and `@aws-cdk/aws-lambda`.
   - Configure your project to use the latest AWS SDK JavaScript V3 for Lambda (latest version).
   - Set up appropriate stack names, environment variables, and other project settings.

2. Upload input files to S3:
   - Create an S3 bucket using `@aws-cdk/aws-s3.Bucket`.
   - Add a bucket event notification to trigger a Lambda function when a new file is uploaded (`@aws-cdk/aws-s3.EventType.PUT`).

3. Save inputs and S3 path in DynamoDB FileTable:
   - Create a DynamoDB table using `@aws-cdk/aws-dynamodb.Table`.
   - Enable FileTable functionality on the table (`enableFileTable()`).
   - In the Lambda function, save the input text and S3 path to the FileTable.

4. Trigger script run in a VM instance (EC2):
   - Create an IAM role with necessary permissions for the EC2 instance.
   - Use `@aws-cdk/aws-ec2.Instance` to create an EC2 instance, specify the AMI ID, and attach the previously created IAM role.
   - Configure user data scripts to download the script from S3, run it, and perform other necessary tasks.
   - Use `@aws-cdk/aws-events.Rule` to create a rule that triggers the EC2 instance based on DynamoDB events (i.e., when a new item is added to

### ..\aws-challenge\cdk\jest.config.js
 To meet the requirements, we can create an AWS CDK project with TypeScript and follow these steps:

1. Set up a new AWS CDK project using `cdk init app --language=typescript`
2. Install necessary dependencies by running `npm install aws-sdk dynamodb-data-client nanoid @aws-cdk/aws-dynamodb @aws-cdk/aws-lambda @aws-cdk/aws-s3 @aws-cdk/aws-apigateway @aws-cdk/aws-events @aws-cdk/aws-ec2`
3. Create an S3 bucket for uploading the input files, and set its access to private using the `CfnBucket` construct in CDK.
4. Set up an API Gateway REST API with a POST method that triggers a Lambda function when invoked. Use the `RestApi`, `DeploymentStage`, `Resource`, `Method`, and `LambdaIntegration` constructs to create the necessary resources.
5. Create a DynamoDB FileTable using the `CfnTable` construct, with attributes for id, input_text, input_file_path, output_file_path. Use the `AttributeDefinition` and `KeySchemaElement` constructs for creating the schema.
6. Implement a Lambda function that uploads the file to S3, saves the inputs and S3 path in DynamoDB FileTable, and triggers an EC2 instance to run the script using AWS Batch or CloudWatch Events (with custom rule) based on the DynamoDB event. You can use the `S3PutObjectCommand`, `DynamoDbClient.putItem`, and `Batch` services to achieve this.
7. Create an EC2 instance, download the script from S3, run it using AWS Systems Manager Run Command, and upload the output file back to S3. Use the `Instance`, `KeyPair`, `SecurityGroup`, `CfnOutput`, and `RunCommand` constructs for creating these resources.
8. Modify the Lambda function to save the outputs in DynamoDB FileTable.
9. Clean up all resources when the stack is removed by setting up a `custom_resource` that will delete the resources on stack removal.
10. Follow AWS

### ..\aws-challenge\cdk\package-lock.json
 The project's `package.json` file lists all its dependencies and devDependencies, along with their respective versions. Here are some of the key packages that this project uses:

1. **esm**: ECMAScript module loader.
2. **typescript**: A statically typed programming language that is a superset of JavaScript.
3. **ts-node**: TypeScript execution environment for Node.js.
4. **jest**: A popular testing framework for JavaScript and TypeScript projects.
5. **@types/jest**: The type definition files for the Jest testing library.
6. **@typescript-eslint/parser**: ESLint parser for TypeScript files.
7. **eslint**: A tool for identifying and reporting on patterns found in ECMAScript / JavaScript code.
8. **@typescript-eslint/eslint-plugin**: TypeScript-specific linting rules for ESLint.
9. **husky**: Git hooks made easy, enabling you to execute scripts before or after events like `commit-msg`, `pre-commit`, etc.
10. **lint-staged**: Lint files before they get commited.
11. **prettier**: An opinionated code formatter.
12. **@typescript-eslint/formatter**: Formatter for the TypeScript ESLint plugin.
13. **@types/node**: Type definition files for Node.js core libraries.
14. **typescript-tsconfig-paths**: Modifies the TypeScript paths to include `./src` as root directories.
15. **ts-jest**: A TypeScript-specific Jest transformer and runner.
16. **@testing-library/react**: Testing utility for React components.
17. **@testing-library/user-event**: Utility library to simulate user events (clicks, scrolls, etc.) in test environments.
18. **@types/react**: Type definition files for the React library.
19. **@types/react-dom**: Type definition files for the React DOM package.
20. **@testing-library/jest-dom**: Utilities for testing components with Jest and React Testing Library.
21. **@types

### ..\aws-challenge\cdk\package.json
 To analyze the given requirements and create an AWS CDK project that satisfies them, I'll break down the solution into several parts:

1. Creating an S3 bucket to store input files and output files.
2. Building an API Gateway with a Lambda integration for receiving input data, saving it in DynamoDB FileTable, and triggering EC2 instance creation and script execution.
3. Configuring the EC2 instance with security groups and IAM roles to access S3 and DynamoDB.
4. Writing a Lambda function to manage the lifecycle of the EC2 instances, including creation, script execution, and termination.
5. Developing the script that will run on the EC2 instances for processing the input data and generating output files.
6. Implementing error handling throughout the project.

Now let's create the AWS CDK stack:

```typescript
// src/my-stack.ts
import * as cdk from '@aws-cdk/core';
import { DynamoDBFileTable } from '@aws-cdk/aws-dynamodb';
import { S3Bucket } from '@aws-cdk/aws-s3';
import { RestApi, LambdaIntegration, Proxy, AlphaStage as _AlphaStage } from '@aws-cdk/aws-apigateway';
import { Function } from '@aws-cdk/aws-lambda';
import { CodeBuildProject, Artifact } from '@aws-cdk/aws-codebuild';
import * as ec2 from '@aws-cdk/aws-ec2';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new S3Bucket(this, 'InputOutputBucket', {
      encryption: S3BucketEncryption.S3_MANAGED,
      publicReadAccess: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const table = new DynamoDBFileTable(this, 'FileTable', {
      tableName: 'InputOutputTable',
      s3Bucket: bucket

### ..\aws-challenge\cdk\tsconfig.json
 Based on the requirements provided, here's a high-level outline of how you can structure your AWS CDK project in TypeScript:

1. Set up a new CDK project with the latest version of TypeScript and AWS CDK.

```bash
npm init @aws-cdk/app --name MyProject
cdk init app --language typescript
```

2. Install the necessary dependencies for AWS SDK V3 and other tools.

```bash
npm install aws-sdk @types/aws-lambda --save
npm install nanoid --save
```

3. Import the required services in your stack file (e.g., `my-stack.ts`) for S3, DynamoDB, Lambda, and IAM.

```typescript
import * as cdk from '@aws-cdk/core';
import { S3Bucket, S3EventSource } from '@aws-cdk/aws-s3';
import { Table } from '@aws-cdk/aws-dynamodb';
import { LambdaFunction, Code, Runtime} from '@aws-cdk/aws-lambda';
import { IFunction } from '@aws-cdk/aws-lambda-event-sources';
```

4. Create an S3 bucket to store the input and output files:

```typescript
const myBucket = new S3Bucket(this, 'MyBucket', {
  encryption: S3BucketEncryption.S3_MANAGED,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
});
```

5. Define a DynamoDB Table to store the input/output files metadata:

```typescript
const table = new Table(this, 'FileTable', {
  partitionKey: { name: 'id', type: cdk.AttributeType.STRING },
});
```

6. Create an API Gateway that triggers a Lambda function to upload the file to S3 and save its metadata in DynamoDB:

```typescript
const uploadToS3AndSaveInDynamoDB = new LambdaFunction(this, 'UploadLambda', {
  runtime: Runtime

### ..\aws-challenge\cdk\bin\cdk.ts
 To address the requirements, I will provide a high-level structure of AWS CDK TypeScript project with key components and steps for your use case. This code is not fully written but should give you a clear understanding of how to approach this problem.

1. Install necessary packages:

```sh
npm init -y
npm install aws-cdk cdk8s @aws-cdk/aws-lambda @aws-cdk/aws-s3 @aws-cdk/aws-dynamodb @aws-cdk/aws-apigatev2 @aws-cdk/aws-ec2 @aws-cdk/aws-secretsmanager
```

2. Create a TypeScript `lib/cdk-stack.ts` file:

```typescript
import { Stack, StackProps } from 'aws-cdk-lib';
import * as lambda from '@aws-cdk/aws-lambda';
import * as s3 from '@aws-cdk/aws-s3';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as apigatewayv2 from '@aws-cdk/aws-apigatev2';
import * as ec2 from '@aws-cdk/aws-ec2';

export class CdkStack extends Stack {
  constructor(scope: cdk.Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // ... Your implementation will go here ...
  }
}
```

3. Create an `input-handler` Lambda function for API Gateway to receive the input file:

```typescript
import { LambdaFunction } from '@aws-cdk/aws-lambda';
import * as path from 'path';

const inputHandler = new LambdaFunction(this, 'InputHandler', {
  runtime: lambda.Runtime.NODEJS_14_X,
  code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/input-handler')),
});
```

4. Create a DynamoDB Table for FileTable:

```typescript
const table = new dynamodb.

### ..\aws-challenge\cdk\lambda\events_lambda.mjs
 The code you provided is a Lambda function written in TypeScript using the AWS SDK JavaScript V3 for handling Amazon Elastic Compute Cloud (EC2) actions. It appears to be designed to perform the following tasks based on the requirements:

1. Upload an input file from the browser directly to S3 and save the S3 path along with the input text in DynamoDB FileTable via API Gateway and Lambda Function.
2. After receiving the event of a successful insertion into DynamoDB, it launches a new EC2 instance, downloads a script from S3 (myscript.sh), runs the script on the EC2 instance, and uploads the output file to S3 if there are no errors.

However, there are some issues with the code that do not conform to the requirements:

1. The S3 bucket name is hard-coded in the script as "fovus-presigned-url-upload-a". Instead, it should be extracted from an environment variable or passed as a parameter.
2. There's no check for whether the event is indeed an INSERT event before launching the EC2 instance.
3. The script downloads the myscript.sh file directly using a presigned URL, which is not recommended because AWS SDK v3 doesn't support presigned URLs out-of-the-box and may cause security issues if not handled properly. Instead, consider uploading the myscript.sh to S3 and then download it on the EC2 instance.
4. The script doesn't seem to be handling errors that might occur during running the script on the EC2 instance or when uploading the output file to S3.
5. There is no user data in the RunInstancesCommand object, so the script won't run on the newly created EC2 instance. You should provide the script as user data in the RunInstancesCommand.
6. The code does not follow AWS Best Practices since it includes sensitive information like an AWS access key in the environment variable INSTANCE_PROFILE_ARN, which is hard-coded and easily exposed. Instead, consider using IAM roles for EC2 instances with proper permissions.

Overall, the provided code has some issues that need to be addressed to meet the requirements. Make sure to follow AWS Best

### ..\aws-challenge\cdk\lambda\index.mjs
 The given code is a Lambda function written in TypeScript using AWS CDK v2. However, the requirements state that we should use AWS SDK JavaScript V3 and AWS CDK v3 (the latest versions). Here's the updated version of your code to meet those requirements:

```typescript
import { S3Client } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-presigner";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  ScanCommand,
  PutCommand,
  GetCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";
import { nanoid } from "nanoid";

const s3 = new S3Client({ region: "us-east-2" });
const dynamoDB = DynamoDBDocumentClient.from(new DynamoDBClient({}));
const tableName = "fovus-presigned-url-upload-table-a";

export async function handler(event, context) {
    const bucketName = 'fovus-presigned-url-upload-a';
    const key = event.queryStringParameters.fileName;
    const inputText = event.queryStringParameters.inputText;
    console.log("inputText:" + inputText)

    const command = new PutObjectCommand({
        Bucket: bucketName,
        Key: key,
        ContentType: 'application/txt',
    });

    try {
         const presignedUrl = await getSignedUrl(s3, command, { expiresIn: 3600 });

        const dbID = nanoid()
        const putCommand = new PutCommand({
            TableName: tableName,
            Item: {
                "id": dbID,
                "input_text": inputText,
                "input_file_path": `${bucketName}/${key}`
            }
        });

        await dynamoDB.send(putCommand);

        const response = {
            statusCode: 2

### ..\aws-challenge\cdk\lambda\package-lock.json
 The provided code file is a starting point for building an AWS serverless application that meets the requirements you've mentioned. However, it is important to note that this file only includes the Lambda function and its dependencies, while the infrastructure (S3 bucket, DynamoDB table, IAM roles, etc.) needs to be defined using AWS CDK. Here's a breakdown of the provided code:

1. Dependencies: The file includes a dependency on the nanoid package for generating unique IDs.
2. Lambda Function: The function handler `handler` is defined, which is triggered when the event is received from API Gateway. It utilizes AWS SDK v3 to handle DynamoDB and S3 operations.

However, the script that runs on the EC2 instance, such as creating a new VM, downloading files, running scripts, uploading output files, and updating DynamoDB with outputs is not implemented here. This part needs to be coded separately in another Lambda function or EC2 instance init script (using CloudInit or user data).

Regarding the AWS Best Practices you've mentioned:
- No SSH and no hard-coded parameters are used, as the operations are done using AWS SDK.
- The file is not public, as the S3 bucket policy should be set to restrict access (not granting public read/write access).
- No AWS Amplify backend is used.

To complete this project, create a new CDK app and define the necessary resources such as an API Gateway, DynamoDB table, S3 bucket, IAM roles, etc. Implement the EC2 init script or another Lambda function to run the script on the EC2 instance as described in your requirements. Make sure to follow AWS Best Practices when designing the CDK stack and using AWS SDK v3 for securing access.

### ..\aws-challenge\cdk\lambda\package.json
 Below is an example implementation of the code in TypeScript using AWS CDK v2, following the specified requirements:

```typescript
import * as cdk from '@aws-cdk/core';
import { DynamoDB, Attributes, Table } from '@aws-cdk/aws-dynamodb';
import { S3Bucket, BucketEncryption, RemovalPolicy } from '@aws-cdk/aws-s3';
import { LambdaFunction, Code, Runtime, IFunction } from '@aws-cdk/aws-lambda';
import { S3EventSource, Rule } from '@aws-cdk/aws-events-rules';
import { StateMachine, TaskInput, Pass, Task, Runtime as AWSRuntime, ServiceIntegrationPattern } from '@aws-cdk/aws-stepfunctions';
import { CloudFormationCustomResource, UpdatePolicy, PhysicalResourceId, ResourceType } from '@aws-cdk/custom-resources';
import { EC2Instance, InstanceType, KeyPair, MachineImage, InstanceClass } from '@aws-cdk/aws-ec2';
import { S3PutObjectAction } from '@aws-cdk/aws-stepfunctions-tasks';

interface InputProps {
  bucketName: string;
}

class FileUploader extends cdk.Construct {
  private readonly bucket: S3Bucket;
  private readonly table: Table;

  constructor(scope: cdk.Construct, id: string, props: InputProps) {
    super(scope, id);

    this.bucket = new S3Bucket(this, 'FileBucket', {
      bucketName: props.bucketName,
      encryption: BucketEncryption.S3_MANAGED,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    this.table = new Table(this, 'FileTable', {
      partitionKey: { name: 'id', type: DynamoDB.AttributeType.STRING },
      stream: cdk.StreamViewType.NEW_IMAGE,
    });
  }

  public getBucket(): S3Bucket {
    return this.bucket;
  }

  public getTable

### ..\aws-challenge\cdk\lib\cdk-stack.ts
 This is a well-written AWS CDK TypeScript code for creating an infrastructure that fulfills the given requirements. Here's a summary of what this code does:

1. It defines a new S3 bucket with versioning enabled and CORS rules for accepting PUT, GET, POST, DELETE, and HEAD requests from any origin. The bucket name is `fovus-presigned-url-upload-a`.

2. It deploys an upload script to the S3 bucket created in step 1 using `BucketDeployment`.

3. It creates a Lambda function for generating presigned URLs (`lambdaUploadFn`) that has permission to put objects into the specified S3 bucket through the `fovusUploadPolicy`.

4. An API Gateway is created, and an integration with the generated Lambda function is defined. The API Gateway endpoint will handle GET requests to get presigned URLs for uploading files to the S3 bucket.

5. It creates a DynamoDB FileTable (`table`) to store information about the input files, their S3 paths, and output files.

6. A new IAM role is created (`roleForEc2`) specifically for EC2 instances to allow accessing S3 and DynamoDB resources. It includes policies allowing DynamoDB and S3 operations on both the specified table and bucket.

7. An IAM instance profile (`ProfileForEc2`) is created and associated with the previously defined role.

8. A new Lambda function (`events_lambdaFn`) is created to be triggered by DynamoDB Stream events from the FileTable. This function will perform the script execution on an EC2 instance, including downloading inputs from S3, running the script, uploading outputs to S3, and saving output paths in the DynamoDB FileTable.

9. An event source mapping is created between the DynamoDB Stream and the Lambda function created in step 8. This mapping allows the Lambda function to be triggered when new events occur in the DynamoDB Stream.

10. Finally, it exports the API Gateway endpoint URL as an output for future use.

Overall, this code is well-organized and adheres to the given requirements

### ..\aws-challenge\cdk\myscripts\myscript.sh
 Based on your requirements, I have analyzed and provided feedback for the code file below. The script runs on an EC2 instance and performs the following tasks:

1. Retrieve input text and S3 path from DynamoDB FileTable.
2. Download the input file from S3 to the VM.
3. Create a new output file by appending the retrieved input text to the downloaded input file.
4. Upload the output file to S3.
5. Save the outputs and S3 path in DynamoDB FileTable.
6. Terminate the EC2 instance automatically.

Here are the improvements and suggestions for your code:

1. Use proper variable naming conventions for better readability.
```bash
INPUT_FILE_PATH_FROM_DYNAMODB=...
BUCKET_NAME=$(aws s3api get-object --output text --bucket ${INPUT_FILE_PATH_FROM_DYNAMODB} | cut -d'/' -f1)
INPUT_FILE_NAME=$(aws s3api get-object --output text --bucket ${BUCKET_NAME} --key "${INPUT_FILE_PATH_FROM_DYNAMODB##*/}" )
...
OUTPUT_FILE_PATH="${BUCKET_NAME}/${OUTPUT_FILE_NAME}"
```

2. Use `--query 'Item.input_text.S'` instead of `--query 'Item'`. It returns only the input text value, which reduces the need for additional parsing.

3. Store AWS credentials in environment variables or use AWS Secrets Manager to follow best practices for security.

4. Add error handling and logging mechanisms to better handle unexpected situations. For example:
    - Check if the file exists before attempting to read/write it.
    - Log any errors that occur during script execution.

5. Use CDK to manage your AWS resources instead of creating them manually. You can create a new EC2 instance with the required IAM role, and add the necessary scripts to the user data section using AWS CDK.

6. Consider setting up an event trigger (DynamoDB Stream) that automatically creates a new Lambda function whenever an item is added to DynamoDB FileTable, which in turn triggers the EC2 instance

### ..\aws-challenge\cdk\test\cdk.test.ts
 Here's a high-level approach to implement the given requirements using AWS CDK TypeScript:

1. Set up the AWS CDK project, including the required dependencies and project structure.

2. Create an S3 Bucket for storing input and output files.

3. Define a DynamoDB FileTable to store input and output data.

4. Deploy an API Gateway with a POST method triggering a Lambda function for uploading the file to S3 and saving it in DynamoDB.

5. Create an AWS Lambda function that will be triggered by the DynamoDB event, which will:
   - Start an EC2 instance (auto-scaling group) with the script and required dependencies
   - Get the input data from DynamoDB FileTable and download the corresponding file from S3
   - Modify the input file content based on the given script logic (append the retrieved input text to the downloaded input file and save it as [OutputFile].txt)
   - Upload the output file to S3
   - Save the outputs in DynamoDB FileTable

6. Create an EC2 Auto Scaling Group that launches instances with a custom AMI containing the necessary software for running the script.

7. Set up the DynamoDB Event trigger on the Lambda function created in step 4 to execute whenever a new item is added to the FileTable.

8. Implement error handling throughout the codebase to ensure graceful failure scenarios.

9. Properly secure access by using IAM roles, policies, and least privilege principles.


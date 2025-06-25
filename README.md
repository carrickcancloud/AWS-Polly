 # Speech Synthesis Workflow

This repository contains a GitHub Actions workflow for synthesizing speech from text using Amazon Polly and uploading the resulting audio files to an S3 bucket.

## Table of Contents
1. [Setup AWS Credentials and S3 Bucket](#setup-aws-credentials-and-s3-bucket)
2. [Create an IAM User with Programmatic Access](#create-an-iam-user-with-programmatic-access)
3. [Attach IAM Policies](#attach-iam-policies)
4. [Modify the Text](#modify-the-text)
5. [Trigger the Workflows](#trigger-the-workflows)
6. [Verify the Uploaded .mp3 Files](#verify-the-uploaded-mp3-files)

## Setup AWS Credentials and S3 Bucket

To set up AWS credentials and an S3 bucket, follow these steps:

1. **AWS Account**: Ensure you have an AWS account. If not, create one at [AWS](https://aws.amazon.com/).

2. **Create an S3 Bucket**:
   - Go to the S3 service in the AWS Management Console.
   - Click on "Create bucket".
   - Choose a unique name for your bucket and select a region.
   - Configure any additional settings as needed and create the bucket.

## Create an IAM User with Programmatic Access

To create an IAM user with programmatic access:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to the IAM service.
3. Click on "Users" in the sidebar, then "Create user".
4. Enter a username for the new user, then click on "Next".
5. Click on "Next".
6. Click on "Create User".

## Attach IAM Policies

After creating the IAM user, you need to attach the necessary policies:

1. **Create the `AcmeLabsAmazonPollyReadOnly` Policy**:
   - In the IAM console, go to "Policies" and click "Create policy".
   - Switch to the "JSON" tab and paste the following policy:
     ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AcmeLabsAmazonPollyReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "polly:SynthesizeSpeech",
                        "polly:DescribeVoices"
                    ],
                    "Resource": "*"
                }
            ]
        }
     ```
   - Click "Next", give it a name (`AcmeLabsAmazonPollyReadOnly`), and click on "Create policy".

2. **Create the `AcmeLabsAmazonS3ReadWrite` Policy**:
   - Repeat the steps to create another policy and paste the following JSON:
     ```json
       {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AcmeLabsAmazonS3ReadWrite",
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        "arn:aws:s3:::acmelabs-aws-polly-synthesize",
                        "arn:aws:s3:::acmelabs-aws-polly-synthesize/*"
                    ]
                }
            ]
       }
     ```
   - Name this policy `AcmeLabsAmazonS3ReadWrite` and create it.

3. **Attach Policies to the User**:
   - Navigate to the IAM service.
   - Click on "Users" in the sidebar, then click on your "Username".
   - Click on "Add permissions", choose "Add Permissions".
   - Select "Attach policies directly" and select both `AcmeLabsAmazonPollyReadOnly` and `AcmeLabsAmazonS3ReadWrite`.
   - Click "Next".
   - Finally, click on "Add permissions".

4. **Create Access Keys**:
   - Navigate to the "Security credentials" tab of your user.
   - Click on "Create access key".
   - Choose "Other" for the Use case.
   - Click "Next" and then fill out "Description tag value" (Name the secret.).
   - Click "Create access key".
   - Make sure to copy the Access Key ID and Secret Access Key. You will need these for your GitHub Actions workflow.
   - Store these credentials securely, as you will not be able to view the Secret Access Key again.
   - You can also download the credentials as a CSV file for safekeeping.
   - Click "Done" to finish.

5. **Configure GitHub Secrets**:
   - Go to your GitHub repository.
   - Navigate to `Settings` > `Secrets and variables` > `Actions`.
   - Add the following secrets:
     - `ACMELABS_SYNTHESIZE_AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
     - `ACMELABS_SYNTHESIZE_AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
     - `ACMELABS_SYNTHESIZE_AWS_S3_BUCKET`: The name of your S3 bucket.

   - Add the following environment variables:
     - `ACMELABS_SYNTHESIZE_AWS_REGION`: The region of your S3 bucket (e.g., `us-east-1`).
     - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_PROD`: The key for production uploads (e.g., `prod.mp3`).
     - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_BETA`: The key for beta uploads (e.g., `beta.mp3`).
     - `ACMELABS_SYNTHESIZE_AWS_S3_PREFIX`: The prefix for your S3 bucket (e.g., `polly-audio`).

## Modify the Text

To modify the text that will be synthesized:

1. Open the `speech.txt` file located in the repository.
2. Edit the content of the file as needed. For example:
 Where’s the kaboom? There was supposed to be an earth-shattering kaboom!
 3. Save your changes.

## Trigger the Workflows

The workflows are triggered automatically based on changes to the `speech.txt` file:

-   **On Merge**: This workflow runs when changes are pushed to the `main` branch.
-   **On Pull Request**: This workflow runs when a pull request is made to the `main` branch.

To manually trigger a workflow:
1. Create a new branch.
2. Make changes to the `speech.txt` file.
3. Commit and push your changes and create a pull request to trigger the workflow. Review GitHub Actions to ensure the workflow runs successfully.
4. Merge the pull request into the `main` branch to trigger the workflow. Review the Actions tab in your GitHub repository to see the status of the workflow.

## Verify the Uploaded .mp3 Files

To verify that the .mp3 files have been uploaded to your S3 bucket:

1. Go to the S3 service in the AWS Management Console.
2. Navigate to your bucket, click on "Objects" to view the contents.
3. Check for the uploaded .mp3 files under the specified prefix (e.g., `polly-audio`).
4. You can open or download the files to verify their content.

## Conclusion

This workflow automates the process of synthesizing text to speech and uploading the audio files to S3. Ensure that your AWS credentials are kept secure and not shared publicly.
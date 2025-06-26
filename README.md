# Speech Synthesis Workflow

This repository contains a GitHub Actions workflow for synthesizing speech from text using Amazon Polly and uploading the resulting audio files to an S3 bucket.

## Table of Contents
1. [Setup AWS Credentials and S3 Bucket](#setup-aws-credentials-and-s3-bucket)
2. [Create an IAM User with Programmatic Access](#create-an-iam-user-with-programmatic-access)
3. [Attach IAM Policies](#attach-iam-policies)
4. [Create Access Keys](#create-access-keys)
5. [Configure GitHub Secrets](#configure-github-secrets)
6. [Trigger the Workflows](#trigger-the-workflows)
7. [Verify the Uploaded .mp3 Files](#verify-the-uploaded-mp3-files)

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
3. Click on "Users" in the sidebar, then click on "Create user".
4. Enter a username for the new user and click on "Next" to proceed to the **Set permissions** section.
5. Click on "Next" to proceed to the "Review and create" section.
6. Click "Create user" to proceed.

## Create & Attach IAM Policies

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
   - Click "Next", give it a name (`AcmeLabsAmazonPollyReadOnly`), and click "Create policy".

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
   - Click on "Users" in the sidebar, then click on your new user's name.
   - Click on the "Permissions" tab.
   - Click on "Add permissions", choose "Attach existing policies directly", and select both `AcmeLabsAmazonPollyReadOnly` and `AcmeLabsAmazonS3ReadWrite`.
   - Click "Next" and then "Add permissions".

## Create Access Keys

1. Navigate to the "Security credentials" tab of your user.
2. Click on "Create access key" tab.
3. Click on "Other" for the "Use case".
4. Click on "Next" and fill out the "Description tag value" (name the secret).
5. Click on "Create access key".
6. Make sure to copy the Access Key ID and Secret Access Key.
   - You will need these for your GitHub Actions workflow.
   - **Store** these credentials **securely**, as you will not be able to **view** the Secret Access Key again.
   - You can also download the credentials as a CSV file for safekeeping.
7. Click "Done" to finish.

## Configure GitHub Secrets

1. Go to your GitHub repository.
2. Navigate to `Settings` > `Secrets and variables` > `Actions`.
3. Add the following secrets:
   1. Click on the "Secrets" tab.
   2. Click on "New repository secret".
   3. Name the secrets as follows:
      - `ACMELABS_SYNTHESIZE_AWS_ACCESS_KEY_ID`
      - `ACMELABS_SYNTHESIZE_AWS_SECRET_ACCESS_KEY`
      - `ACMELABS_SYNTHESIZE_AWS_S3_BUCKET`
   4. Enter the corresponding values for each secret.
      - For example:
        - `ACMELABS_SYNTHESIZE_AWS_ACCESS_KEY_ID`: `AKIAIOSFODNN7EXAMPLE`
        - `ACMELABS_SYNTHESIZE_AWS_SECRET_ACCESS_KEY`: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
        - `ACMELABS_SYNTHESIZE_AWS_S3_BUCKET`: `acmelabs-aws-polly-synthesize`
   5. Click "Add secret" to save each one.

4. Add the following environment variables:
   1. Click on the "Variables" tab.
   2. Click on "New repository variable".
   3. Name the variables as follows:
      - `ACMELABS_SYNTHESIZE_AWS_REGION`
      - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_PROD`
      - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_BETA`
      - `ACMELABS_SYNTHESIZE_AWS_S3_PREFIX`
   4. Enter the corresponding values for each variable.
      - For example:
        - `ACMELABS_SYNTHESIZE_AWS_REGION`: `us-east-1`
        - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_PROD`: `prod.mp3`
        - `ACMELABS_SYNTHESIZE_AWS_S3_KEY_BETA`: `beta.mp3`
        - `ACMELABS_SYNTHESIZE_AWS_S3_PREFIX`: `polly-audio`
   5. Click "Add variable" to save each one.

## Trigger the Workflows

The workflows are triggered automatically based on changes to the `speech.txt` file:

1. Create a new branch.
2. Make changes to the `speech.txt` file.
   - Open the `speech.txt` file located in the repository.
   - Edit the content of the file as needed. For example:
     ```
     Where’s the kaboom? There was supposed to be an earth-shattering kaboom!
     ```
   - Save your changes.
3. Commit and push your changes and create a pull request into the `main` branch to trigger the workflow.
   - Review GitHub Actions to ensure the workflow runs successfully.
     1. Click on "Actions" tab in your GitHub repository.
     2. In the left sidebar, select the workflow named `On Pull Request`.
     3. Click on the latest run to view the details.
     4. Check the logs to ensure that the speech synthesis and S3 upload steps completed successfully.
4. Merge the pull request into the `main` branch to trigger the workflow. 
   - Review GitHub Actions to ensure the workflow runs successfully.
     1. Click on "Actions" tab in your GitHub repository.
     2. In the left sidebar, select the workflow named `On Merge`.
     3. Click on the latest run to view the details.
     4. Check the logs to ensure that the speech synthesis and S3 upload steps completed successfully.

## Verify the Uploaded .mp3 Files

To verify that the .mp3 files have been uploaded to your S3 bucket:

1. Go to the S3 service in the AWS Management Console.
2. Navigate to your bucket, click on "Objects" to view the contents.
3. Check for the uploaded .mp3 files under the specified prefix (e.g., `polly-audio`).
4. You can open or download the files to verify their content.

## Conclusion

This workflow automates the process of synthesizing text to speech and uploading the audio files to S3. Ensure that your AWS credentials are kept secure and not shared publicly.

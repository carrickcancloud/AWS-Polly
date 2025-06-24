import boto3
import io

# Initialize the boto3 client
polly = boto3.client('polly')
s3 = boto3.client('s3')

# File to be transcribed (Located in the same directory as this script)
with open('speech.txt', 'r') as file:
    text = file.read()

# Synthesize speech using Amazon Polly
response = polly.synthesize_speech(
    Engine='generative',
    LanguageCode='en-US',
    OutputFormat='mp3',
    Text=text,
    TextType='text',
    VoiceId='Ruth',
)

# Print the response
print(
    f'RequestId: {response["ResponseMetadata"]["RequestId"]}\n'
    f'HTTPStatusCode: {response["ResponseMetadata"]["HTTPStatusCode"]}\n'
    f'HTTPHeaders:\n'
    f'    x-amzn-requestid: {response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-requestid"]}\n'
    f'    x-amzn-requestcharacters: {response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-requestcharacters"]}\n'
    f'    date: {response["ResponseMetadata"]["HTTPHeaders"]["date"]}\n'
    f'    content-type: {response["ResponseMetadata"]["HTTPHeaders"]["content-type"]}\n'
    f'    transfer-encoding: {response["ResponseMetadata"]["HTTPHeaders"]["transfer-encoding"]}\n'
    f'    connection: {response["ResponseMetadata"]["HTTPHeaders"]["connection"]}\n'
    f'RetryAttempts: {response["ResponseMetadata"]["RetryAttempts"]}\n'
    f'ContentType: {response["ContentType"]}\n'
    f'RequestCharacters: {response["RequestCharacters"]}\n'
    f'AudioStream: {response["AudioStream"]}\n'
)

# Define a variable to hold the audio stream
audio_stream = response['AudioStream']

# Check if the audio stream is not None
if audio_stream:
    audio_data = audio_stream.read() # Read the audio stream data into memory
    content_length = len(audio_data) # Get the length of the audio data

    # Create a BytesIO stream for uploading
    audio_bytes_io = io.BytesIO(audio_data)

    # Upload the audio stream to S3
    s3.put_object(
        Bucket='acmelabs-aws-polly-synthesize',
        ContentLength=content_length,
        ContentType='audio/mpeg3',
        Key='speech.mp3',
        Body=audio_bytes_io
    )

    print("Audio stream uploaded successfully to S3 bucket 'acmelabs-aws-polly-synthesize' with key 'speech.mp3'.")
else:
    print("No audio stream returned in the response.")

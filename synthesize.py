import boto3
import io
from botocore.exceptions import BotoCoreError, ClientError
from typing import Optional, Union

def synthesize_speech(
    text_file_path: str,
    engine: str = 'generative',
    language_code: str = 'en-US',
    output_format: str = 'mp3',
    text_type: str = 'text',
    voice_id: str = 'Ruth'
) -> Optional[Union[io.BytesIO, str]]:
    """Synthesize speech from a text file using Amazon Polly.

    Args:
        text_file_path (str): Path to the text file containing the text to synthesize.
        engine (str): The engine to use for synthesis (default is 'generative').
        language_code (str): The language code for the speech (default is 'en-US').
        output_format (str): The output format for the audio (default is 'mp3').
        text_type (str): The type of text (default is 'text').
        voice_id (str): The voice ID for the synthesis (default is 'Ruth').

    Returns:
        Optional[Union[io.BytesIO, str]]: Audio stream if successful, else an error message string.
    """
    polly = boto3.client('polly')

    try:
        with open(text_file_path, 'r') as file:
            text = file.read()

        response = polly.synthesize_speech(
            Engine=engine,
            LanguageCode=language_code,
            OutputFormat=output_format,
            Text=text,
            TextType=text_type,
            VoiceId=voice_id,
        )

        # Print the response metadata
        print(
            f'RequestId: {response["ResponseMetadata"]["RequestId"]}\n'
            f'HTTPStatusCode: {response["ResponseMetadata"]["HTTPStatusCode"]}\n'
            f'ContentType: {response["ContentType"]}\n'
        )

        return response.get('AudioStream')

    except (BotoCoreError, ClientError) as e:
        print(f"Error occurred while synthesizing speech: {e}")
        return str(e)
    except FileNotFoundError:
        print(f"File not found: {text_file_path}")
        return f"File not found: {text_file_path}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return str(e)

def upload_to_s3(audio_stream: Optional[io.BytesIO], bucket_name: str, s3_key: str) -> None:
    """Upload the audio stream to an S3 bucket.

    Args:
        audio_stream (Optional[io.BytesIO]): The audio stream to upload.
        bucket_name (str): The name of the S3 bucket.
        s3_key (str): The key under which to store the object in S3.
    """
    s3 = boto3.client('s3')

    if audio_stream:
        try:
            audio = audio_stream.read()  # Read the audio stream data into memory
            content_length = len(audio)  # Get the length of the audio data

            # Create a BytesIO stream for uploading
            audio_bytes = io.BytesIO(audio)

            # Upload the audio stream to S3
            s3.put_object(
                Bucket=bucket_name,
                ContentLength=content_length,
                ContentType='audio/mpeg3',
                Key=s3_key,
                Body=audio_bytes
            )

            print(f"Audio stream uploaded successfully to S3 bucket '{bucket_name}' with key '{s3_key}'.")
        except ClientError as e:
            print(f"Failed to upload to S3: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during upload: {e}")
    else:
        print("No audio stream returned in the response.")

# Main Execution
if __name__ == "__main__":
    audio_stream = synthesize_speech(
        text_file_path='speech.txt',
        engine='generative',
        language_code='en-US',
        output_format='mp3',
        text_type='text',
        voice_id='Ruth'
    )
    upload_to_s3(
        audio_stream,
        'acmelabs-aws-polly-synthesize',
        'speech.mp3'
    )

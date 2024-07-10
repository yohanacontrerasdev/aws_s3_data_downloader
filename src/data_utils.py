import boto3
import os
from dotenv import load_dotenv

from pathlib import Path
from src import config 

def download_pdfs():
  # Load the variables from the .env file
  load_dotenv()

  # Get credentials and configurations from environment variables
  ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
  SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
  BUCKET_NAME = os.getenv('BUCKET_NAME')
  PREFIX = os.getenv('PREFIX')

  # Initialize the boto3 session
  s3 = boto3.client(
      's3',
      aws_access_key_id=ACCESS_KEY,
      aws_secret_access_key=SECRET_KEY
  )

  # Directory where the downloaded files will be saved
  DOWNLOAD_DIR = config.DATASET_ROOT_PATH
  os.makedirs(DOWNLOAD_DIR, exist_ok=True)

  # List the objects within the bucket/prefix
  response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

  # Download each object
  if 'Contents' in response:
    for obj in response['Contents']:
        file_name = obj['Key']
        if file_name.endswith('/'):
            # It's a directory, do nothing
            continue
        
        # Preserve the full path, maintaining the directory structure
        destination_path = os.path.join(DOWNLOAD_DIR, file_name)

        # Create necessary directories
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))
        
        # Download the file
        s3.download_file(BUCKET_NAME, file_name, str(destination_path))
        print(f'Downloaded: {file_name} to {destination_path}')
  else:
      print(f'No objects found in prefix {PREFIX}')


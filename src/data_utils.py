import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
from src import config
import fitz  # PyMuPDF

def download_pdfs_and_convert_to_text():
    # Load the variables from the .env file
    load_dotenv()

    # Get credentials and configurations from environment variables
    ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    PREFIX = os.getenv("PREFIX")

    # Initialize the boto3 session
    s3 = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    # Directory where the text files will be saved
    TEXT_DIR = config.DATASET_ROOT_PATH / "texts"
    os.makedirs(TEXT_DIR, exist_ok=True)

    # List the objects within the bucket/prefix
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

    # Download each object
    if "Contents" in response:
        for obj in response["Contents"]:
            file_name = obj["Key"]
            if file_name.endswith("/"):
                # It's a directory, do nothing
                continue

            # Get the file object
            try:
              file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)

              # Read the content of the file into memory
              pdf_content = file_obj['Body'].read()

              # Convert the PDF content to text
              extract_text_from_pdf_content(pdf_content, TEXT_DIR, Path(file_name).name)
            except Exception as e:
                print(f"Failed to process in prefix {PREFIX}")
    else:
        print(f"No objects found in prefix {PREFIX}")

def extract_text_from_pdf_content(pdf_content, text_dir, original_file_name):
    # Open the PDF document from memory
    document = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    # Extract text from each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    # Define the output path for the text file
    output_path = os.path.join(text_dir, original_file_name.replace(".pdf", ".txt").replace(".PDF", ".txt"))
    # Save the extracted text to a .txt file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Converted: {original_file_name} to {output_path}")





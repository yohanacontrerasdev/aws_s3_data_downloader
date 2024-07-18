import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
import fitz  # PyMuPDF
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

def download_pdfs_and_convert_to_text():
    ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    PREFIX = os.getenv("PREFIX")

    s3 = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    all_text = ""

    if "Contents" in response:
        for obj in response["Contents"]:
            file_name = obj["Key"]
            if file_name.endswith("/"):
                continue

            try:
                file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
                pdf_content = file_obj['Body'].read()
                text = extract_text_from_pdf_content(pdf_content)
                all_text += text + "\n"
                print(f"Downloaded and processed: {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name} in prefix {PREFIX}: {e}")
    else:
        print(f"No objects found in prefix {PREFIX}")

    # Get and save text chunks
    chunks = get_text_chunks(all_text)
    return chunks

def extract_text_from_pdf_content(pdf_content):
    document = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


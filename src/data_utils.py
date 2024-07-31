import boto3
import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
import pandas as pd
import nest_asyncio
import re

nest_asyncio.apply()
load_dotenv()

def extract_year(name):
  match = re.search(r'_(\d{4})\.pdf$', name)
  return int(match.group(1)) if match else None

def download_pdfs_from_s3():
  ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
  SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
  BUCKET_NAME = os.getenv("BUCKET_NAME")
  PREFIX = os.getenv("PREFIX")

  s3 = boto3.client(
    "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
  )

  response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
  data = []

  if "Contents" in response:
    for obj in response["Contents"]:
      file_name = obj["Key"]
      if file_name.endswith("/") or not file_name.endswith(".pdf"):
        continue

      try:
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
        pdf_content = file_obj['Body'].read()
        data.append({"name": os.path.basename(file_name), "content": pdf_content})
      except Exception as e:
        print(f"Failed to download {file_name}: {e}")
  else:
    print(f"No objects found in prefix {PREFIX}")

  return pd.DataFrame(data)

def filter_pdfs_by_years(df):
  df['year'] = df['name'].apply(extract_year)
  df['base_name'] = df['name'].apply(lambda x: re.sub(r'_\d{4}\.pdf$', '', x))

  grouped = df.groupby('base_name')['year']
  max_year = grouped.transform('max')
  min_year = grouped.transform('min')

  filtered_df = df[(df['year'] == max_year) | (df['year'] == min_year)]
  return filtered_df

def extract_text_from_pdf_content(pdf_content, api_key, file_name):
  document = LlamaParse(result_type="markdown", api_key=api_key).load_data(pdf_content, extra_info={"file_name": file_name})
  full_text = "".join([t.text for t in document])
  return full_text

def download_pdfs_and_convert_to_text():
  LLAMAPARSE_API_KEY = os.getenv("LLAMAPARSE_API_KEY")

  # Download all PDFs from S3
  df = download_pdfs_from_s3()

  if df.empty:
    print("No PDFs downloaded.")
    return pd.DataFrame()

  # Filter PDFs by most recent and oldest years
  filtered_df = filter_pdfs_by_years(df)

  if filtered_df.empty:
    print("No PDFs found for the specified years.")
    return pd.DataFrame()

  # Limit to the first 20 PDFs
  filtered_df = filtered_df.head(20)

  # Extraer texto de los PDFs filtrados
  filtered_df['text'] = filtered_df.apply(
      lambda row: extract_text_from_pdf_content(row['content'], LLAMAPARSE_API_KEY, row['name']), axis=1
  )

  return filtered_df

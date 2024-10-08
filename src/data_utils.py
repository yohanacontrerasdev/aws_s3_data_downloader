import boto3
import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
import pandas as pd
import nest_asyncio
import re
import fitz
import io

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

def extract_text_with_llamaparse(pdf_content, api_key, file_name):
  document = LlamaParse(result_type="markdown", api_key=api_key).load_data(pdf_content, extra_info={"file_name": file_name})
  full_text = "".join([t.text for t in document])
  return full_text

def extract_text_with_fitz(pdf_content):
  document = fitz.open(stream=pdf_content, filetype="pdf")
  text = ""
  for page_num in range(len(document)):
      page = document.load_page(page_num)
      text += page.get_text()
  return text

class LlamaParseAPIKeyMissingError(Exception):
  pass

def clean_pdf_in_memory(pdf_content):
    try:
        # Abre el archivo PDF en memoria
        document = fitz.open(stream=pdf_content, filetype="pdf")
        # Crea un nuevo archivo PDF en memoria
        new_pdf_stream = io.BytesIO()
        document.save(new_pdf_stream)
        # Devuelve el contenido del nuevo archivo PDF
        return new_pdf_stream.getvalue()
    except Exception as e:
        #logger.error(f"Error cleaning PDF in memory: {e}")
        return None

# Extract text based on the selected method
def extract_text(row, use_llamaparse, llamaparse_api_key):
    cleaned_pdf_content = clean_pdf_in_memory(row['content'])
    if not cleaned_pdf_content:
        return None
    
    if use_llamaparse:
        return extract_text_with_llamaparse(row['content'], llamaparse_api_key, row['name'])
    else:
        return extract_text_with_fitz(row['content'])

def download_pdfs_and_convert_to_text(use_llamaparse=False, llamaparse_api_key=None):
  if use_llamaparse and not llamaparse_api_key:
    raise LlamaParseAPIKeyMissingError("API key for LlamaParse is required when use_llamaparse is set to True.")

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
  #filtered_df = filtered_df.head(20)

  filtered_df = filtered_df.copy()
  filtered_df['text'] = filtered_df.apply(lambda row: extract_text(row, use_llamaparse, llamaparse_api_key), axis=1)

  # Count the number of failed extractions
  failed_count = filtered_df['text'].isnull().sum()

  # Remove rows where text extraction failed
  filtered_df = filtered_df.dropna(subset=['text'])

  print(f"Total PDFs processed: {len(df)}")
  print(f"Total PDFs successfully processed: {len(filtered_df)}")
  print(f"Total PDFs failed to process: {failed_count}")

  return filtered_df

# Nasdaq GPT

This project is a Python script to download annual reports and 10-K statements of all NASDAQ listed companies from an Amazon S3 bucket.

## Requirements

- Python 3.x
- pip
- Access to AWS with the necessary credentials

## Project Configuration

1. Clone this repository:

    ```bash
    git clone https://github.com/tu-usuario/aws_s3_data_downloader.git
    cd aws_s3_data_downloader.git
    ```

2. Create and activate a virtual environment:

    For Unix (Linux/MacOS):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    For Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory with the following content, replacing the values ​​with your AWS credentials:

    ```env
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    BUCKET_NAME=anyoneai-datasets
    PREFIX=nasdaq_annual_reports/
    ```

## Use

To run the script:

```bash
python app.py
```
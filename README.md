# NasdaqGPT

The main goal of our project is to develop a chatbot that serves as a financial advisor, providing quick and accurate answers to questions about companies listed on NASDAQ. For context, NASDAQ is one of the largest stock exchanges in the world, known for its high-tech stocks and innovative companies.

## Requirements

- Python >= 3.10.12
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
    LLAMAPARSE_API_KEY='YOUR_LLAMAPARSE_API_KEY'
    OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
    ```
5. Run all cells in data_exploration.ipynb

## Use

To use the chatbot, simply run the following command in your terminal:

```bash
streamlit run app.py
```
This command will start the chatbot in an interactive web application through streamlit.
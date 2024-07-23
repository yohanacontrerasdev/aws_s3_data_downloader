import os
from pathlib import Path

VECTORSTORE_PATH = str(Path(__file__).parent.parent / "vectorstore")
os.makedirs(VECTORSTORE_PATH, exist_ok=True)

# from pathlib import Path 

# # Determine the project root path 
# PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent 
 
# # Define the data directory 
# VECTORSTORE_PATH = PROJECT_ROOT_PATH / 'vectorstore'

# Create the data directory if it doesn't exist
# DATASET_ROOT_PATH.mkdir(parents=True, exist_ok=True)
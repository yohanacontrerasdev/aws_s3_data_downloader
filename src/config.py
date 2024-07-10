import os
from pathlib import Path

DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "data")
os.makedirs(DATASET_ROOT_PATH, exist_ok=True)

from pathlib import Path 

# Determine the project root path 
PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent 
 
# Define the data directory 
DATASET_ROOT_PATH = PROJECT_ROOT_PATH / 'data' 

# Create the data directory if it doesn't exist 
DATASET_ROOT_PATH.mkdir(parents=True, exist_ok=True)
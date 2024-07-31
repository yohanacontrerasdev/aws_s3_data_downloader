import os
from pathlib import Path

VECTORSTORE_PATH = str(Path(__file__).parent.parent / "vectorstore")
os.makedirs(VECTORSTORE_PATH, exist_ok=True)

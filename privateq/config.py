import os
from pathlib import Path

# Model parameters
EMBEDDING_DIMENSIONS = 768
MAX_CONTENT_LENGTH = 8192

# Directories
FILE_DIR = os.environ.get("FILE_DIR")
ROOT_DIR = Path(__file__).resolve().parent.parent
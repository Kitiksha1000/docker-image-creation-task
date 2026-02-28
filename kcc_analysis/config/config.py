# KCC Analysis Configuration

# Processing Settings
CHUNK_SIZE = 1_000_000  # 1M rows per chunk for optimal performance
USE_MULTIPROCESSING = True
N_WORKERS = -1  # -1 = use all available CPU cores

# GPU Settings (if available)
USE_GPU = True  # Set to False if no GPU available
GPU_BACKEND = "cudf"  # Options: cudf (RAPIDS), None

# Data Paths
DATA_DIR = "../data"
OUTPUT_DIR = "../outputs"
LOGS_DIR = "../logs"

# Dataset
DATASET_FILE = "kcc_master_dataset.csv"
DATASET_ENCODING = "utf-8"

# Language Detection
ENABLE_LANGUAGE_DETECTION = True
LANGUAGE_SAMPLE_SIZE = 10_000  # Sample this many queries per chunk for language detection
SUPPORTED_LANGUAGES = [
    "English", "Hindi", "Telugu", "Marathi", "Tamil", 
    "Kannada", "Malayalam", "Bengali", "Gujarati", 
    "Punjabi", "Odia", "Assamese", "Urdu"
]

# Weather Keywords (Path to keyword reference)
WEATHER_KEYWORDS_FILE = "../../multilingual_keywords_reference.md"

# Output Formats
SAVE_JSON = True
SAVE_CSV = True
SAVE_REPORTS = True

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
ENABLE_PROGRESS_BAR = True

# Performance Tuning
LOW_MEMORY_MODE = False  # Set True if RAM < 16GB
OPTIMIZE_MEMORY = True  # Use categorical dtypes where possible

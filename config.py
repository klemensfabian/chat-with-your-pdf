# PDF processing parameters
PDF_CHUNK_SIZE = 1000
PDF_CHUNK_OVERLAP = 150

# Database configuration
DB_DEFAULT = "FAISS"  # Can be "HANA" or "FAISS"
DB_TABLE = "ZCHATDATA"

# AI components
EMBEDDING_MODEL = "text-embedding-3-small" # Can be "text-embedding-ada-002" or "text-embedding-3-small"
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0
LLM_MAX_TOKENS = 1000
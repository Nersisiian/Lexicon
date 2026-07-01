from prometheus_client import Counter, Histogram

DOCUMENTS_UPLOADED = Counter('documents_uploaded_total', 'Total uploaded documents')
PROCESSING_TIME = Histogram('document_processing_seconds', 'Time spent processing document')

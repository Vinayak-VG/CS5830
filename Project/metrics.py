from prometheus_client import Counter, Histogram

# Counter for the number of requests
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['endpoint', 'method'])

# Histogram for request latency
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['endpoint'])

# Counter for classification outcomes
CLASSIFICATION_OUTCOMES = Counter('classification_outcomes', 'Deep fake classification outcomes', ['result'])
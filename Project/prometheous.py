from flask import Flask, request, jsonify
from time import time
from metrics import REQUEST_COUNT, REQUEST_LATENCY, CLASSIFICATION_OUTCOMES

app = Flask(__name__)

@app.before_request
def before_request():
    request.start_time = time()

@app.after_request
def after_request(response):
    request_latency = time() - request.start_time
    endpoint = request.endpoint
    method = request.method

    # Increment request counter
    REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()

    # Observe request latency
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(request_latency)

    return response

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    # Assume there's a function classify_deepfake that returns 'real' or 'fake'
    result = classify_deepfake(data)

    # Increment classification outcomes counter
    CLASSIFICATION_OUTCOMES.labels(result=result).inc()

    return jsonify({'result': result})

@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

def classify_deepfake(data):
    
    ## put the defake model here 
    
    return 'fake'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


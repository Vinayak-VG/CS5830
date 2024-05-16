from fastapi import FastAPI, File, UploadFile, Request
import torch
import torch.nn as nn
from PIL import Image
from mnist import Net
import io
import numpy as np
import torchvision.transforms as transforms
import sys
import time
from prometheus_client import Summary, start_http_server, Counter, Gauge
from prometheus_client import disable_created_metrics

# Initialize the FastAPI app
REQUEST_DURATION = Summary('api_timing', 'Request duration in seconds')
counter = Counter('api_call_counter', 'number of times that API is called', ['endpoint', 'client'])
gauge = Gauge('api_runtime_secs', 'runtime of the method in seconds', ['endpoint', 'client'])
app = FastAPI()

# Load the model using the provided model_path
def load_model(model_path):
    model = Net()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

model_path = sys.argv[1]
model = load_model(model_path)

# Define the image transformation pipeline
def transform_image(image_bytes):
    my_transforms = transforms.Compose([
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5,), (0.5,))
                                        ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

# Define the prediction function
def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return predicted_idx

# Define the prediction route
@REQUEST_DURATION.time()
@app.post("/predict")
# async def predict_digit(image_file: UploadFile = File(...), request:Request):

async def predict_digit(image_file: UploadFile, request:Request):

    counter.labels(endpoint='/predict', client=request.client.host).inc()
    
    start = time.time()
    """
    Predicts the digit from uploaded image.

    Args:
        image: Uploaded image file.

    Returns:
        JSON response with predicted digit.
    """

    image_bytes = image_file.file.read()
    class_id = get_prediction(image_bytes)
    result = {
            "digit": class_id
        }
    time_taken = time.time() - start
    gauge.labels(endpoint='/np', client=request.client.host).set(time_taken)

    return result

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    start_http_server(18000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, File, UploadFile
import torch
import torch.nn as nn
from PIL import Image
from mnist import Net
import io
import numpy as np
import torchvision.transforms as transforms
import sys

# Initialize the FastAPI app
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
@app.post("/predict")
async def predict_digit(image_file: UploadFile = File(...)):
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
    return result

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
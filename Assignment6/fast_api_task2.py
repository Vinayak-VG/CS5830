from fastapi import FastAPI, File, UploadFile
import torch
import torch.nn as nn
from PIL import Image
from mnist import Net
import io
import numpy as np
import torchvision.transforms as transforms
import sys

app = FastAPI()

def format_image(image_bytes):
    """
    Preprocess the input image by resizing, converting to grayscale, and normalizing.
    """
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((28, 28))
    image = np.array(image)

    try:
        if image.shape[2] == 3 or image.shape[2] == 4:
            image = 0.2989 * image[:, :, 0] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 2]
    except:
        pass

    image = image.astype(np.float32)
    return image

def load_model(model_path):
    """
    Load the trained model from the provided path.
    """
    model = Net()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

model_path = sys.argv[1]
model = load_model(model_path)

def transform_image(image):
    """
    Transform the preprocessed image into a tensor for input to the model.
    """
    my_transforms = transforms.Compose([
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5,), (0.5,))
                                        ])
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    """
    Get the prediction for the input image.
    """
    image = format_image(image_bytes)
    tensor = transform_image(image=image)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return predicted_idx

@app.post("/predict")
async def predict_digit(image_file: UploadFile = File(...)):
    """
    Predict the digit from the uploaded image.
    """
    image_bytes = image_file.file.read()
    class_id = get_prediction(image_bytes)
    result = {
            "digit": class_id
        }
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
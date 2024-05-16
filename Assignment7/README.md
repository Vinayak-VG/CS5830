# Build a FastAPI for MNIST digit prediction

This repository contains a FastAPI implementation for digit classification using the MNIST dataset. The API allows users to upload an image of a handwritten digit, and it returns the predicted digit value.

## Overview

This assignment aimed to build a FastAPI that exposes the MNIST digit classification functionality through a REST API. Users can upload an image of a handwritten digit, and the API will respond with the predicted digit value.

## Files

- `data/MNIST/raw`: Directory containing the raw MNIST dataset.
- `fast_api_task1.py`: FastAPI implementation for Task 1.
- `fast_api_task2.py`: FastAPI implementation for Task 2, including image preprocessing.
- `mnist.pth`: Saved weights of the trained MNIST model.
- `mnist.py`: Python script for training the MNIST model.

## Setup

1. Clone the repository: `git clone https://github.com/Vinayak-VG/CS5830.git` and cd Assignment6
2. Start the FastAPI server: python3.11 fast_api_task1.py "mnist.pth" (for Task 1) or python3.11 fast_api_task2.py "mnist.pth" (for Task 2)
3. Access the API documentation at `http://127.0.0.1:8000/docs`

## Usage

1. Open the API documentation in your web browser.
2. Navigate to the `/predict` endpoint.
3. Click on the "Try it out" button.
4. Upload an image of a handwritten digit (28x28 pixels for Task 1, any size for Task 2).
5. Click on the "Execute" button.
6. The API will respond with the predicted digit value in the format `{"digit": "X"}`, where X is the predicted digit.

## Testing

For Task 2, draw 10 images of handwritten digits using tools like MS Paint or a touchscreen. Upload these images to the API and record the performance (number of correctly predicted digits out of 10).

## Report

Detailed Analysis can be found here - [Report](https://docs.google.com/document/d/1tEzUKdUY8yH9pytzDBXSx7BpcTISu9qSyX_hsw8X1hQ/edit?usp=sharing)

# MNIST Digit Classification with MLflow

This repository contains a Jupyter Notebook (assign5.ipynb) that builds and compares several neural network models for the MNIST digit classification task with different model configuration settings. The objective of this assignment was to set up MLflow for tracking experiments and logging metrics and parameters during the model training process.

## Assignment Overview

The goal of this assignment was to build and compare several neural network models for the MNIST digit classification task, with different model configuration settings. Each configuration was expected to exhibit different performance patterns over the training epochs. To streamline the process of tracking metrics and parameters, MLflow was utilized through the `mlflow.autolog()` function in the provided Jupyter Notebook (MNIST.ipynb). The objective was to set up MLflow, integrate it with the notebook, and ensure that at least 10 different model variations were logged as separate experiments in the MLflow console.

## Setup

To run the experiments locally, follow these steps:

1. Clone this repository: `git clone https://github.com/Vinayak-VG/CS5830.git`
2. Start the MLflow server: `mlflow ui -p 5100`
3. Open the Jupyter Notebook: `jupyter notebook assign5.ipynb`
4. Execute the notebook cells to train the models and log the experiments to MLflow.

After running the notebook, you should see 10 different experiments in the MLflow console, corresponding to the 10 variations of the neural network model configurations.

## Results

The trained models and their performance metrics are logged in the MLflow tracking server. You can visualize and compare the experiments using the MLflow UI at `http://127.0.0.1:5100`.

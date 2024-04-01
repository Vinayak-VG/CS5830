# Machine Learning Pipeline for Digit Classification

This repository contains the code for a machine-learning pipeline designed for the simple task of digit classification. The pipeline includes data generation, model training, and performance monitoring.

## Files in the Repository

- **dataset.py**: Contains functions for loading and preprocessing the dataset.
- **generate_dataset.py**: Script for generating a synthetic dataset(random rotations) for digit classification.
- **main.py**: Main script to run the entire pipeline.
- **model.py**: Defines the machine learning model architecture.
- **monitor_performance.py**: This module monitors and visualizes model performance.
- **trainer.py**: Module for training the machine learning model.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/digit-classification.git
   ```

2. Generate the dataset:

   ```bash
   python generate_dataset.py
   ```

3. Train the model:

   ```bash
   python main.py
   ```

4. Monitor performance:

   ```bash
   python monitor_performance.py
   ```

## Usage

- Modify the dataset generation parameters in `generate_dataset.py` to generate datasets at various rotation angles.
- Customize the machine learning model architecture in `model.py`.
- Adjust training hyperparameters in `trainer.py` for hyperparameter tuning.
- Use `main.py` to orchestrate the entire pipeline.

## Acknowledgements

- The dataset used in this project is sourced from [MNIST](http://yann.lecun.com/exdb/mnist/).
- The code architecture and structure are inspired by best practices in machine learning development.

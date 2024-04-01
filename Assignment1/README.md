# Machine Learning Pipeline for Digit Classification

This repository contains the code for a machine learning pipeline designed for the simple task of digit classification. The pipeline includes data generation, model training, monitoring performance, and inference functionalities.

## Files in the Repository

- **dataset.py**: Contains functions for loading and preprocessing the dataset.
- **generate_dataset.py**: Script for generating a synthetic dataset for digit classification.
- **main.py**: Main script to run the entire pipeline.
- **model.py**: Defines the machine learning model architecture.
- **monitor_performance.py**: Module for monitoring and visualizing model performance.
- **trainer.py**: Module for training the machine learning model.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/digit-classification.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Generate the dataset:

   ```bash
   python generate_dataset.py
   ```

4. Train the model:

   ```bash
   python main.py
   ```

5. Monitor performance:

   ```bash
   python monitor_performance.py
   ```

## Usage

- Modify the dataset generation parameters in `generate_dataset.py` if needed.
- Customize the machine learning model architecture in `model.py`.
- Adjust training hyperparameters in `trainer.py` as per your requirements.
- Use `main.py` to orchestrate the entire pipeline.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The dataset used in this project is sourced from [MNIST](http://yann.lecun.com/exdb/mnist/).
- The code architecture and structure are inspired by best practices in machine learning development.

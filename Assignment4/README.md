# Dataset Consistency Verification Pipeline

This repository contains the code for setting up a pipeline to verify the consistency of a climatological dataset from the National Centers for Environmental Information. The dataset covers data collected from over 13400 stations from 1901 to 2024, including various readings such as Altimeter, DewPointTemperature, DryBulbTemperature, Precipitation, PresentWeatherType, and more.

## Pipeline Overview

The pipeline aims to extract monthly aggregates from the dataset and compare them against computed monthly averages from daily data points. The comparison is done using the R2 score, with a threshold of 0.9 to determine consistency (C).

## Pipeline Setup and Execution

Follow these steps to set up and run the pipeline:

1. Install Git for source control and DVC for pipeline management.
2. Create a blank project in GitHub and clone it to your local machine.
3. Initialize DVC in the project folder to link it with Git.
4. Use `dvc stage add --run -v -f <script_name>` to add stages to the pipeline.
5. Update `dvc.yaml` and `params.yaml` as needed for your pipeline configuration.
6. Visualize the pipeline DAG using `dvc dag`.
7. Run the pipeline using `dvc repro`. Change parameters in `params.yaml` for different runs.
8. Use `dvc exp show` to list experiment runs and `dvc params diff` to compare experiments.
9. Ensure all versions of experiments are tracked and checked into DVC and GitHub.

## Files in the Repository

- **download.py**: Script to download the climatological dataset.
- **prepare.py**: Prepares the dataset for processing and evaluation.
- **process.py**: Processes the dataset to extract monthly aggregates.
- **evaluate.py**: Evaluates the consistency of monthly aggregates using R2 score.
- **dvc.yaml**: Configuration file for Data Version Control (DVC).
- **params.yaml**: Parameter file for configuring pipeline parameters.
- **data/**: Directory containing the dataset.

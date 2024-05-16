# Deepfake Detection Project

This project aims to develop a pipeline for Deepfake detection, incorporating various components such as Apache Spark, Apache Airflow, MLFlow, REST API, Prometheus, Grafana, and Docker.

## Project Structure

The project is structured as follows:
<!-- 
deepfake-detection/
* data/
    * raw/
    * processed/
* notebooks/
* src/
    * data/
    * models/
    * api/
    * utils/
* docs/
* models/
* metrics/
* reports/
* figures/
* .gitignore
* README.md
* requirements.txt
* Dockerfile
* docker-compose.yml -->

## Setup

1. Clone the repository:

```bash
git clone https://https://github.com/Vinayak-VG/CS5830.git
cd deepfake-detection
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Data Preprocessing (Apache Spark)
The data preprocessing pipeline is implemented using Apache Spark. It includes the following steps:

- Data acquisition automation
- Data cleansing
- Data munging
- Data transformation
- Data vectorization

To run the data preprocessing pipeline, execute the following command:
```
spark-submit src/data/preprocess.py
```

This will load the raw data from data/raw, perform the necessary preprocessing steps, and save the processed data to data/processed.

4. Pipeline Orchestration (Apache Airflow)
The pipeline orchestration is managed using Apache Airflow. The Airflow DAGs are defined in the airflow/dags directory.
To start the Airflow webserver and scheduler, run:
```
airflow webserver --port 8080
airflow scheduler
```
You can then access the Airflow UI at http://localhost:8080 and monitor the progress of your DAGs.

5. Model Building and Tracking (MLFlow)
The model building process is tracked using MLFlow. You can log model parameters, metrics, and artifacts to the MLFlow tracking server.
To start the MLFlow tracking server, run:
```
mlflow server --backend-store-uri /path/to/mlflow/tracking/dir --default-artifact-root /path/to/mlflow/artifacts
```
You can then log model runs and retrieve experiment details using the MLFlow Python API.

6. REST API and Instrumentation
The project includes a REST API for serving the Deepfake detection model. The API endpoints are defined in src/api/app.py.
To start the API server, run:
```
uvicorn src.api.app:app --reload
```

The API is instrumented with Prometheus to capture metrics. You can access the Prometheus metrics endpoint at http://localhost:8000/metrics.

7. Grafana Dashboard
A Grafana dashboard is provided to visualize the captured metrics from Prometheus. To set up Grafana, follow these steps:

- Install and start Grafana.
- Import the provided Grafana dashboard configuration from grafana/dashboard.json.
- Configure the Grafana data source to point to your Prometheus instance.

8. Docker Deployment
The instrumented REST API can be deployed as a Docker container for easy deployments with resource limitations and port mapping.
To build the Docker image, run:
```
docker build -t deepfake-detection-api .
```

To run the Docker container, execute:
```
docker run -p 8000:8000 deepfake-detection-api
```

This will start the API server and expose it on http://localhost:8000.

License
This project is licensed under the MIT License.
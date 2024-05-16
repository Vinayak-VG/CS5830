# FastAPI Application with Prometheus Monitoring and Dockerization

This repository contains code and instructions for implementing Task 1 and Task 2 of the assignment, which involves setting up Prometheus monitoring and Dockerizing a FastAPI application.

## Task 1: Prometheus Monitoring

### Code Overview
- `main.py`: Contains the FastAPI application code with Prometheus monitoring hooks.
- `prometheus.yml`: Prometheus configuration for scraping metrics from the FastAPI application.
- `grafana_dashboard.json`: Sample Grafana dashboard configuration for visualizing metrics.

### Implementation Steps
1. Install required libraries:
   ```bash
   pip install fastapi prometheus-fastapi-instrumentator

2. Modify FastAPI code to include Prometheus monitoring hooks.
    - Track API usage from different client IP addresses using counters.
    - Export metrics such as API run time, T/L time, etc.
3. Configure Prometheus (prometheus.yml) to scrape metrics from FastAPI application.
4. Visualize metrics in Grafana using the provided grafana_dashboard.json.

## Task 2: Dockerization and Cluster Setup

### Code Overview
- `Dockerfile`: Docker configuration for containerizing the FastAPI application.
- `docker-compose.yml`: Docker Compose configuration for setting up multiple instances.

### Implementation Steps
1. Dockerize the FastAPI application:

2. Build Docker image using the provided Dockerfile.
``` 
docker build -t fast_api_task1 .
```
3. Run Docker container with appropriate port mappings.
```
docker run -d -p 8000:8000 -p 9090:9090 fast_api_task1
```
4. Set CPU utilization limit and scale up instances as needed.
```
docker run -d -p 8000:8000 -p 9090:9090 --cpus 1 fast_api_task1
```

5. Configure Prometheus to monitor the Dockerized FastAPI cluster.
```
docker run -d -p 8001:8000 -p 9091:9090 fast_api_task1
docker run -d -p 8002:8000 -p 9092:9090 fast_api_task1
```

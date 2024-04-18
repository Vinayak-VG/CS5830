# Climatological Data Pipeline with Apache Airflow

This repository contains the code for setting up a data pipeline using Apache Airflow to acquire public domain climatological data from the National Centers for Environmental Information (NCEI). The pipeline performs various tasks such as fetching data files, processing them, generating visualizations, and creating animations.

## Assignment Outline

The assignment outlines the following tasks to be performed by the data pipeline:

1. Fetch the location-wise datasets for a specified year from NCEI.
2. Randomly select data files based on requirements.
3. Fetch individual data files and zip them into an archive.
4. Place the archive at a specified location.
5. Unzip the archive and process individual CSV files.
6. Compute monthly averages of required fields.
7. Generate data visualizations using heatmaps.
8. Create a GIF animation using monthly data.

## Files in the Repository

- **datapipeline.py**: Contains code for the first 5 tasks of the assignment, including fetching, selecting, fetching individual files, zipping, and placing the archive.
- **dataanalytics.py**: Includes code for the remaining tasks (6 to 8), such as processing CSV files, computing averages, generating visualizations, and creating animations.
- **anim_final.avi**: Contains the final GIF animation created by the pipeline.
- **heatmap.png**: Contains the Heatmap created by the pipeline.

## Usage

1. Clone the repository to your local machine:

   ```markdown
   git clone https://github.com/Vinayak-VG/CS5830.git
   cd Assignment2
   ```

2. Install Apache Airflow and necessary dependencies:

   ```markdown
   pip install apache-airflow
   ```

3. Set up Apache Airflow environment and configure the DAGs (Directed Acyclic Graphs) for `datapipeline.py` and `dataanalytics.py` 

4. Start the Airflow scheduler and web server:

   ```markdown
   airflow scheduler &
   airflow webserver -p 8080 &
   ```

5. Access the Airflow web interface at `http://localhost:8080` to monitor and manage the data pipeline.

6. Trigger the DAGs manually or set them to auto trigger as specified in the assignment outline.

## Requirements

- Python 3.x
- Apache Airflow
- pandas
- geopandas
- geodatasets
- Apache Beam
- ffmpeg (optional for creating GIF animation)

## Acknowledgements

- This project uses data from the National Centers for Environmental Information (NCEI).
- Visualization and processing tasks are implemented using Apache Beam and geospatial libraries like geopandas.
- GIF animation creation requires suitable tools like ffmpeg.

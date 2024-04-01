from airflow import DAG
from airflow.providers.airflow.sensors.file import FileSensor
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io.filesystems import FileSystems
from apache_beam.options.pipeline_options import PipelineOptions
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cv2
from shapely.geometry import Point, Polygon

# Replace with your DAG details
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'data_analytics',
    default_args=default_args,
    description='Data Analytics Pipeline',
    schedule_interval=None,
)

# Sensor to wait for file
wait_for_file = FileSensor(
    task_id='wait_for_file',
    poke_interval=10,  # Check every 10 seconds
    timeout=300,  # Timeout after 5 minutes (300 seconds)
    filepath='/path/to/your/archive.zip',
    dag=dag,
)

# Check if archive is valid
check_valid_archive = BashOperator(
    task_id='check_valid_archive',
    bash_command='unzip -tq /path/to/your/archive.zip && echo "Archive is valid"',
    dag=dag,
)

# Unzip files
unzip_files = BashOperator(
    task_id='unzip_files',
    bash_command='unzip -o /path/to/your/archive.zip -d /path/to/extract',
    dag=dag,
)

# Extract CSV files
extract_csv_files = BashOperator(
    task_id='extract_csv_files',
    bash_command='cd /path/to/extract && find . -name "*.csv" -exec mv {} /path/to/extracted_files \;',
    dag=dag,
)

# Task to extract and filter CSVs
def extract_csvs_and_convert_to_tuples(path_to_csvs):
    def process_dataframes_to_tuples(dataframes):
        # Processing logic
        dataframe_list = []
        all_csvs_tuples = []
        for dataframe in dataframes:
            tuple_list = []
            # dataframe_cleaned = dataframe.iloc[:, [2, 3, 4, 9, 10, 13, 14, 15, 17, 18, 20, 21, 23]]
            dataframe_cleaned = dataframe.iloc[:, [0, 3, 4]]
            tuple_list.extend([dataframe.iloc[1, 2], dataframe.iloc[1, 3]])
            hourly_data_list = []
            for column in range(dataframe_cleaned.shape[1]):
                hourly_data_list.append(list(dataframe_cleaned.iloc[:, column]))
            tuple_list.append(hourly_data_list)
            dataframe_list.append(dataframe_cleaned)
            all_csvs_tuples.append(tuple_list)
        
        return all_csvs_tuples

    with beam.Pipeline(options=PipelineOptions()) as pipeline:
        # Read CSV files
        csv_files = (pipeline
                     | 'Read CSV Files' >> beam.Create(FileSystems.match([f'{path_to_csvs}*.csv'])[0].metadata_list)
                     | 'Read CSV' >> beam.Map(lambda file: pd.read_csv(file.path))
                    )

        # Filter required fields and extract Lat/Long
        filtered_data = (csv_files
                         | 'Extract the Lat, Long, Parameter Values' >> beam.Map(process_dataframes_to_tuples)
                        )

extract_filter_task = PythonOperator(
    task_id='extract_filter_task',
    python_callable=extract_csvs_and_convert_to_tuples,
    dag=dag,
)

# Task to create monthly averages
def pipeline_create_averages():
    # Processing logic
    def create_monthly_averages(all_csvs_tuples):
        final_all_locations_monthly_averages = []
        # print(all_csvs_tuples)
        # quit()
        for location_list in all_csvs_tuples:
            final_list = []
            final_list.extend([location_list[0], location_list[1]])
            month = 1
            all_months_average = {}
            for columns in range(1, len(location_list[2])):
                all_months_average[columns] = []
            hourly_data_list = {}
            for columns in range(1, len(location_list[2])):
                hourly_data_list[columns] = []
            for date in range(len(location_list[2][0])):
                if int(location_list[2][0][date][5:7]) == month:
                    for columns in range(1, len(location_list[2])):
                        hourly_data_list[columns].append(location_list[2][columns][date])
                else:
                    month = month + 1
                    for columns in range(1, len(location_list[2])):
                        all_months_average[columns].append(sum(hourly_data_list[columns])/len(hourly_data_list[columns]))
                        hourly_data_list[columns] = []
            for columns in range(1, len(location_list[2])):
                final_list.append(all_months_average[columns])
            final_all_locations_monthly_averages.append(final_list)
        return final_all_locations_monthly_averages
    
    with beam.Pipeline(options=PipelineOptions()) as pipeline:
        # Filter required fields and extract Lat/Long
        monthly_averaged_data = (pipeline
                            | 'Extract the Lat, Long, Parameter Values' >> beam.Map(create_monthly_averages)
                            )

monthly_average_task = PythonOperator(
    task_id='monthly_average_task',
    python_callable=pipeline_create_averages,
    dag=dag,
)

# Task to plot heat maps
def plot_heat_maps():
    # Plotting logic
    def create_world(df):
        SHAPEFILE = 'ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp'
        worldmap = gpd.read_file(SHAPEFILE)[['ADMIN', 'ADM0_A3', 'geometry']]
        # # Rename columns.
        worldmap.columns = ['country', 'country_code', 'geometry']

        worldmap = worldmap.drop(worldmap.loc[worldmap['country'] == 'Antarctica'].index)
        # Print the map
        worldmap.plot(figsize=(20, 20), edgecolor='white', linewidth=1, color='lightblue')
        crs = {'init':'EPSG:4326'}
        geometry = [Point(xy) for xy in zip(df['LONGITUDE'], df['LATITUDE'])]
        geo_df = gpd.GeoDataFrame(df, 
                                crs = crs, 
                                geometry = geometry)
        
        return worldmap, geo_df


    def create_heat_maps(worldmap, geo_df):
        fig, ax = plt.subplots(figsize = (10,10))
        from matplotlib.colors import BoundaryNorm, ListedColormap
        my_colors = ['blue', 'gold', 'orange', 'red', 'darkred']
        my_cmap = ListedColormap(my_colors)
        bounds = [0, 2, 4, 6, 8, 10]
        my_norm = BoundaryNorm(bounds, ncolors=len(my_colors))
        worldmap.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
        geo_df.plot(column = 'Hour Data', ax=ax, cmap = my_cmap, norm=my_norm,
                    legend = True, legend_kwds={'shrink': 0.3}, 
                    markersize = 10)
        # ax.set_title('Kings County Price Heatmap')
        plt.savefig('Heat Map')

    with beam.Pipeline(options=PipelineOptions()) as pipeline:
        # Filter required fields and extract Lat/Long
        heatmaps = (pipeline
                         | 'Filter Fields' >> beam.Map(create_world)
                         | 'Extract Lat/Lon' >> beam.Map(create_heat_maps)
                         )


plotting_heatmaps = PythonOperator(
    task_id='plotting_heatmaps',
    python_callable=plot_heat_maps,
    dag=dag,
)

# Task to create animation
def create_animation():
    # Animation creation logic
    def geo_anim():
        img_array = []
        image_folder = "plots"
        video_name = 'anim.gif'
        images = [img for img in sorted(os.listdir(image_folder)) if img.endswith(".png")]

        for filename in images:
            img = cv2.imread(os.path.join(image_folder, filename))
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        
        
        out = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()


    with beam.Pipeline(options=PipelineOptions()) as pipeline:
        # Filter required fields and extract Lat/Long
        animation = (pipeline
                         | 'Create Video Animation' >> beam.Map(geo_anim)
                         )
        


Animation_Creator = PythonOperator(
    task_id='Animation_Creator',
    python_callable=create_animation,
    dag=dag,
)

# Task to delete CSV file
delete_csv_file = BashOperator(
    task_id='delete_csv_file',
    bash_command='rm /path/to/your/archive.zip',  # Replace with the actual path to your CSV file
    dag=dag,
)

# Define task dependencies
wait_for_file >> check_valid_archive >> unzip_files >> extract_csv_files >> extract_filter_task >> monthly_average_task >> plotting_heatmaps >> Animation_Creator >> delete_csv_file

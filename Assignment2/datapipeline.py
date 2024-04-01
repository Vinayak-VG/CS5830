from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import random
import os
import zipfile
import urllib.request
from inscriptis import get_text
import subprocess

# Define DAG arguments
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Function to fetch all links from a specific website
def get_all_links():
    years = list(range(2023, 2024))
    all_links = []
    for year in years:
        baseurl = f"https://www.ncei.noaa.gov/data/local-climatological-data/access/" + str(year) + "/"
        html = urllib.request.urlopen(baseurl).read().decode('utf-8')
        text = get_text(html)
        for i in range(len(text)-15):
            if ".csv" in text[i+11:i+15]:
                url = baseurl + text[i:i+15]
                all_links.append(url)
    return all_links

# Function to select random URLs from the list
def select_urls(csvs_list):
    return random.sample(eval(csvs_list), 5)

# Function to fetch CSVs from given URLs
def fetch_csvs_from_urls(list_of_urls):
    for url in eval(list_of_urls):
        subprocess.run(f"wget {url} -P downloads/2023/", shell=True)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

# Function to zip all CSV files and place at a required location
def zipallfiles_and_placeatrequiredlocation():
    os.makedirs("downloads/", exist_ok=True)
    zipfilename = "download_2023_csvs.zip"
    with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir("downloads/", zipf)

    required_location = "final_location/"
    subprocess.run([f"mv download_2023_csvs.zip {required_location}"], shell=True)

# Define the DAG
with DAG('datapipeline_Take4', 
         default_args=default_args,
         start_date=datetime(2024, 3, 1, 4),
         schedule='*/2 * * * *',
         catchup=False) as dag:

    fetch_datasets = PythonOperator(
        task_id='get_all_links',
        python_callable=get_all_links,
    )

    select_files = PythonOperator(
        task_id='select_urls',
        python_callable=select_urls,
        op_kwargs={'csvs_list':"{{ ti.xcom_pull(task_ids='get_all_links') }}"}
    )

    fetch_files = PythonOperator(
        task_id='fetch_csvs_from_urls',
        python_callable=fetch_csvs_from_urls,
        op_kwargs={'list_of_urls':"{{ ti.xcom_pull(task_ids='select_urls') }}"}
    )

    zip_files_task = PythonOperator(
        task_id='zipallfiles_and_placeatrequiredlocation',
        python_callable=zipallfiles_and_placeatrequiredlocation,
    )

    fetch_datasets >> select_files >> fetch_files >> zip_files_task

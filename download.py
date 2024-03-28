import subprocess
import os
import yaml

def download_csv(files):
    for url in files:
        # Use subprocess to run wget command to download files
        subprocess.run(f"wget {os.path.join('https://www.ncei.noaa.gov/data/local-climatological-data/access/2023/', url)} -P data/", shell=True)

if __name__ == "__main__":
    # Load parameters from the YAML file
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
        
    # Create 'data' directory if it doesn't exist
    os.makedirs("data/", exist_ok=True)
    
    # Call download_csv function with file names from params
    download_csv(params["params"]["file_names"])
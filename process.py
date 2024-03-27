import pandas as pd
import pickle
import yaml

def compute_averages(csv_path, readings=[[34, 53]]):
    # Load the CSV file containing climatological data
    geo_data = pd.read_csv(csv_path)
    
    # Initialize a dictionary to store monthly reading averages
    monthly_reading_average = {}
    
    # Iterate through the specified readings to compute monthly averages
    for idx in readings:
        monthly_reading_average[geo_data.columns[idx[0]]] = []
        
    month_count = 0
    for i in range(geo_data.shape[0]):
        for idx in readings:
            # Check for non-null values to compute averages
            if not pd.isnull(geo_data.iloc[i, idx[1]]):
                # Compute the monthly average and round to 2 decimal places
                monthly_reading_average[geo_data.columns[idx[0]]].append(round(geo_data.iloc[month_count:i, idx[0]].mean(), 2))
                month_count = i
    
    # Save the computed monthly reading averages to a pickle file
    with open('compute.pickle', 'wb') as handle:
        pickle.dump(monthly_reading_average, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    # Load parameters from the YAML file
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
        
    # Call the compute_averages function with specified CSV path and readings indices
    compute_averages("data/99999913724.csv", params["params"]["compute_index"])
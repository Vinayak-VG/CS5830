import pandas as pd
import pickle
import yaml

def prepare_gt(csv_path, readings=[53]):
    # Load the CSV file containing climatological data
    geo_data = pd.read_csv(csv_path)
    
    # Initialize a dictionary to store monthly reading averages
    monthly_reading_average = {}
    
    # Iterate through the specified readings to compute monthly averages
    for idx in readings:
        monthly_reading_average[geo_data.columns[idx]] = []
        
    # Compute monthly averages for each specified reading
    for i in range(geo_data.shape[0]):
        for idx in readings:
            if not pd.isnull(geo_data.iloc[i, idx]):
                monthly_reading_average[geo_data.columns[idx]].append(geo_data.iloc[i, idx])
                
    # Save the computed monthly reading averages to a pickle file
    with open('gt.pickle', 'wb') as handle:
        pickle.dump(monthly_reading_average, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    # Load parameters from the YAML file
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
        
    # Call the prepare_gt function with specified CSV path and readings index
    monthly_reading_average = prepare_gt("data/99999913724.csv", params["params"]["gt_index"])
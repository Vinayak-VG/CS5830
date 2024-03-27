import pandas as pd
import numpy as np
import pickle

def compute_averages(csv_path, readings=[[34, 53]]):
    geo_data = pd.read_csv(csv_path)
    monthly_reading_average = {}
    for idx in readings:
        monthly_reading_average[geo_data.columns[idx[0]]] = []
    month_count = 0
    for i in range(geo_data.shape[0]):
        for idx in readings:
            if not pd.isnull(geo_data.iloc[i, idx[1]]):
                monthly_reading_average[geo_data.columns[idx[0]]].append(round(geo_data.iloc[month_count:i, idx[0]].mean(), 2))
                month_count = i
    with open('compute.pickle', 'wb') as handle:
        pickle.dump(monthly_reading_average, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    monthly_reading_average = compute_averages("/Users/prasannakumargupta/CS5830/Assignment3/data/99999913724.csv")
    print(monthly_reading_average)
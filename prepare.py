import pandas as pd
import numpy as np
import pickle

def prepare_gt(csv_path, readings=[53]):
    geo_data = pd.read_csv(csv_path)
    monthly_reading_average = {}
    for idx in readings:
        monthly_reading_average[geo_data.columns[idx]] = []
    for i in range(geo_data.shape[0]):
        for idx in readings:
            if not pd.isnull(geo_data.iloc[i, idx]):
                monthly_reading_average[geo_data.columns[idx]].append(geo_data.iloc[i, idx])
    with open('gt.pickle', 'wb') as handle:
        pickle.dump(monthly_reading_average, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    monthly_reading_average = prepare_gt("/Users/prasannakumargupta/CS5830/Assignment3/data/99999913724.csv")
    print(monthly_reading_average)
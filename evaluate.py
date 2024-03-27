from sklearn.metrics import r2_score
import pickle

def evaluate(pred_pkl, gt_pkl):
    # Load predicted and ground truth data from pickle files
    with open(pred_pkl, 'rb') as handle:
        pred = pickle.load(handle)
    with open(gt_pkl, 'rb') as handle:
        gt = pickle.load(handle)
    
    # Initialize a dictionary to store R2 scores for each reading
    r2_metric = {}
    
    # Compute R2 score for each reading and store in the dictionary
    for i in range(len(list(pred.keys()))):
        reading_name = list(pred.keys())[i]
        pred_values = pred[reading_name]
        gt_values = gt[reading_name]
        r2_metric[reading_name] = r2_score(pred_values, gt_values)
    
    # Save the computed R2 scores to a pickle file
    with open('r2_score.pickle', 'wb') as handle:
        pickle.dump(r2_metric, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    # Call the evaluate function with predicted and ground truth pickle file paths
    evaluate("compute.pickle", "gt.pickle")
    print("R2 scores computed and saved to 'r2_score.pickle'")

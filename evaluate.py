from sklearn.metrics import r2_score
import pickle

def evaluate(pred_pkl, gt_pkl):
    with open(pred_pkl, 'rb') as handle:
        pred = pickle.load(handle)
    with open(gt_pkl, 'rb') as handle:
        gt = pickle.load(handle)
    r2_metric = {}
    for i in range(len(list(pred.keys()))):
        r2_metric[list(pred.keys())[i]] = r2_score(pred[list(pred.keys())[i]], gt[list(gt.keys())[i]])
    with open('r2_score.pickle', 'wb') as handle:
        pickle.dump(r2_metric, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    r2_score = evaluate("/Users/prasannakumargupta/vinayak/IITM/CS5830/compute.pickle", "/Users/prasannakumargupta/vinayak/IITM/CS5830/gt.pickle")
    print(r2_score)
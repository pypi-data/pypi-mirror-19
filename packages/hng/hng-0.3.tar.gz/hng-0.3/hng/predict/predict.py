from sklearn.metrics import confusion_matrix
import pandas as pd

def confuse_me(url, true_name, pred_name):
    """
    Precision = tp/(tp+fp)
    Specificity = tn/(tn+fp)
    Recall = accuracy
    """
    return_stats = {}
    for i in range(len(url)):
        df = pd.read_csv(url[i])
        y_true = df[true_name].tolist()
        y_pred = df[pred_name].tolist()
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
        tp = cm[0][0]
        fn = cm[0][1]
        fp = cm[1][0]
        tn = cm[1][1]
        precision = float(tp)/float(tp+fp)
        specificity = float(tn)/float(tn+fp)
        recall = float(tp)/float(tp+fn)
        return_stats[url[i].split("_")[1]] = [precision, specificity, recall]
    df = pd.DataFrame.from_dict(return_stats)
    df.rename(index=dict(zip([0,1,2],["precision", "specificity", "recall"])),inplace=True)
    #df.to_csv("static_stats_1.csv")
    return df
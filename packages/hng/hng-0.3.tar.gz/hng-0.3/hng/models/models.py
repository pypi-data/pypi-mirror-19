from markdown import markdown
import pandas as pd
import numpy as np
import tensorflow as tf
import re
import h2o
from h2o.estimators.random_forest import H2ORandomForestEstimator
from sklearn.metrics import confusion_matrix




class OneVSAll(object):
    """
    Create a One-VS-All wrapper Class for multilabel classification
    """

    def __init__(self):
        self._author = "nilesh"
        self._kernel = "drf"
        self._features = []           #feature columns from the DataFrame
        self._ignore_columns = []
        self._label = ''
        self._models_list = []
        self._modes = 0
        self._n_labels = 0


    def _create_OvA_df(self, data, label, label_value):
        data[label] = data[label].apply(lambda x: label_value if x == label_value else "Other")
        return data
    #def _build_forest()

    def list_models(self):
        return [key for key in self._models_dict.iterkeys()]

    def train(self, df, label,balance_classes=False ,ignore_columns=[], ntrees=50, max_depth=10, kernel="drf"):

        self._label = label
        self._uniq_labels = df[label].unique().tolist()
        self._n_labels = len(self._uniq_labels)
        self._models_dict = {}
        df_dict = {}
        for i in self._uniq_labels:
            df_dict["df"+"{:s}".format(i).replace(" ","_")] = self._create_OvA_df(pd.DataFrame.copy(df), self._label, i)
            hframe = h2o.H2OFrame(df_dict["df"+"{:s}".format(i).replace(" ","_")])
            X = hframe.col_names[1:-1] #ignore encounter_id column
            y = hframe.col_names[-1]
            train, valid, test = hframe.split_frame([0.7,0.2], seed=np.random.randint(137,729927007,1)[0])
            self._models_dict["drf"+"{:s}".format(i).replace(" ","_")] = H2ORandomForestEstimator(model_id="drf"+"{:s}".format(i).replace(" ","_"), ntrees=ntrees, max_depth=max_depth, balance_classes=balance_classes)
            self._models_dict["drf"+"{:s}".format(i).replace(" ","_")].train(X, y, training_frame=train, validation_frame=valid)
            path = h2o.save_model(self._models_dict["drf"+"{:s}".format(i).replace(" ","_")], force=True)
            print("Model saved at %s" %path)
        return "Models trained!"

    def predict(self, sample):
        #sample is a Pandas DataFrame with a single row
        hframe = h2o.H2OFrame(sample[sample.columns.tolist()[:-1]])
        p = {}#pd.DataFrame(columns=self._uniq_labels)
        keys = []
        for key in self._models_dict.iterkeys():
            print "Enterred the loop"
            p[key] = self._models_dict[key].predict(hframe)
            keys.append(key)
        for i in range(len(keys)-1):
            p[keys[i+1]] = p[keys[i]].cbind(p[keys[i+1]])
        dx =  p[keys[i+1]].as_data_frame(use_pandas=True)[self._uniq_labels]
        return dx

    def predict_batch(self, df):
        hframe = h2o.H2OFrame(df)
        p = {}#pd.DataFrame(columns=self._uniq_labels)
        keys = []
        for key in self._models_dict.iterkeys():
            print "Enterred the loop"
            p[key] = self._models_dict[key].predict(hframe)
            keys.append(key)
        for i in range(len(keys)-1):
            p[keys[i+1]] = p[keys[i]].cbind(p[keys[i+1]])
        dx =  p[keys[i+1]].as_data_frame(use_pandas=True)[self._uniq_labels]
        dx["predict"] = dx.idxmax(axis=1)
        return dx["predict"]


    def my_function(self):
        #print self._new_var
        for i in range(5):
            self._models_list.append(i*i +10)
            print self._models_list[i]
        return "My objective is to create a wrapper for OneVSAll for the given kernel."




    def test_wrapper(self,param):
        self._models_list = param
        for i in range(self._models_list):
            print ("self._models_list"+"{:d}".format(i))
        print self._models_list
        self._new_var = 69
        print self._new_var
        return "Did it?"





class MGCrisis(object):
    def __init__(self):
        self._author = "nilesh"
        self._model = None

    def train(self, df, target_class, balance_classes=False ,ignore_columns=[], ntrees=50, max_depth=10, kernel="drf"):

        self._target_class = target_class

        hframe = h2o.H2OFrame(df)
        feat_cols = hframe.col_names[1:-1]
        label_col = hframe.col_names[-1]

        train, valid, test = hframe.split_frame([0.7,0.2], seed=137)

        self._model = H2ORandomForestEstimator(model_id="mgcrisis",ntrees=ntrees, max_depth=max_depth,balance_classes=balance_classes)

        self._model.train(feat_cols,label_col,training_frame=train, validation_frame=valid)
        path = h2o.save_model(self._model, force=True)
        print("Model saved at %s" %path)

        return "MG Crisis Model trained and ready for prediction."

    def predict(self, sample):
        #sample is a Pandas DataFrame with a single row
        hframe = h2o.H2OFrame(sample[sample.columns.tolist()[:-1]])
        y_pred = self._model.predict(hframe)
        y_pred = y_pred.as_data_frame(use_pandas=True)
        return y_pred
        
    def get_stats(self, y_true, y_pred):
        """
        Precision = tp/(tp+fp)
        Specificity = tn/(tn+fp)
        Recall = accuracy
        """
        return_stats = {}
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
        tp = cm[0][0]
        fn = cm[0][1]
        fp = cm[1][0]
        tn = cm[1][1]
        precision = float(tp)/float(tp+fp)
        specificity = float(tn)/float(tn+fp)
        recall = float(tp)/float(tp+fn)
        return_stats[self._model.model_id] = [precision, specificity, recall]
        df = pd.DataFrame.from_dict(return_stats)
        df.rename(index=dict(zip([0,1,2],["precision", "specificity", "recall"])),inplace=True)
        #df.to_csv("static_stats_1.csv")
        return df



    

    def my_function(self):
        return "My function is to create an MGCrisis object."


class CKDCrisis(object):
    def __init__(self):
        self._author = "nilesh"
        self._model = None

    def train(self, df, target_class, balance_classes=False ,ignore_columns=[], ntrees=50, max_depth=10, kernel="drf"):

        self._target_class = target_class

        hframe = h2o.H2OFrame(df)
        feat_cols = hframe.col_names[1:-1]
        label_col = hframe.col_names[-1]

        train, valid, test = hframe.split_frame([0.7,0.2], seed=137)

        self._model = H2ORandomForestEstimator(model_id="ckdcrisis",ntrees=ntrees, max_depth=max_depth,balance_classes=balance_classes)

        self._model.train(feat_cols,label_col,training_frame=train, validation_frame=valid)
        path = h2o.save_model(self._model, force=True)
        print("Model saved at %s" %path)

        return "CKD Crisis Model trained and ready for prediction."

    def predict(self, sample):
        #sample is a Pandas DataFrame with a single row
        hframe = h2o.H2OFrame(sample[sample.columns.tolist()[:-1]])
        y_pred = self._model.predict(hframe)
        y_pred = y_pred.as_data_frame(use_pandas=True)
        return y_pred

    def get_stats(self, y_true, y_pred):
        """
        Precision = tp/(tp+fp)
        Specificity = tn/(tn+fp)
        Recall = accuracy
        """
        return_stats = {}
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
        tp = cm[0][0]
        fn = cm[0][1]
        fp = cm[1][0]
        tn = cm[1][1]
        precision = float(tp)/float(tp+fp)
        specificity = float(tn)/float(tn+fp)
        recall = float(tp)/float(tp+fn)
        return_stats[self._model.model_id] = [precision, specificity, recall]
        df = pd.DataFrame.from_dict(return_stats)
        df.rename(index=dict(zip([0,1,2],["precision", "specificity", "recall"])),inplace=True)
        #df.to_csv("static_stats_1.csv")
        return df

    def my_function(self):
        return "My function is to create a CKDCrisis object."





class Medicines(object):
    def __init__(self):
        self._author = "nilesh"
    def my_function(self):
        return "My function is to create a Medicines object."

    def get_bayes_prob(self, df, A, M, d):
            for k, v in d.iteritems():
                if k == M:
                    colnum = v
            m_given = np.sum(A[:, colnum], axis=0)/float(np.sum(np.sum(A, axis=0), axis=1))

            disc_stat = dict(Counter(df.dischg_disp_code_desc))
            b = disc_stat['negative']
            d_negative = float(b)/df.shape[0]

            #md_condition
            location = df[df.dischg_disp_code_desc == 'negative'].index.tolist()
            A2 = A[location]
            md_condition = np.sum(A2[:, colnum], axis=0)/ float(np.sum(np.sum(A2, axis=0), axis=1))
            return (m_given, d_negative, md_condition) 



class TimelineData(object):
    def __init__(self):
        self._author = "nilesh"
        self._weights = {}
        self._biases = {}

    def say_hi(self):
        return markdown("hi " + self._nilesh)

    def my_function(self):
        return "My function is to create a TimelineData object."

    def predict_next_data(self, df):
        def get_tf():
            return
        return

            # y_ = tf.Variable((tf.zeroes())
            #for i in len(layers):
            #   w_i, b_i as tf.Variable
            #   y_ = activate(y_, wi, bi)
            #return y_
        #tf.saver for weights and biases
        #y = get_tf()
        #with tf.Session() as sess:
        #   sees(init)
        #   saver.restore(sess, "loc")
        #   return sess.run(y)



class GeneralClass(object):
    def __init__(self):
        pass
    def get_encounter_level_similarity(self,pt_id):
        client = MongoClient("mongodb://localhost:27017")
        hng = client.healthnextgen_development
        enc = hng.native_encounters
        df = pd.DataFrame(list(enc.find({"patient_sk":{"$eq":pt_id}}))) #patient_id for now, change it to patient_sk
        enc_id = list(df.loc[df[df.patient_sk== int(pt_id)].index.tolist(), "encounter_id"])
        labs = hng.native_lab_procedures
        labs = pd.DataFrame(list(labs.find({"encounter_id":{"$in":enc_id}})))
        labs = labs[['lab_procedure_name', 'encounter_id', 'numeric_result']]
        labs.numeric_result = labs.numeric_result.replace('', np.nan)
        labs.dropna(inplace=True)
        labs.numeric_result = labs.numeric_result.astype(float)
        labs = labs.pivot_table(index='encounter_id',columns='lab_procedure_name',values='numeric_result', aggfunc=np.mean)
        labs.fillna(0.0, inplace=True)
        sim = cosine_similarity(labs,labs)
        src = []
        trg = []
        wt = []
        for i in range(len(labs.index)):
            src.append(labs.index[i])
            trg.append(labs.index[sim[i].argsort()[::-1].tolist()[1:]].tolist())
            wt.append(sim[i][sim[i].argsort()[::-1].tolist()[1:]].tolist())
        result = dict(zip(src,zip(trg,wt)))
        res1 = jsonify(zip(src,trg))
        return res1

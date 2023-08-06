#test358_1 = list(set(sum(df.labs_taken[df.diagnosis_code.apply(lambda x: True if '358.01' in np.array(x) else False)].tolist(),[])))
import pandas as pd
import numpy as np
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.healthnextgen_development


#return a Pandas DataFrame after removing columns with variance less than given threshold
def remove_const_cols(df, var_to_drop=0.0):
    #df
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("Argument should be a pandas DataFrame.")
    #have to exclude enum features
    #DONE
    enum_df = df.select_dtypes(include=['object'])
    num_df = df.select_dtypes(exclude=['object'])
    num_df = num_df.loc[:, num_df.var() > var_to_drop]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    return pd.concat([num_df, enum_df], axis=1)

#all those columns for which less than 10 are missing
#df.loc[:,df.isnull().sum() <10]
def impute_missing():
    return

def missing_stats(df, percentage):
    if not isinstance(df, pandas.core.frame.DataFrame):
        raise TypeError("Argument should be a Pandas DataFrame.")
    percentage = float(percentage)
    df = df.loc[:,df.isnull().sum() < percentage*len(df)]
    _, n_cols = df.shape
    cols = df.columns.tolist()
    return cols#n_cols

def get_icds_labs_by_priority(priority=10):
    """
    Get all the labs tests and the ICD codes for top $priority$ priorities per encounter.
    Part of the pre-preprocessing pipeline.
    Intended use is to segment lab tests by top $priority$ ICD codes and then train a classifier per segment.

    Parameters
    ----------
    priority : int, positive
        Upto which diagnosis priorities to inquire for.

    Attributes
    ----------

    Returns
    -------
    df : A Pandas DataFrame
        A Pandas DataFrame of shape (n_possible_encounters, 2):
            column types = List(str), List(str)

    See also
    --------
    """
    import pandas as pd
    import numpy as np
    from pymongo import MongoClient



    #make sure the file all_enc_with_labs.npy exists
    encounters = np.load("all_enc_with_labs.npy").tolist()
    #print encounters
    #print "Yeah, inside %d" %priority
    #return
    #coming to this step is itself another pre-preprocessing task. Let's skip for the moment
    #labs = pd.read_csv("all_labs_all_enc.csv")
    client = MongoClient("mongodb://localhost:27017")
    db = client.hng_ml
    comorb = db.native_comorbs
    df = pd.DataFrame(list(comorb.find({"diagnosis_priority":{"$in":range(10)}, "encounter_id":{"$in":encounters}})))
    labsT = pd.read_csv("all_labs_all_enc.csv")#pd.DataFrame(labs)
    labsT.rename(index=dict(zip(labsT.index.tolist(), labsT.encounter_id.tolist())), inplace=True)
    labsT = pd.DataFrame(labsT.T)
    xnxx = pd.DataFrame(columns=["encounter_id","labs_taken"])
    #xnxx.append(pandas.DataFrame([[137.0, 333]],columns = ["encounter_id","labs_taken"]),ignore_index=True)
    #xnxx.append(pandas.DataFrame([[x, labsT[x].dropna().index.tolist()[1:]]],columns = ["encounter_id","labs_taken"]),ignore_index=True)
    for x in labsT.columns.tolist():
        xnxx = xnxx.append(pd.DataFrame([[x, labsT[x].dropna().index.tolist()[1:]]],columns = ["encounter_id","labs_taken"]),ignore_index=True)
        print "Done for %d" %x
    xnxx.to_csv("labs_taken_by_enc.csv", index=False)
    xnxx.reset_index(drop=True,inplace=True)
    df.diagnosis_code = df.diagnosis_code.astype(str)
    df = pd.DataFrame(df.groupby('encounter_id')['diagnosis_code'].apply(list)).reset_index(drop=False)
    df.to_csv("Top_ICD_codes_for_encounters.csv",index=False)
    if xnxx.shape == df.shape:
        final = pd.merge(df,xnxx, on='encounter_id',how='outer')
        final.to_csv("enc_icd_labs_segment.csv",index=False)
        print "Final saved."
    else:
        return "Something screwed up. >:("
    return "Code executed properly. :-) "

def get_enc_labs(encounter_id):
    client = MongoClient("mongodb://localhost:27017")
    hng = client.healthnextgen_development
    labs = hng.native_lab_procedures
    labs = pd.DataFrame(list(labs.find({"encounter_id":{"$eq":encounter_id}},{"_id":0, 'lab_procedure_name':1, 'encounter_id':1, 'numeric_result':1})))
    labs.numeric_result = labs.numeric_result.replace('', np.nan)
    labs.dropna(inplace=True)
    labs.numeric_result = labs.numeric_result.astype(float)
    labs = labs.pivot_table(index='encounter_id',columns='lab_procedure_name',values='numeric_result', aggfunc=np.mean)
    labs.fillna(0.0, inplace=True)
    return labs
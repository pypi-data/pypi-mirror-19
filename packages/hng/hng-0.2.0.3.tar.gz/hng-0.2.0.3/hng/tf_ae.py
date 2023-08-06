import tensorflow as tf
import numpy as np
import pandas as pd
import math

df = pd.read_csv("/home/nilesh/labs_data_with_gauss_ml.csv")
labs = np.array(df[df.columns[1:]])
#px.shape #(18128, 1247)
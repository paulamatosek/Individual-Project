import numpy as np
import scipy as sp
import pandas as pd


from sklearn.datasets import load_iris

iriss = load_iris()
df_iris = pd.DataFrame(iriss.data, columns=iriss.feature_names)


print(df_iris)


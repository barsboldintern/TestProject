from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import requests

df = pd.read_csv("structured_data.csv")
print(df.dtypes)
print(df["Шал:"].unique())
print(df["Шал:"].value_counts())
label_encoder = LabelEncoder()
df["Шал:"] = label_encoder.fit_transform(df["Шал:"])

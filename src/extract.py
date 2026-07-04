import pandas as pd

df = pd.read_csv("data/raw/openipf-2026-06-27/openipf-2026-06-27-7197dc8d.csv")

print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())
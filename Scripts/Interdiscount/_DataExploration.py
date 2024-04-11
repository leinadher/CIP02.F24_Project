import pandas as pd

df_interdiscount = pd.read_csv("interdiscount_cleaned.csv")

unique_brands = df_interdiscount['brand'].unique()
for i in unique_brands:
    print(i)
print("-" * 30)

models = []
for index, row in df_interdiscount.iterrows():
    models.append(" ".join([row['brand'], row['model']]))
tuple(models)
print(len(f"There are {models} models"))
print("-" * 30)

unique_colors = df_interdiscount['color'].unique()
for i in unique_colors:
    print(i)
print("-" * 30)

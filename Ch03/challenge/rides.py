# %%
import numpy as np
import pandas as pd

df = pd.read_csv('rides.csv')
df
# %%
# Find out all the rows that have bad values
# - Missing values are not allowed
# - A plate must be a combination of at least 3 upper case letters or digits
# - Distance much be bigger than 0
df[df.isnull().any(axis=1)]
# %%
df['plate'] = df['plate'].str.strip()
df.loc[df['plate'] == '', 'plate'] = np.nan
df[df['plate'].str.match(r'^[0-9A-Z]{3,}', na=False)]

# %%
df
# %%
df.loc[df['name'] == 'Fester', 'plate']
# %%
df[(df['plate'].str.len() >= 3) & (df['distance'] > 0)]
# %%

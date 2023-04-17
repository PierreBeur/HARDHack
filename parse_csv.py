import pandas as pd

# load CSV file with headers into a pandas DataFrame
df = pd.read_csv('wave_non_clutch.csv', header=0, names=['time', 'value'])

# display the DataFrame
print(df)

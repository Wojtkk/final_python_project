import pandas as pd

# Create a DataFrame
data = {'ID': [3, 1, 2],
        'Name': ['Charlie', 'Alice', 'Bob'],
        'Age': [35, 30, 25]}

df = pd.DataFrame(data)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Sort the DataFrame based on the 'ID' column
df_sorted = df.sort_values(by='ID')

# Display the sorted DataFrame
print("\nDataFrame after sorting:")
print(df_sorted)

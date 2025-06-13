import pandas as pd
import numpy as np

def generate_data():
	# Create a DataFrame with 100 rows and 5 columns
	data = pd.DataFrame(np.random.randn(100, 5), columns=list('ABCDE'))
	
	# Introduce some NaN values randomly
	for col in data.columns:
		data.loc[data.sample(frac=0.1).index, col] = np.nan
	
	return data


def main():	
	# Generate the data
	data = generate_data()
	
	# Print the first few rows of the DataFrame
	print("Generated DataFrame:")
	print(data.head())
	
	# Print the shape of the DataFrame
	print("\nShape of DataFrame:", data.shape)
	
	# Print summary statistics
	print("\nSummary Statistics:")
	print(data.describe())
	
	# Print the number of NaN values in each column
	print("\nNumber of NaN values in each column:")
	print(data.isna().sum())

if __name__ == "__main__":
	main()	





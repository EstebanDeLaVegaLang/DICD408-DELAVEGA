import pandas as pd
import numpy as np 

# Extraccion
wine_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"
wine_data = pd.read_csv(wine_url, header = None)

wine_quality_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
wine_quality_data = pd.read_csv(wine_quality_url, sep = ";")

# Initial look of data
print(wine_data.head())
print(wine_quality_data.head())


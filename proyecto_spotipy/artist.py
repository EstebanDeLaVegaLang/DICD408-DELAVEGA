import pandas as pd

# Cargar el archivo CSV
archivo_csv = 'datos_artistas.csv'  # Aquí puedes poner el nombre del archivo CSV que quieras visualizar
df = pd.read_csv(archivo_csv)

# Mostrar las primeras filas del DataFrame
print(df.head())

# Si deseas ver todo el DataFrame
print(df)

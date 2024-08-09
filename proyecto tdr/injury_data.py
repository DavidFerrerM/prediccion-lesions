import pandas as pd

# Cargar el archivo CSV
file_path = 'injury_data.csv'
data = pd.read_csv(file_path)

# Mostrar las primeras filas del archivo para inspeccionar
data.head()

import pandas as pd
from sklearn.preprocessing import StandardScaler

def cargar_datos(ruta_archivo):
    """Carga un archivo CSV de Pokémon desde la ruta especificada."""
    try:
        return pd.read_csv(ruta_archivo)
    except Exception as e:
        print(f"Error cargando los datos: {e}")
        return None

def limpiar_datos(df):
    """Limpia los datos eliminando filas con valores nulos."""
    df = df.dropna()
    return df

def seleccionar_caracteristicas(df, columnas):
    """Selecciona columnas específicas para el análisis."""
    return df[columnas]

def escalar_datos(df):
    """Escala los datos con StandardScaler (media = 0, desviación estándar = 1)."""
    scaler = StandardScaler()
    datos_escalados = scaler.fit_transform(df)
    return datos_escalados
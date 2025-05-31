from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def entrenar_kmeans(datos_escalados, num_clusters):
    modelo = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    etiquetas = modelo.fit_predict(datos_escalados)
    return modelo, etiquetas

def resumen_clusters(datos, etiquetas, columnas):
    datos = datos.copy()
    datos['cluster'] = etiquetas
    resumen = ""
    
    descripciones = {
        0: "Pokémon rápidos y ofensivos",
        1: "Pokémon defensivos y lentos",
        2: "Pokémon balanceados"
    }
    
    for c in sorted(datos['cluster'].unique()):
        descripcion = descripciones.get(c, "Cluster desconocido")
        grupo = datos[datos['cluster'] == c]
        resumen += f"\nCluster {c}: {descripcion}\n"
        for col in columnas:
            promedio = grupo[col].mean()
            resumen += f"  - Promedio {col}: {promedio:.2f}\n"
        resumen += f"  - Tamaño del cluster: {len(grupo)}\n"
    return resumen

def graficar_clusters(datos_originales, etiquetas, columna_x, columna_y, ruta_guardado):
    datos_originales = datos_originales.copy()
    datos_originales['Cluster'] = etiquetas

    nombres_clusters = {
        0: "Pokémon rápidos y ofensivos",
        1: "Pokémon defensivos y lentos",
        2: "Pokémon balanceados"
    }
    datos_originales['cluster_nombre'] = datos_originales['Cluster'].map(nombres_clusters)

    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=datos_originales,
        x=columna_x,
        y=columna_y,
        hue='cluster_nombre',
        palette='tab10',
        alpha=0.8
    )
    plt.title('Filtro de pokemon segun preferencias')
    plt.xlabel(columna_x.capitalize())
    plt.ylabel(columna_y.capitalize())
    plt.legend(title='Tipo de cluster')
    plt.savefig(ruta_guardado)
    plt.close()

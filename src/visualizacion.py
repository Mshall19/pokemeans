import matplotlib.pyplot as plt
import seaborn as sns

def graficar_clusters(df, columnas, etiquetas, ruta="visuals/clusters.png"):
    """
    Dibuja un scatterplot de los clusters según dos columnas.
    """
    col_x, col_y = columnas[1], columnas[2]  # attack y defense por defecto
    df['cluster'] = etiquetas

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=col_x, y=col_y, hue='cluster', palette='Set2', s=60)
    plt.title(f'Clusters de Pokémon por {col_x} y {col_y}')
    plt.xlabel(col_x.capitalize())
    plt.ylabel(col_y.capitalize())
    plt.legend(title='Cluster')
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()

def guardar_resumen_clusters(df, columnas, num_clusters, ruta):
    """
    Guarda estadísticas de cada cluster en un archivo de texto.
    """
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Resumen del análisis de clustering (K-Means, {num_clusters} clusters):\n\n")
        for i in range(num_clusters):
            cluster_df = df[df['cluster'] == i]
            f.write(f"Cluster {i}:\n")
            for col in columnas:
                promedio = cluster_df[col].mean()
                f.write(f"  - Promedio {col}: {promedio:.2f}\n")
            f.write(f"  - Tamaño del cluster: {len(cluster_df)}\n\n") 
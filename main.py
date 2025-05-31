from src.utils import cargar_datos, limpiar_datos, seleccionar_caracteristicas, escalar_datos
from src.modelo import entrenar_kmeans, resumen_clusters, graficar_clusters
from src.analisis import calcular_peluche_score, calcular_combate_score, graficar_pokemon_peluche, graficar_pokemon_utiles
import os
def resumen_scores(df):
    resumen = "\nAnálisis adicional de Scores:\n"
    for score in ['peluche_score', 'combate_score']:
        resumen += f"\n{score}:\n"
        resumen += f"  - Promedio: {df[score].mean():.2f}\n"
        resumen += f"  - Mediana: {df[score].median():.2f}\n"
        resumen += f"  - Máximo: {df[score].max():.2f}\n"
        resumen += f"  - Mínimo: {df[score].min():.2f}\n"
        resumen += f"  - Desviación estándar: {df[score].std():.2f}\n"
    return resumen

def main():
    ruta_archivo = "data/pokemon.csv"
    columnas = ["HP", "Attack", "Defense", "Speed"]
    num_clusters = 3

    # Verificación de existencia del archivo
    if not os.path.exists(ruta_archivo):
        print(f"Error: archivo no encontrado en {ruta_archivo}")
        return

    # Cargar y procesar los datos
    datos = cargar_datos(ruta_archivo)
    if datos is None:
        return

    datos_limpios = limpiar_datos(datos)
    datos_seleccionados = seleccionar_caracteristicas(datos_limpios, columnas)
    datos_escalados = escalar_datos(datos_seleccionados)
    datos_limpios = calcular_peluche_score(datos_limpios)
    datos_limpios = calcular_combate_score(datos_limpios)
    datos_limpios.to_csv('results/pokemon_scores.csv', index=False)

    # Aplicar modelo
    modelo, etiquetas = entrenar_kmeans(datos_escalados, num_clusters)

    # Crear carpetas de resultados si no existen
    os.makedirs("results", exist_ok=True)
    os.makedirs("visuals", exist_ok=True)

    # Guardar resumen en texto
    resumen = resumen_clusters(datos_seleccionados.copy(), etiquetas, columnas)
    with open("results/analysis_summary.txt", "w", encoding="utf-8") as f:
        f.write("Resumen del análisis de clustering con K-Means:\n")
        f.write(f"- Número de grupos: {modelo.n_clusters}\n")
        f.write(f"- Columnas utilizadas: {', '.join(columnas)}\n\n")
        f.write("Observaciones por cluster:\n")
        f.write(resumen)

    # Visualizar clusters — aquí el cambio importante:
    ruta_imagen = "visuals/clusters.png"
    graficar_clusters(datos_seleccionados.copy(), etiquetas, "Attack", "Defense", ruta_imagen)

    # Visualizar gráficos de peluche y utilidad
    graficar_pokemon_peluche(datos_limpios.copy(), 'visuals/peluche_scatter.png')
    graficar_pokemon_utiles(datos_limpios.copy(), 'visuals/utilidad_scatter.png')

    print("Análisis completado.")
    print("Resumen guardado en: results/analysis_summary.txt")
    print("Visualización guardada en: visuals/clusters.png")

if __name__ == "__main__":
    main()

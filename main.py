from src.utils import cargar_datos, limpiar_datos, seleccionar_caracteristicas, escalar_datos
from src.modelo import entrenar_kmeans, resumen_clusters, graficar_clusters
from src.analisis import calcular_peluche_score, calcular_combate_score, graficar_pokemon_peluche, graficar_pokemon_utiles, graficar_mejores_generacion, mejores_generacion, graficar_utiles_vs_peluches, graficar_utiles_vs_peluches_3d

import os

def main():
    ruta_archivo = "data/pokemon.csv"
    columnas = ["HP", "Attack", "Defense", "Speed"]
    num_clusters = 3

    if not os.path.exists(ruta_archivo):
        print(f"Error: archivo no encontrado en {ruta_archivo}")
        return

    datos = cargar_datos(ruta_archivo)
    if datos is None:
        return

    datos_limpios = limpiar_datos(datos)
    datos_seleccionados = seleccionar_caracteristicas(datos_limpios, columnas)
    datos_escalados = escalar_datos(datos_seleccionados)
    datos_limpios = calcular_peluche_score(datos_limpios)
    datos_limpios.to_csv('results/pokemon_scores.csv', index=False)
    datos_limpios = calcular_combate_score(datos_limpios)
    datos_limpios.to_csv('results/pokemon_scores.csv', index=False)
    top_peluches = datos_limpios.sort_values(by=['peluche_score', 'combate_score'], ascending=[False, True]).head(10)
    top_peluches.to_csv('results/top_peluches.csv', index=False)
    top_utiles = datos_limpios.sort_values(by=['combate_score', 'peluche_score'], ascending=[False, True]).head(10)
    top_utiles.to_csv('results/top_utiles.csv', index=False)
    mejores = mejores_generacion(datos_limpios)
    mejores.to_csv('results/mejores_por_generacion.csv', index=False)
    modelo, etiquetas = entrenar_kmeans(datos_escalados, num_clusters)
    

    os.makedirs("results", exist_ok=True)
    os.makedirs("visuals", exist_ok=True)

    resumen = resumen_clusters(datos_seleccionados.copy(), etiquetas, columnas)
    with open("results/analysis_summary.txt", "w", encoding="utf-8") as f:
        f.write("Resumen del análisis de clustering con K-Means:\n")
        f.write(f"- Número de grupos: {modelo.n_clusters}\n")
        f.write(f"- Columnas utilizadas: {', '.join(columnas)}\n\n")
        f.write("Observaciones por cluster:\n")
        f.write(resumen)

    ruta_imagen = "visuals/clusters.png"
    graficar_clusters(datos_seleccionados.copy(), etiquetas, "Attack", "Defense", ruta_imagen)
    graficar_pokemon_peluche(datos_limpios.copy(), 'visuals/peluche_scatter.png')
    graficar_pokemon_utiles(datos_limpios.copy(), 'visuals/utilidad_scatter.png')
    graficar_utiles_vs_peluches(datos_limpios.copy(), 'visuals/utiles_vs_peluches.png')
    graficar_utiles_vs_peluches_3d(datos_limpios.copy(), 'visuals/utiles_vs_peluches_3d.png')
    graficar_mejores_generacion(datos_limpios.copy(), 'visuals/mejores_por_generacion.png')
    

    print("Análisis completado.")
    print("Resumen guardado en: results/analysis_summary.txt")
    print("Visualización guardada en: visuals/clusters.png")

if __name__ == "__main__":
    main()

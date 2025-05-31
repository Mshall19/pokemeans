import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

def calcular_peluche_score(df):
    df = df.copy()
    # Para que los Pokémon con stats bajos (HP, Defensa, Velocidad) obtengan un score alto:
    # Usamos 1/(stat + 1) * 100 para cada stat.
    df['peluche_score'] = (
        (1 / (df['HP'] + 1)) * 100 +
        (1 / (df['Defense'] + 1)) * 100 +
        (1 / (df['Speed'] + 1)) * 100
    )
    return df

def calcular_combate_score(df):
    df = df.copy()
    # Peso más al ataque y velocidad para definir utilidad en combate
    df['combate_score'] = (df['HP']*0.2 + df['Attack']*0.4 + df['Defense']*0.2 + df['Speed']*0.2)
    return df

def mejores_generacion(df):
    # Implementación de la función
    df = df.copy()
    if 'combate_score' not in df.columns:
        df = calcular_combate_score(df)  # calcular si no está

    # Filtrar sin legendarios si quieres
    df = df[~df['Legendary']]

    mejores = df.loc[df.groupby('Generation')['combate_score'].idxmax()]
    return mejores[['Name', 'Generation', 'combate_score']]


import matplotlib.pyplot as plt

def graficar_pokemon_peluche(df, ruta_salida, top_n=10):
    # Ordenamos por peluche_score descendente (los más tiernos, menos letales)
    df_peluches = df.sort_values(by=['peluche_score', 'combate_score'], ascending=[False, True])
    top_peluches = df_peluches.head(top_n)

    # Guardamos imagen PNG
    plt.figure(figsize=(10, 6))
    plt.scatter(df['peluche_score'], df['combate_score'], alpha=0.3, color='gray', label='Todos')
    plt.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], color='hotpink', label='Top Peluches')

    for i, row in top_peluches.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='hotpink')
    
    plt.xlabel('Puntuación Peluche (mayor = más peluche)')
    plt.ylabel('Puntuación Combate (menor = menos útil)')
    plt.title('Pokémon más “peluche”')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    # Mostrar también como ventana emergente
    plt.figure(figsize=(10, 6))
    plt.scatter(df['peluche_score'], df['combate_score'], alpha=0.3, color='gray', label='Todos')
    plt.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], color='hotpink', label='Top Peluches')

    for i, row in top_peluches.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='hotpink')
    
    plt.xlabel('Puntuación Peluche (mayor = más peluche)')
    plt.ylabel('Puntuación Combate (menor = menos útil)')
    plt.title('Pokémon más “peluche”')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_pokemon_utiles(df, ruta_salida, top_n=10):
    # Ordenamos: combate_score alto y peluche_score bajo
    df_utiles = df.sort_values(by=['combate_score', 'peluche_score'], ascending=[False, True])
    top_utiles = df_utiles.head(top_n)

    # Guardar como imagen PNG
    plt.figure(figsize=(10, 6))
    plt.scatter(df['peluche_score'], df['combate_score'], alpha=0.3, color='gray', label='Todos')
    plt.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], color='seagreen', label='Top Útiles')

    for _, row in top_utiles.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='seagreen')
    
    plt.xlabel('Puntuación Peluche (menor = menos peluche)')
    plt.ylabel('Puntuación Combate (mayor = más útil)')
    plt.title('Pokémon más útiles en combate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    # Mostrar también ventana emergente
    plt.figure(figsize=(10, 6))
    plt.scatter(df['peluche_score'], df['combate_score'], alpha=0.3, color='gray', label='Todos')
    plt.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], color='seagreen', label='Top Útiles')

    for _, row in top_utiles.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='seagreen')
    
    plt.xlabel('Puntuación Peluche (menor = menos peluche)')
    plt.ylabel('Puntuación Combate (mayor = más útil)')
    plt.title('Pokémon más útiles en combate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_mejores_generacion(df, ruta_salida):
    # Filtrar legendarios
    df_filtrado = df[~df['Legendary']]
    mejores = df_filtrado.loc[df_filtrado.groupby('Generation')['combate_score'].idxmax()]

    plt.figure(figsize=(10, 6))

    # Graficar todos los Pokémon en gris sin etiquetas
    plt.scatter(df_filtrado['Generation'], df_filtrado['combate_score'], 
                color='lightgray', alpha=0.5, label='Otros Pokémon')

    # Graficar mejores con color y etiquetas
    colores = plt.cm.viridis(mejores['Generation'] / mejores['Generation'].max())
    plt.scatter(mejores['Generation'], mejores['combate_score'], 
                color=colores, label='Mejor por generación', s=100)

    for i, row in mejores.iterrows():
        plt.text(row['Generation'], row['combate_score'], row['Name'], 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("Mejor Pokémon por generación (sin legendarios)")
    plt.xlabel("Generación")
    plt.ylabel("Puntuación de combate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    # Mostrar ventana emergente con la misma gráfica
    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtrado['Generation'], df_filtrado['combate_score'], 
                color='lightgray', alpha=0.5, label='Otros Pokémon')
    plt.scatter(mejores['Generation'], mejores['combate_score'], 
                color=colores, label='Mejor por generación', s=100)

    for i, row in mejores.iterrows():
        plt.text(row['Generation'], row['combate_score'], row['Name'], 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("Mejor Pokémon por generación (sin legendarios)")
    plt.xlabel("Generación")
    plt.ylabel("Puntuación de combate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_utiles_vs_peluches(df, ruta_salida, top_n=10):
    df = df.copy()
    # Ordenar para obtener top peluches y top útiles
    top_peluches = df.sort_values(by='peluche_score', ascending=False).head(top_n)
    top_utiles = df.sort_values(by='combate_score', ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    # Dibujar todos en gris claro, sin etiquetas
    plt.scatter(df['peluche_score'], df['combate_score'], color='lightgray', alpha=0.4, label='Todos')

    # Top peluches en color rosa
    plt.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], color='hotpink', label=f'Top {top_n} Peluches', s=100)
    for _, row in top_peluches.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='hotpink', fontweight='bold')

    # Top útiles en color verde
    plt.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], color='seagreen', label=f'Top {top_n} Útiles', s=100)
    for _, row in top_utiles.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='seagreen', fontweight='bold')

    plt.xlabel('Puntuación Peluche (mayor = más peluche)')
    plt.ylabel('Puntuación Combate (mayor = más útil)')
    plt.title(f'Top {top_n} Pokémon más útiles vs más peluches')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    # Mostrar ventana emergente igual
    plt.figure(figsize=(10, 6))
    plt.scatter(df['peluche_score'], df['combate_score'], color='lightgray', alpha=0.4, label='Todos')
    plt.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], color='hotpink', label=f'Top {top_n} Peluches', s=100)
    for _, row in top_peluches.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='hotpink', fontweight='bold')
    plt.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], color='seagreen', label=f'Top {top_n} Útiles', s=100)
    for _, row in top_utiles.iterrows():
        plt.text(row['peluche_score'], row['combate_score'], row['Name'], fontsize=8, color='seagreen', fontweight='bold')

    plt.xlabel('Puntuación Peluche (mayor = más peluche)')
    plt.ylabel('Puntuación Combate (mayor = más útil)')
    plt.title(f'Top {top_n} Pokémon más útiles vs más peluches')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_utiles_vs_peluches_3d(df, ruta_salida, top_n=10):
    df = df.copy()

    # Top peluches y top útiles
    top_peluches = df.sort_values(by='peluche_score', ascending=False).head(top_n)
    top_utiles = df.sort_values(by='combate_score', ascending=False).head(top_n)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Todos en gris oscuro (#665c5d), sin nombres, puntos más grandes
    ax.scatter(df['peluche_score'], df['combate_score'], df['Speed'],
               color='#665c5d', s=80, alpha=0.8, label='Resto de Pokémon')

    # Top peluches en naranja, puntos más grandes
    ax.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], top_peluches['Speed'],
               color='orange', s=110, label=f'Top {top_n} Peluches')

    # Top útiles en rojo (#e51a4c), puntos más grandes
    ax.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], top_utiles['Speed'],
               color='#e51a4c', s=110, label=f'Top {top_n} Útiles')

    # Etiquetas para top peluches
    for _, row in top_peluches.iterrows():
        ax.text(row['peluche_score'], row['combate_score'], row['Speed'],
                row['Name'], color='orange', fontsize=9)

    # Etiquetas para top útiles
    for _, row in top_utiles.iterrows():
        ax.text(row['peluche_score'], row['combate_score'], row['Speed'],
                row['Name'], color='#e51a4c', fontsize=9)

    ax.set_xlabel('Puntuación Peluche')
    ax.set_ylabel('Puntuación Combate')
    ax.set_zlabel('Velocidad (Speed)')
    ax.set_title(f'Top {top_n} Pokémon más útiles vs más peluches (3D)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.show()
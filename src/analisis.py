import matplotlib.pyplot as plt

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
    df = df[~df['Legendary']]
    mejores = df.loc[df.groupby('Generation')['combate_score'].idxmax()]

    plt.figure(figsize=(10, 6))
    
    # Scatter plot: Generación vs Combate Score
    plt.scatter(mejores['Generation'], mejores['combate_score'], c=mejores['Generation'], cmap='viridis', s=100, edgecolors='black')

    # Agregar etiquetas con el nombre del Pokémon sobre cada punto
    for _, row in mejores.iterrows():
        plt.text(row['Generation'], row['combate_score'] + 0.5, row['Name'], ha='center', fontsize=9)

    plt.xlabel("Generación")
    plt.ylabel("Puntuación de Combate")
    plt.title("Mejor Pokémon por generación (sin legendarios)")
    plt.grid(True)
    plt.xticks(mejores['Generation'].unique())  # Para que se muestren solo generaciones existentes
    plt.tight_layout()
    
    plt.savefig(ruta_salida)
    plt.show()
    plt.close()

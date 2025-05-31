import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def calcular_peluche_score(df):
    df = df.copy()
    df['peluche_score'] = (
        (1 / (df['HP'] + 1)) * 100 +
        (1 / (df['Defense'] + 1)) * 100 +
        (1 / (df['Speed'] + 1)) * 100
    )
    return df

def calcular_combate_score(df):
    df = df.copy()
    df['combate_score'] = (df['HP']*0.2 + df['Attack']*0.4 + df['Defense']*0.2 + df['Speed']*0.2)
    return df

def mejores_generacion(df):
    df = df.copy()
    if 'combate_score' not in df.columns:
        df = calcular_combate_score(df)
    df = df[~df['Legendary']]
    mejores = df.loc[df.groupby('Generation')['combate_score'].idxmax()]
    return mejores[['Name', 'Generation', 'combate_score']]

def mejores_generacion_normales(df):
    mejores = []
    for gen in sorted(df['Generation'].unique()):
        sub = df[(df['Generation'] == gen) &
                 (~df['Legendary']) &
                 (~df['Name'].str.contains('Mega|X|Y|Alola|Galar|Hisui|Gigantamax', case=False))]

        if not sub.empty:
            mejor = sub.loc[sub['combate_score'].idxmax()]
            mejores.append(mejor)

    return pd.DataFrame(mejores)

def graficar_pokemon_peluche(df, ruta_salida, top_n=10):
    df_peluches = df.sort_values(by=['peluche_score', 'combate_score'], ascending=[False, True])
    top_peluches = df_peluches.head(top_n)

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
    df_utiles = df.sort_values(by=['combate_score', 'peluche_score'], ascending=[False, True])
    top_utiles = df_utiles.head(top_n)

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
    df_filtrado = df[~df['Legendary']]
    mejores = df_filtrado.loc[df_filtrado.groupby('Generation')['combate_score'].idxmax()]
    mejores_normales = mejores_generacion_normales(df)

    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtrado['Generation'], df_filtrado['combate_score'],
                color='lightgray', alpha=0.5, label='Otros Pokémon')

    colores_absolutos = plt.cm.viridis(mejores['Generation'] / mejores['Generation'].max())
    colores_normales = plt.cm.plasma(mejores_normales['Generation'] / mejores_normales['Generation'].max())

    plt.scatter(mejores['Generation'], mejores['combate_score'],
                color=colores_absolutos, label='Mejor por generación', s=100)
    for _, row in mejores.iterrows():
        plt.text(row['Generation'], row['combate_score'] + 2, row['Name'],
                 ha='center', fontsize=8, color='black', fontweight='bold')

    plt.scatter(mejores_normales['Generation'], mejores_normales['combate_score'],
                color=colores_normales, marker='s', label='Mejor normal', s=80)
    for _, row in mejores_normales.iterrows():
        plt.text(row['Generation'], row['combate_score'] - 5, row['Name'],
                 ha='center', fontsize=8, color='blue')

    plt.title("Mejor Pokémon por generación")
    plt.xlabel("Generación")
    plt.ylabel("Puntuación de combate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtrado['Generation'], df_filtrado['combate_score'],
                color='lightgray', alpha=0.5, label='Otros Pokémon')

    plt.scatter(mejores['Generation'], mejores['combate_score'],
                color=colores_absolutos, label='Mejor por generación', s=100)
    for _, row in mejores.iterrows():
        plt.text(row['Generation'], row['combate_score'] + 2, row['Name'],
                 ha='center', fontsize=8, color='black', fontweight='bold')

    plt.scatter(mejores_normales['Generation'], mejores_normales['combate_score'],
                color=colores_normales, marker='s', label='Mejor normal', s=80)
    for _, row in mejores_normales.iterrows():
        plt.text(row['Generation'], row['combate_score'] - 5, row['Name'],
                 ha='center', fontsize=8, color='blue')

    plt.title("Mejor Pokémon por generación")
    plt.xlabel("Generación")
    plt.ylabel("Puntuación de combate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def graficar_utiles_vs_peluches(df, ruta_salida, top_n=10):
    df = df.copy()
    top_peluches = df.sort_values(by='peluche_score', ascending=False).head(top_n)
    top_utiles = df.sort_values(by='combate_score', ascending=False).head(top_n)

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
    plt.savefig(ruta_salida)
    plt.close()

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
    top_peluches = df.sort_values(by='peluche_score', ascending=False).head(top_n)
    top_utiles = df.sort_values(by='combate_score', ascending=False).head(top_n)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(df['peluche_score'], df['combate_score'], df['Speed'],
               color='#665c5d', s=80, alpha=0.8, label='Resto de Pokémon')

    ax.scatter(top_peluches['peluche_score'], top_peluches['combate_score'], top_peluches['Speed'],
               color='orange', s=110, label=f'Top {top_n} Peluches')

    ax.scatter(top_utiles['peluche_score'], top_utiles['combate_score'], top_utiles['Speed'],
               color='#e51a4c', s=110, label=f'Top {top_n} Útiles')

    for _, row in top_peluches.iterrows():
        ax.text(row['peluche_score'], row['combate_score'], row['Speed'],
                row['Name'], color='orange', fontsize=9)

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

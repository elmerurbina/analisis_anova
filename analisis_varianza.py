import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


# Ruta del archivo
file_path = r"D:\Copy of Estudio_sobre_la_eficiencia_de_diferentes_dietas_en_la_reducción_de_colesterol(1).xlsx"

# Cargar los datos desde el archivo Excel
df = pd.read_excel(file_path)

# Limpiar los nombres de las columnas eliminando espacios, saltos de línea y tabulaciones
df.columns = df.columns.str.replace(r'\n', ' ', regex=True)  # Reemplazar saltos de línea por espacios
df.columns = df.columns.str.replace(r'\t', '', regex=True)  # Eliminar tabulaciones
df.columns = df.columns.str.strip()  # Eliminar espacios extra al inicio y final de los nombres

# Imprimir las primeras filas del dataframe para verificar que se cargaron correctamente
print("Primeras filas del dataframe:")
print(df.head())

# Verificar las columnas disponibles en el dataframe
print("\nColumnas disponibles:")
print(df.columns)

# Definir las columnas específicas que necesitamos para el análisis
columna_colesterol = 'Si realizaste un análisis reciente de colesterol, indica el valor total (en mg/dL):'
columna_dieta = '¿Cuál de las siguientes dietas has seguido en los últimos 3 meses?'

# Verificar si las columnas que necesitamos existen en el DataFrame
if columna_colesterol in df.columns and columna_dieta in df.columns:
    # Limpiar los datos eliminando filas con valores nulos o NaN en las columnas relevantes
    df_cleaned = df.dropna(subset=[columna_colesterol, columna_dieta])

    # Limpiar y convertir los valores de colesterol a numéricos (eliminar caracteres no numéricos)
    df_cleaned[columna_colesterol] = pd.to_numeric(df_cleaned[columna_colesterol], errors='coerce')

    # Eliminar filas con valores NaN (incompatibles con el análisis)
    df_cleaned = df_cleaned.dropna(subset=[columna_colesterol])

    # Agrupar los datos por el tipo de dieta y obtener los valores de colesterol
    groups = df_cleaned.groupby(columna_dieta)[columna_colesterol].apply(list)

    # Realizar el análisis de varianza (ANOVA)
    anova_result = stats.f_oneway(*groups)

    # Estadístico F y valor p
    f_stat = anova_result.statistic
    p_value = anova_result.pvalue

    # Grados de libertad
    df_between = len(groups) - 1  # Grados de libertad entre grupos (k-1)
    df_within = len(df_cleaned) - len(groups)  # Grados de libertad dentro de los grupos (N-k)

    # Nivel de significancia
    alpha = 0.05

    # Calcular el valor F crítico
    f_critical = stats.f.ppf(1 - alpha, df_between, df_within)

    # Mostrar resultados
    print(f"\nEstadístico F: {f_stat}")
    print(f"Valor p: {p_value}")
    print(f"Grados de libertad entre grupos (df_between): {df_between}")
    print(f"Grados de libertad dentro de los grupos (df_within): {df_within}")
    print(f"F crítico (valor de referencia): {f_critical}")

    # Interpretación basada en F y F crítico
    if f_stat > f_critical:
        print("\nSe rechaza la hipótesis nula: Existen diferencias significativas entre las dietas.")
    else:
        print("\nNo rechazamos la hipótesis nula: No hay diferencias significativas entre las dietas.")

    # Mejorar el gráfico
    plt.figure(figsize=(12, 8))

    # Usar un color distintivo para cada dieta
    sns.set_palette("Set2")  # Paleta de colores más clara

    # Crear un gráfico de cajas
    ax = sns.boxplot(x=columna_dieta, y=columna_colesterol, data=df_cleaned, palette='Set2')

    # Agregar el título y etiquetas
    plt.title('Distribución de los Niveles de Colesterol por Dieta', fontsize=16)
    plt.xlabel('Dieta', fontsize=14)
    plt.ylabel('Niveles de Colesterol (mg/dL)', fontsize=14)

    # Mejorar la legibilidad de las etiquetas del eje X
    plt.xticks(rotation=45, ha='right', fontsize=12)

    # Mostrar los valores dentro de las cajas para mayor claridad
    for i in range(len(groups)):
        group = groups.iloc[i]
        y = group
        x = i
        for value in y:
            ax.text(x, value, f'{value:.2f}', color='black', ha='center', va='center')

    # Ajustar el tamaño de la figura para que no se solapen los elementos
    plt.tight_layout()

    # Guardar el gráfico si es necesario
    plt.savefig("boxplot_colesterol_dieta.png")

    # Mostrar el gráfico
    plt.show()

else:
    print(
        "\nUna o ambas de las columnas necesarias no están presentes en el DataFrame. Por favor, verifica los nombres de las columnas.")

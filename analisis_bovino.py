import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.libqsturng import psturng

# Datos del dataset
data = {
    'Costo_Alimentacion': ['20000', '10000', '10000', 'Depende', '2000', '2000', '5000', '4000', 'NA', '20000'],
    'Costo_Mano_Obra': ['25000', '18000', '7500', 'Depende', '5000', '3500', '1000', '5000', 'NA', '20000'],
    'Costo_Salud': ['7000', '3000', '3400', 'Depende', '1000', '2500', '1000', '2000', 'NA', '10000'],
    'Costo_Otros': ['NA', '2000', '4000', '1000', '1000', '0', '500', '0', 'NA', '2000']
}

# Crear DataFrame
df = pd.DataFrame(data)

# Convertir columnas a numéricas
cols_to_convert = ['Costo_Alimentacion', 'Costo_Mano_Obra', 'Costo_Salud', 'Costo_Otros']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Rellenar NaN con 0
df[cols_to_convert] = df[cols_to_convert].fillna(0)

# Calcular el costo total
df['Costo_Total_Alimentacion'] = (
    df['Costo_Alimentacion'] +
    df['Costo_Mano_Obra'] +
    df['Costo_Salud'] +
    df['Costo_Otros']
)

# Análisis para cada hipótesis
analisis = {}

# Hipótesis 1: Proporción de costos de alimentación
analisis['Proporcion_Alimentacion'] = (df['Costo_Alimentacion'] / df['Costo_Total_Alimentacion']).mean()

# Hipótesis 2: Influencia de la mano de obra
analisis['Proporcion_Mano_Obra'] = (df['Costo_Mano_Obra'] / df['Costo_Total_Alimentacion']).mean()

# Hipótesis 3: Consistencia de los costos de salud (Desviación estándar)
analisis['Consistencia_Salud'] = df['Costo_Salud'].std()

# Hipótesis 4: Importancia de los costos adicionales
analisis['Proporcion_Costos_Otros'] = (df['Costo_Otros'] / df['Costo_Total_Alimentacion']).mean()

# Hipótesis 5: Agrupamiento por niveles de costos
bins = [0, 10000, 20000, np.inf]  # Definir rangos
labels = ['Bajo', 'Medio', 'Alto']
df['Nivel_Costos'] = pd.cut(df['Costo_Total_Alimentacion'], bins=bins, labels=labels)

# Resultados
print("Análisis Hipótesis:")
print(pd.DataFrame([analisis]))

# Mostrar DataFrame con niveles de costos
print("\nDataset con niveles de costos:")
print(df)

import scipy.stats as stats

# Hipótesis 1: Proporción de costos de alimentación
grupo_alimentacion = df['Costo_Alimentacion']
grupo_total = df['Costo_Total_Alimentacion']

# ANOVA para la Hipótesis 1: Proporción de costos de alimentación
F1, p1 = stats.f_oneway(grupo_alimentacion, grupo_total)
F_critico1 = stats.f.ppf(0.95, len(grupo_alimentacion)-1, len(grupo_total)-1)

# Hipótesis 2: Influencia de la mano de obra
grupo_mano_obra = df['Costo_Mano_Obra']

# ANOVA para la Hipótesis 2: Influencia de la mano de obra
F2, p2 = stats.f_oneway(grupo_mano_obra, grupo_total)
F_critico2 = stats.f.ppf(0.95, len(grupo_mano_obra)-1, len(grupo_total)-1)

# Hipótesis 3: Consistencia de los costos de salud
grupo_salud = df['Costo_Salud']

# ANOVA para la Hipótesis 3: Consistencia de los costos de salud
F3, p3 = stats.f_oneway(grupo_salud, grupo_total)
F_critico3 = stats.f.ppf(0.95, len(grupo_salud)-1, len(grupo_total)-1)

# Hipótesis 4: Importancia de los costos adicionales
grupo_otros = df['Costo_Otros']

# ANOVA para la Hipótesis 4: Importancia de los costos adicionales
F4, p4 = stats.f_oneway(grupo_otros, grupo_total)
F_critico4 = stats.f.ppf(0.95, len(grupo_otros)-1, len(grupo_total)-1)

# Hipótesis 5: Agrupamiento por niveles de costos
# Agrupar por "Nivel_Costos"
nivel_costos = df['Nivel_Costos'].map({'Bajo': 1, 'Medio': 2, 'Alto': 3})  # Convertir a números para el test ANOVA
grupo_nivel = nivel_costos

# ANOVA para la Hipótesis 5: Agrupamiento por niveles de costos
F5, p5 = stats.f_oneway(grupo_nivel, grupo_total)
F_critico5 = stats.f.ppf(0.95, len(grupo_nivel)-1, len(grupo_total)-1)

# Mostrar los resultados
print("\nResultados ANOVA para las Hipótesis:")
print(f"Hipótesis 1: F = {F1:.2f}, F crítico = {F_critico1:.2f}, p-valor = {p1:.5f}")
print("Decisión: " + ("Rechazamos H0" if p1 < 0.05 else "Aceptamos H0"))

print(f"Hipótesis 2: F = {F2:.2f}, F crítico = {F_critico2:.2f}, p-valor = {p2:.5f}")
print("Decisión: " + ("Rechazamos H0" if p2 < 0.05 else "Aceptamos H0"))

print(f"Hipótesis 3: F = {F3:.2f}, F crítico = {F_critico3:.2f}, p-valor = {p3:.5f}")
print("Decisión: " + ("Rechazamos H0" if p3 < 0.05 else "Aceptamos H0"))

print(f"Hipótesis 4: F = {F4:.2f}, F crítico = {F_critico4:.2f}, p-valor = {p4:.5f}")
print("Decisión: " + ("Rechazamos H0" if p4 < 0.05 else "Aceptamos H0"))

print(f"Hipótesis 5: F = {F5:.2f}, F crítico = {F_critico5:.2f}, p-valor = {p5:.5f}")
print("Decisión: " + ("Rechazamos H0" if p5 < 0.05 else "Aceptamos H0"))

print("\nAplicando la prueba de Duncan (Post-Hoc) para la Hipótesis 1")

# Función para realizar la prueba de Duncan
def prueba_duncan(df, dependiente, factor):
    """
    Realiza la prueba de Duncan para comparar medias de grupos en un análisis post-hoc
    """
    # Agrupar por factor y calcular la media y desviación estándar de cada grupo
    grupos = df.groupby(factor).agg({dependiente: ['mean', 'std', 'count']})

    # Obtener las medias y el número de muestras de cada grupo
    medias = grupos['Costo_Alimentacion']['mean']
    n = grupos['Costo_Alimentacion']['count']

    # Calcular el rango crítico de Duncan (para un nivel de significancia de 0.05)
    duncan_critico = psturng(0.05, len(medias), len(medias) - 1)

    # Calcular el valor de q de Duncan (comparación de medias)
    q_values = []

    for i in range(len(medias)):
        for j in range(i+1, len(medias)):
            q = abs(medias[i] - medias[j]) / np.sqrt((grupos['Costo_Alimentacion']['std'][i]**2 / n[i]) +
                                                      (grupos['Costo_Alimentacion']['std'][j]**2 / n[j]))
            q_values.append((i, j, q))

    # Mostrar los resultados de la prueba de Duncan
    print("Comparaciones de Duncan (q valores):")
    for comparacion in q_values:
        print(f"Comparando grupo {comparacion[0]} con grupo {comparacion[1]}: q = {comparacion[2]}")
        if comparacion[2] > duncan_critico:
            print("Diferencia significativa")
        else:
            print("No hay diferencia significativa")

# Llamar a la función para realizar la prueba de Duncan
prueba_duncan(df, 'Costo_Alimentacion', 'Nivel_Costos')

# Configuración para gráficos más estéticos
sns.set(style="whitegrid")

# Interpretación y Gráficas

# Hipótesis 1: Proporción de costos de alimentación
print(f"Hipótesis 1: Los costos de alimentación representan, en promedio, el {analisis['Proporcion_Alimentacion']:.2%} del costo total.")
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x=df.index, y="Costo_Alimentacion", color="skyblue", label="Costo Alimentación")
plt.plot(df.index, df['Costo_Total_Alimentacion'], color="red", label="Costo Total", linewidth=2)
plt.title("Hipótesis 1: Relación Costo Alimentación y Total")
plt.xlabel("Índice")
plt.ylabel("Costo")
plt.legend()
plt.show()


# Hipótesis 2: Proporción de costos de mano de obra
print(f"Hipótesis 2: La mano de obra representa, en promedio, el {analisis['Proporcion_Mano_Obra']:.2%} del costo total.")
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x=df.index, y="Costo_Mano_Obra", color="orange", label="Costo Mano de Obra")
plt.plot(df.index, df['Costo_Total_Alimentacion'], color="red", label="Costo Total", linewidth=2)
plt.title("Hipótesis 2: Relación Costo Mano de Obra y Total")
plt.xlabel("Índice")
plt.ylabel("Costo")
plt.legend()
plt.show()

# Hipótesis 3: Consistencia en costos de salud
print(f"Hipótesis 3: La desviación estándar de los costos de salud es {analisis['Consistencia_Salud']:.2f}, indicando su variabilidad.")
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, y="Costo_Salud", color="green")
plt.title("Hipótesis 3: Variabilidad en Costos de Salud")
plt.ylabel("Costo Salud")
plt.show()

# Hipótesis 4: Proporción de costos adicionales
print(f"Hipótesis 4: Los costos adicionales representan, en promedio, el {analisis['Proporcion_Costos_Otros']:.2%} del costo total.")
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x=df.index, y="Costo_Otros", color="purple", label="Costo Otros")
plt.plot(df.index, df['Costo_Total_Alimentacion'], color="red", label="Costo Total", linewidth=2)
plt.title("Hipótesis 4: Relación Costos Adicionales y Total")
plt.xlabel("Índice")
plt.ylabel("Costo")
plt.legend()
plt.show()

# Hipótesis 5: Agrupamiento por niveles de costos
print("Hipótesis 5: Distribución de costos totales en niveles (Bajo, Medio, Alto).")
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Nivel_Costos", palette="pastel")
plt.title("Hipótesis 5: Niveles de Costos Totales")
plt.xlabel("Nivel de Costos")
plt.ylabel("Cantidad")
plt.show()
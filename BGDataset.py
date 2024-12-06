import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
import matplotlib.pyplot as plt

# Leer los datos
archivo_csv = "https://drive.google.com/uc?id=1KH62XtloMmxz9K3r2i4GFjlhGACnaiyR"
data = pd.read_csv(archivo_csv)


# Filtrar las variables que necesitamos: 'Elapsed days' como X y '# Shares' como Y
X = data['Elapsed days'].values.reshape(-1, 1)  # La variable independiente
Y = data['# Shares'].values  # La variable dependiente

# 1. Ajuste del modelo de regresión lineal
model = LinearRegression()
model.fit(X, Y)

# Coeficientes de la regresión
intercept = model.intercept_
slope = model.coef_[0]

# Predicciones del modelo
Y_pred = model.predict(X)

# Imprimir los coeficientes
print(f"Intercepto (a): {intercept}")
print(f"Pendiente (b): {slope}")

# Visualizar la regresión
plt.scatter(X, Y, color='blue', label='Datos reales')
plt.plot(X, Y_pred, color='red', label='Modelo de regresión')
plt.xlabel('Días transcurridos')
plt.ylabel('Número de Shares')
plt.title('Regresión Lineal: Días transcurridos vs. Número de Shares')
plt.legend()
plt.show()

# 2. Prueba de Breusch-Godfrey para autocorrelación en los residuos
# Obtener los residuos de la regresión
residuals = Y - Y_pred

# Ajustar el modelo con una constante (para la prueba de autocorrelación)
X_with_const = sm.add_constant(X)  # Agregar el término constante
model_sm = sm.OLS(Y, X_with_const).fit()

# Realizar la prueba de Breusch-Godfrey
bg_test = acorr_breusch_godfrey(model_sm, nlags=1)

# Estadístico LM y p-valor de la prueba
lm_stat = bg_test[0]
p_value = bg_test[1]

# Imprimir los resultados de la prueba
print(f"\nPrueba de Breusch-Godfrey:")
print(f"Estadístico LM: {lm_stat}")
print(f"p-valor: {p_value}")

# 3. Interpretación de los resultados
if p_value < 0.05:
    print("\nHay evidencia significativa de autocorrelación en los residuos (rechazamos la hipótesis nula).")
else:
    print("\nNo hay evidencia significativa de autocorrelación en los residuos (no rechazamos la hipótesis nula).")

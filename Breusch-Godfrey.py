import tkinter as tk
from tkinter import messagebox
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2

def calcular_regresion_y_prueba():
    try:
        # Obtener los valores de X e Y desde las entradas de texto
        x_values = list(map(float, x_entry.get().split(',')))
        y_values = list(map(float, y_entry.get().split(',')))

        # Comprobar que la cantidad de datos sea la misma
        if len(x_values) != len(y_values):
            messagebox.showerror("Error", "X e Y deben tener la misma cantidad de valores.")
            return

        # Convertir a arreglos de numpy
        X = np.array(x_values)
        Y = np.array(y_values)

        # 1. Ajustar el modelo de regresión lineal
        X_with_const = sm.add_constant(X)  # Agregar el término constante (intercepto)
        model = sm.OLS(Y, X_with_const).fit()  # Ajustar el modelo

        # Obtener los coeficientes de la regresión
        a = model.params[0]  # Intercepto
        b = model.params[1]  # Pendiente
        r_squared = model.rsquared  # R² del modelo

        # 2. Obtener los residuos y rezagos
        # Residuos del modelo ajustado
        residuals = model.resid
        # Rezagos de los residuos (todos menos el último)
        lag_residuals = residuals[:-1]
        # Los residuos desplazados en una posición
        residuals_lagged = residuals[1:]

        # 3. Ajustar el modelo auxiliar
        # Agregar el término constante (intercepto) para la regresión auxiliar
        X_aux = sm.add_constant(lag_residuals)
        # Ajustar el modelo auxiliar
        model_aux = sm.OLS(residuals_lagged, X_aux).fit()

        # Obtener los coeficientes de la regresión auxiliar
        # Intercepto del modelo auxiliar
        a_aux = model_aux.params[0]
        # Pendiente del modelo auxiliar
        b_aux = model_aux.params[1]
        # R² del modelo auxiliar
        r_squared_aux = model_aux.rsquared

        # 4. Prueba de Breusch-Godfrey para autocorrelación de primer orden
        bg_test = sm.stats.diagnostic.acorr_breusch_godfrey(model, nlags=1)

        # Estadístico LM y p-valor de la prueba de Breusch-Godfrey
        lm_stat = bg_test[0]
        p_value = bg_test[1]

        # Crear el texto de resultados
        resultados_texto = (
            f"**Ecuación Ajustada**:\n"
            f"Y = {a:.4f} + {b:.4f}X\n\n"
            f"**Coeficientes del Modelo Auxiliar**:\n"
            f"a (intercepto): {a_aux:.4f}\n"
            f"b (pendiente): {b_aux:.4f}\n"
            f"R² del modelo auxiliar: {r_squared_aux:.4f}\n\n"
            f"**Prueba de Breusch-Godfrey**:\n"
            f"Estadístico LM: {lm_stat:.4f}\n"
            f"p-valor: {p_value:.4f}\n\n"
            f"**Interpretación**:\n"
        )

        # Interpretación de los resultados
        if p_value < 0.05:
            interpretacion = "Hay evidencia significativa de autocorrelación de primer orden en los residuos."
        else:
            interpretacion = "No hay evidencia significativa de autocorrelación de primer orden en los residuos."

        # Añadir interpretación a los resultados
        resultados_texto += interpretacion

        # Mostrar los resultados en una ventana de mensaje
        messagebox.showinfo("Resultados", resultados_texto)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para X e Y.")


# Crear la ventana principal
root = tk.Tk()
root.title("Análisis de Regresión Lineal y Prueba de Breusch-Godfrey")

# Etiquetas y cuadros de texto para X e Y
tk.Label(root, text="Valores de X (Temperatura, separados por comas):").pack(pady=5)
x_entry = tk.Entry(root, width=50)
x_entry.pack()

tk.Label(root, text="Valores de Y (Consumo de energía, separados por comas):").pack(pady=5)
y_entry = tk.Entry(root, width=50)
y_entry.pack()

# Botón para realizar el análisis
calculate_button = tk.Button(root, text="Realizar Análisis", command=calcular_regresion_y_prueba)
calculate_button.pack(pady=20)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()

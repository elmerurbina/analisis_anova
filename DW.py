import tkinter as tk
from tkinter import messagebox
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson


# Función para calcular Durbin-Watson
def calcular_dw():
    try:
        # Obtener los valores de X y Y desde las entradas de texto
        X_values = entry_x.get().split(',')
        Y_values = entry_y.get().split(',')

        # Convertir los valores de X y Y a arrays de números
        X = np.array([float(x.strip()) for x in X_values])
        Y = np.array([float(y.strip()) for y in Y_values])

        if len(X) != len(Y):
            messagebox.showerror("Error", "Las listas de X y Y deben tener el mismo tamaño.")
            return

        # Ajustar el modelo de regresión lineal
        # Añadir constante (intercepto)
        X_ajustado = sm.add_constant(X)
        # Modelo de regresión lineal
        model = sm.OLS(Y, X_ajustado).fit()

        # Calcular Durbin-Watson utilizando la función de statsmodels
        dw_statistic = durbin_watson(model.resid)

        # Mostrar el resultado
        label_resultado.config(text=f"Estadístico Durbin-Watson: {dw_statistic:.4f}")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa solo números válidos.")


# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Calculadora Durbin-Watson")

# Crear las etiquetas y campos de entrada para X y Y
label_x = tk.Label(ventana, text="Introduce los valores de X (separados por comas):")
label_x.pack()

entry_x = tk.Entry(ventana, width=40)
entry_x.pack()

label_y = tk.Label(ventana, text="Introduce los valores de Y (separados por comas):")
label_y.pack()

entry_y = tk.Entry(ventana, width=40)
entry_y.pack()

# Crear el botón para calcular Durbin-Watson
boton_calcular = tk.Button(ventana, text="Calcular Durbin-Watson", command=calcular_dw)
boton_calcular.pack(pady=10)

# Crear una etiqueta para mostrar el resultado
label_resultado = tk.Label(ventana, text="Estadístico Durbin-Watson: ")
label_resultado.pack()

# Ejecutar la interfaz
ventana.mainloop()

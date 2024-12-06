import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import tkinter as tk
from tkinter import messagebox


# Función para ajustar el modelo y generar el gráfico
def ajustar_regresion():
    try:
        # Obtener los valores de X y Y desde las entradas
        X_values = list(map(float, entry_X.get().split(',')))
        Y_values = list(map(float, entry_Y.get().split(',')))

        # Comprobar que ambos arreglos tengan la misma longitud
        if len(X_values) != len(Y_values):
            messagebox.showerror("Error", "Los valores de X y Y deben tener la misma longitud.")
            return

        # Añadir una constante a X para el intercepto
        X_ = sm.add_constant(X_values)

        # Ajustar el modelo de regresión lineal
        model = sm.OLS(Y_values, X_)
        results = model.fit()

        # Obtener los residuos
        residuos = results.resid

        # Graficar los residuos vs. horas de estudio
        plt.figure(figsize=(8, 6))
        plt.scatter(X_values, residuos, color='blue', label='Residuos')
        plt.axhline(y=0, color='red', linestyle='--', label='Línea cero')
        plt.title('Gráfico de Residuos vs. Horas de Estudio')
        plt.xlabel('Horas de Estudio')
        plt.ylabel('Residuos')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Interpretación del patrón de residuos
        interpretacion = interpretar_patron(residuos)
        messagebox.showinfo("Interpretación", interpretacion)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa los valores de X y Y correctamente.")


# Función para interpretar el patrón de residuos
def interpretar_patron(residuos):
    # Analizamos si los residuos muestran un patrón sistemático
    # Si hay una tendencia clara, es probable que haya una relación no capturada por el modelo.

    if np.all(np.diff(residuos) > 0) or np.all(np.diff(residuos) < 0):
        return "Los residuos muestran una tendencia (positiva o negativa), lo que sugiere que el modelo podría no ser adecuado."
    elif np.var(residuos) < np.var(residuos[0:len(residuos) // 2]) or np.var(residuos) < np.var(
            residuos[len(residuos) // 2:]):
        return "Los residuos parecen estar agrupados en una zona. Esto sugiere que podrían existir problemas de heterocedasticidad."
    else:
        return "Los residuos no muestran un patrón evidente, lo que sugiere que el modelo podría ser adecuado."


# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Análisis de Regresión Lineal")

# Etiquetas y campos de entrada para los valores de X y Y
label_X = tk.Label(root, text="Ingresa las horas de estudio (X), separadas por coma:")
label_X.pack()

entry_X = tk.Entry(root, width=50)
entry_X.pack()

label_Y = tk.Label(root, text="Ingresa los puntajes obtenidos (Y), separados por coma:")
label_Y.pack()

entry_Y = tk.Entry(root, width=50)
entry_Y.pack()

# Botón para ajustar la regresión y generar la gráfica
btn_ajustar = tk.Button(root, text="Ajustar Regresión y Mostrar Gráfica", command=ajustar_regresion)
btn_ajustar.pack()

# Ejecutar la interfaz de Tkinter
root.mainloop()

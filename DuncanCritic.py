import numpy as np

def get_q_duncan(p, v):
    # Tabla de valores críticos de Duncan (nivel de significancia = 0.05)
    duncan_table = {
        2: {1: 18.0, 2: 6.09, 3: 4.50, 4: 3.93, 5: 3.64, 6: 3.46, 7: 3.35, 8: 3.26, 9: 3.20, 10: 3.15, 20: 3.05,
            50: 3.00, 100: 3.00},
        3: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.01, 5: 3.74, 6: 3.58, 7: 3.47, 8: 3.39, 9: 3.34, 10: 3.30, 20: 3.20,
            50: 3.13, 100: 3.12},
        4: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.79, 6: 3.64, 7: 3.54, 8: 3.47, 9: 3.41, 10: 3.37, 20: 3.28,
            50: 3.20, 100: 3.18},
        5: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.34,
            50: 3.26, 100: 3.23},
        6: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.34,
            50: 3.27, 100: 3.24},
        7: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.35,
            50: 3.28, 100: 3.25},
        8: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.36,
            50: 3.29, 100: 3.26},
        9: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.37,
            50: 3.30, 100: 3.27},
        10: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.38,
             50: 3.31, 100: 3.28},
        20: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.40,
             50: 3.34, 100: 3.31},
        50: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.41,
             50: 3.36, 100: 3.33},
        100: {1: 18.0, 2: 6.09, 3: 4.50, 4: 4.02, 5: 3.83, 6: 3.68, 7: 3.58, 8: 3.52, 9: 3.47, 10: 3.43, 20: 3.42,
              50: 3.37, 100: 3.34},
    }

    # Interpolación lineal entre dos valores de p o v
    def interpolate(value, table):
        sorted_keys = sorted(table.keys())
        if value in table:
            return table[value]
        for i in range(1, len(sorted_keys)):
            if sorted_keys[i-1] <= value <= sorted_keys[i]:
                x0, y0 = sorted_keys[i-1], table[sorted_keys[i-1]]
                x1, y1 = sorted_keys[i], table[sorted_keys[i]]
                return y0 + (value - x0) * (y1 - y0) / (x1 - x0)
        return "Valor fuera del rango"

    # Encuentra el valor crítico
    if p in duncan_table and v in duncan_table[p]:
        return duncan_table[p][v]
    elif p in duncan_table:
        return interpolate(v, duncan_table[p])
    elif v in duncan_table:
        return interpolate(p, duncan_table[v])
    else:
        return "Valores fuera de la tabla de referencia. Ajusta p o v."


def calculate_duncan_critical_value(group_means, v):
    p = len(group_means)  # Número de grupos
    group_means.sort(reverse=True)  # Ordenar las medias de mayor a menor
    q_critical = get_q_duncan(p, v)
    return q_critical

# Solicitar datos al usuario
try:
    group_means_input = input("Ingresa las medias de los grupos separadas por espacios: ")
    group_means = list(map(float, group_means_input.split()))
    v = int(input("Ingresa los grados de libertad del ANOVA: "))

    # Calcular el valor crítico de Duncan
    q_critical = calculate_duncan_critical_value(group_means, v)
    print(f"\nEl valor crítico de Duncan es: {q_critical}")
except ValueError:
    print("Por favor, ingresa valores válidos.")

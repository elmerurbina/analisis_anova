import random
import keyboard


# Función para asignar tratamientos de forma aleatoria y en columnas
def asignar_tratamientos_en_columnas(subjects, num_columns):
    random.shuffle(subjects)  # Barajamos la lista de sujetos aleatoriamente
    columnas = {f"Bloque {chr(65 + i)}": [] for i in range(num_columns)}  # Crear nombres de columnas dinámicamente

    # Asignamos sujetos a las columnas en orden
    for idx, subject in enumerate(subjects):
        columna = f"Bloque {chr(65 + idx % num_columns)}"
        columnas[columna].append(subject)

    return columnas


# Entradas de datos
subjects_input = input("Ingrese los números de las muestras separados por espacios (hasta 20): ").split()
try:
    subjects = [float(subject) for subject in subjects_input]  # Convertir a flotantes
except ValueError:
    print("Error: Por favor ingrese solo números decimales o enteros separados por espacios.")
    exit()

# Validación del número de sujetos
if len(subjects) > 20 or (len(subjects) % 3 != 0 and len(subjects) % 4 != 0):
    print("Error: El número de sujetos debe ser múltiplo de 3 o 4 y no puede exceder 20.")
    exit()

# Selección dinámica de columnas según el número de sujetos
if len(subjects) % 3 == 0:  # Configuración para múltiplos de 3
    num_columns = 3
    print(f"\nAsignación con {num_columns} columnas y {len(subjects) // num_columns} filas.")
    if len(subjects) == 18:
        print("Presiona Ctrl+X para continuar...")
        keyboard.wait('ctrl+x')  # Espera hasta que el usuario presione Ctrl+X
else:  # Configuración estándar para múltiplos de 4
    num_columns = 4
    print(f"\nAsignación con {num_columns} columnas y {len(subjects) // num_columns} filas.")

# Realizamos la asignación aleatoria en columnas
asignacion_aleatoria = asignar_tratamientos_en_columnas(subjects, num_columns)

# Mostramos la asignación aleatoria
print("\nAsignación aleatoria de tratamientos:")
for columna, sujetos in asignacion_aleatoria.items():
    print(f"{columna}: {sujetos}")

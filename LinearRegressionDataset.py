import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import joblib


archivo_csv = "https://drive.google.com/uc?id=1KH62XtloMmxz9K3r2i4GFjlhGACnaiyR"
df = pd.read_csv(archivo_csv)

# Selecciona las variables objetivos
X = df[['Word count', '# of Links', '# of comments', '# Images video', 'Elapsed days']]
y = df['# Shares']

# Manejo de datos faltantes
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)

# Limpieza de los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo de regresion lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer las predicciones y evaluar el modelo
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Media de Error Absoluto (MAE): {mae}")
print(f"R-cuadrado (R^2): {r2}")

# Visualiza los resultados
plt.scatter(y_test, y_pred, color='blue', edgecolor='w')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("Actual # Shares")
plt.ylabel("Predicted # Shares")
plt.title("Actual vs Predicted # Shares")
plt.show()

# Guarda el modelo entrenado
joblib.dump(model, 'modelo_regresion_lineal.pkl')
print("Model saved as 'modelo_regresion_lineal.pkl'")

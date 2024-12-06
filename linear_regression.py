import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt


# Function to validate if x and y values have the same length
def validate_input(x, y):
    if len(x) != len(y):
        messagebox.showerror("Error", "The number of X and Y values must be the same.")
        return False
    return True


# Function to calculate and display results for the normal method
def normal_method():
    try:
        x = np.array(list(map(float, entry_x.get().split())))
        y = np.array(list(map(float, entry_y.get().split())))

        if not validate_input(x, y):
            return

        n = len(x)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)  # Sum of xy
        sum_x2 = np.sum(x ** 2)  # Sum of x^2
        sum_y2 = np.sum(y ** 2)  # Sum of y^2

        b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        a = (sum_y - b * sum_x) / n

        mean_x = np.mean(x)
        mean_y = np.mean(y)

        # Create a formatted output for the table and display in the GUI
        output = "Normal Method:\n"
        output += "x\t\ty\t\tx^2\t\ty^2\t\txy\t\tProjection (a + bx)\n"
        output += "-" * 90 + "\n"

        sum_projection = 0

        for i in range(n):
            projection = a + b * x[i]
            sum_projection += projection
            output += f"{x[i]:.4f}\t\t{y[i]:.4f}\t\t{x[i] ** 2:.4f}\t\t{y[i] ** 2:.4f}\t\t{(x[i] * y[i]):.4f}\t\t{projection:.4f}\n"

        output += "-" * 90 + "\n"
        output += f"Total X: {sum_x:.4f}\n"
        output += f"Total Y: {sum_y:.4f}\n"
        output += f"Total X^2: {sum_x2:.4f}\n"
        output += f"Total Y^2: {sum_y2:.4f}\n"
        output += f"Total XY: {sum_xy:.4f}\n"
        output += f"Total Projection: {sum_projection:.4f}\n"

        # Show a and b values separately
        output += f"\nMean of X: {mean_x:.4f}\n"
        output += f"Mean of Y: {mean_y:.4f}\n"
        output += f"Value of a: {a:.4f}\n"
        output += f"Value of b: {b:.4f}\n"
        output += f"General Equation: y = {a:.4f} + {b:.4f}x\n"

        # Display output in the text widget
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, output)

        # Plot regression line
        plot_regression(x, y, a, b, f"y = {a:.4f} + {b:.4f}x")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to calculate and display results for the least squares method
def least_squares_method():
    try:
        x = np.array(list(map(float, entry_x.get().split())))
        y = np.array(list(map(float, entry_y.get().split())))

        if not validate_input(x, y):
            return

        n = len(x)

        # Calculate means
        mean_x = np.mean(x)
        mean_y = np.mean(y)

        # Prepare data for the first table
        output_table_1 = "Least Squares Method - Table 1:\n"
        output_table_1 += "x\t\ty\t\tSx\t\tSy\t\tProjection P\n"
        output_table_1 += "-" * 70 + "\n"

        projections = []
        sum_SxSy = 0  # To calculate total SxSy
        sum_Sx_squared = 0  # To calculate total Sx^2
        sum_x = 0  # Total sum of x
        sum_y = 0  # Total sum of y

        for i in range(n):
            Sx = x[i] - mean_x  # Deviation from mean for x
            Sy = y[i] - mean_y  # Deviation from mean for y
            P = mean_y + (Sy / Sx if Sx != 0 else 0) * (x[i] - mean_x)  # Projection calculation

            projections.append(P)
            sum_SxSy += Sx * Sy  # Increment total SxSy
            sum_Sx_squared += Sx ** 2  # Increment total Sx^2
            sum_x += x[i]  # Increment total sum of x
            sum_y += y[i]  # Increment total sum of y
            output_table_1 += f"{x[i]:.4f}\t\t{y[i]:.4f}\t\t{Sx:.4f}\t\t{Sy:.4f}\t\t{P:.4f}\n"

        output_table_1 += "-" * 70 + "\n"
        output_table_1 += f"Total SxSy: {sum_SxSy:.4f}\n"
        output_table_1 += f"Total X: {sum_x:.4f}\n"
        output_table_1 += f"Total Y: {sum_y:.4f}\n"

        output_table_1 += f"Mean of X: {mean_x:.4f}\n"
        output_table_1 += f"Mean of Y: {mean_y:.4f}\n"

        # Prepare data for the second table
        output_table_2 = "Least Squares Method - Table 2:\n"
        output_table_2 += "x\t\tSx^2\t\tSxSy\n"
        output_table_2 += "-" * 40 + "\n"

        for i in range(n):
            Sx = x[i] - mean_x  # Deviation from mean for x
            Sy = y[i] - mean_y  # Deviation from mean for y
            Sx_squared = Sx ** 2  # Square of the deviation
            SxSy = Sx * Sy  # Product of deviations

            output_table_2 += f"{x[i]:.4f}\t\t{Sx_squared:.4f}\t\t{SxSy:.4f}\n"

        output_table_2 += "-" * 40 + "\n"
        output_table_2 += f"Total Sx^2: {sum_Sx_squared:.4f}\n"

        # Calculate a and b for least squares method
        b = sum_SxSy / sum_Sx_squared if sum_Sx_squared != 0 else 0
        a = mean_y - b * mean_x

        output_table_2 += f"Value of a: {a:.4f}\n"
        output_table_2 += f"Value of b: {b:.4f}\n"
        output_table_2 += f"General Equation: y = {a:.4f} + {b:.4f}x\n"

        # Display output in the text widget
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, output_table_1)
        result_text.insert(tk.END, output_table_2)

        # Plot regression line
        plot_regression(x, y, a, b, f"y = {a:.4f} + {b:.4f}x")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to plot the linear regression graph
def plot_regression(x, y, a, b, equation):
    plt.scatter(x, y, color="blue", label="Data points")
    plt.plot(x, a + b * x, color="red", label=equation)
    plt.scatter(x, a + b * x, color="yellow", label="Projections")
    plt.title("Linear Regression")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()


# Set up the GUI using Tkinter
root = tk.Tk()
root.title("Simple Linear Regression Calculator")

# Labels and text fields for input
label_x = tk.Label(root, text="Enter X values (space-separated):")
label_x.grid(row=0, column=0, padx=10, pady=5)
entry_x = tk.Entry(root, width=40)
entry_x.grid(row=0, column=1, padx=10, pady=5)

label_y = tk.Label(root, text="Enter Y values (space-separated):")
label_y.grid(row=1, column=0, padx=10, pady=5)
entry_y = tk.Entry(root, width=40)
entry_y.grid(row=1, column=1, padx=10, pady=5)

# Text area for displaying results
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Button for normal method
btn_normal = tk.Button(root, text="Normal Method", command=normal_method)
btn_normal.grid(row=3, column=0, padx=10, pady=10)

# Button for least squares method
btn_least_squares = tk.Button(root, text="Least Squares Method", command=least_squares_method)
btn_least_squares.grid(row=3, column=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()

"""
Solve quadratic equations a*x**2 + b*x + c = 0 with coefficients read
from the terminal, and plot the corresponding quadratic function using
matplotlib.pyplot (replacing the pylab module used in the book).
"""
import matplotlib.pyplot as plt
import numpy as np


while True:
    a_input = input("Enter coefficient a (ENTER to quit): ")
    if a_input == "":
        break
    a = float(a_input)
    b = float(input("Enter coefficient b: "))
    c = float(input("Enter coefficient c: "))

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        print("no real solutions")
        xopt = -b / (2 * a)
        x_min, x_max = xopt - 5, xopt + 5
    elif discriminant == 0:
        x1 = -b / (2 * a)
        print("one solution: ", x1)
        x_min, x_max = x1 - 5, x1 + 5
    else:
        sqrt_disc = np.sqrt(discriminant)
        x1 = (-b + sqrt_disc) / (2 * a)
        x2 = (-b - sqrt_disc) / (2 * a)
        print("two solutions: ", x1, x2)
        lo, hi = min(x1, x2), max(x1, x2)
        margin = (hi - lo) * 0.5 + 1
        x_min, x_max = lo - margin, hi + margin

    x = np.linspace(x_min, x_max, 150)
    y = a * x**2 + b * x + c

    plt.figure()
    plt.plot(x, y)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title(f"y = {a}x^2 + {b}x + {c}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()
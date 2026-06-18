import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from curved_text import CurvedText

Mass_flow = 50.0          # lb/s
Density = 60.0            # lb/ft^3
Viscosity = 6.72e-4       # lb/(ft·s)
Pump_Efficiency = 0.6
Cost_Coeff_Pump = 0.5938
Cost_Coeff_Pipe = 5.7
Pipe_Exponent = 1.3
Pipe_Length = 1.0         # ft
Gravitational_constant = 32.174  # lb·ft/(lbf·s^2)


def total_cost(diameter):
    area = np.pi * diameter**2 / 4
    velocity = Mass_flow / (Density * area)
    reynolds = Density * velocity * diameter / Viscosity
    friction_factor = 0.046 * reynolds**-0.2
    friction_loss = 2 * friction_factor * Pipe_Length * velocity**2 / diameter

    capital = Cost_Coeff_Pipe * diameter**Pipe_Exponent
    operating = (Cost_Coeff_Pump / Pump_Efficiency) * Mass_flow * friction_loss / Gravitational_constant
    return capital + operating


def make_plot(diameter_opt):
    diameters = np.linspace(0.2, 1.2, 300)
    capital = Cost_Coeff_Pipe * diameters**Pipe_Exponent
    operating = np.array([total_cost(d) for d in diameters]) - capital
    total = capital + operating

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(diameters, capital, lw=2, color="#1f77b4")
    ax.plot(diameters, operating, lw=2, color="#ff0e12")
    ax.plot(diameters, total, lw=2.5, color="#2ca02c")
    ax.axvline(diameter_opt, color="grey", ls=":")
    ax.set_xlim(0.2, 1.2)
    ax.set_ylim(-2, 38)

    CurvedText(diameters, capital, "capital", ax, pos=0.070, offset=-7.5,
               color="#1f77b4", fontsize=13, fontweight="bold")
    CurvedText(diameters, operating, "operating", ax, pos=0.1, offset=7.5,
               color="#ff0e12", fontsize=13, fontweight="bold")
    CurvedText(diameters, total, "total", ax, pos=0.9, offset=8,
               color="#2ca02c", fontsize=13, fontweight="bold")

    ax.plot(diameter_opt, total_cost(diameter_opt), "o", color="black", zorder=5)
    ax.annotate(f"D = {diameter_opt:.3f} ft", xy=(diameter_opt, total_cost(diameter_opt)),
                xytext=(8, 10), textcoords="offset points", fontsize=12, fontweight="bold")

    ax.set_xlabel("Diameter D (ft)")
    ax.set_ylabel("Annual cost ($/yr)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("pipe_plot.png", dpi=300)
    plt.show()

result = minimize_scalar(total_cost, bounds=(0.1, 2.0), method="bounded")
diameter_opt = result.x
velocity_opt = Mass_flow / (Density * np.pi * diameter_opt**2 / 4)

print(f"Optimal diameter: {diameter_opt:.4f} ft = {diameter_opt * 12:.2f} in")
print(f"Velocity:         {velocity_opt:.2f} ft/s")

make_plot(diameter_opt)
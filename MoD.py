# educational purpose python code. Free to use and modify. Main concept atributed to radu-mihai.panduru@student.tuiasi.ro
#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Funcții pentru calcule
def presiunea_saturatiei(temp):
    """Calculul presiunii de saturație (hPa) în funcție de temperatură."""
    return 6.1078 * np.exp((17.27 * temp) / (temp + 237.3))

def umiditate_absoluta(RH, temp, pres_atm):
    """Calculul umidității absolute (kg vapori / kg aer uscat)."""
    P_sat = presiunea_saturatiei(temp)
    P_v = RH * P_sat / 100  # Presiunea parțială
    return 0.622 * P_v / (pres_atm - P_v)

def entalpia(temp, W):
    """Calculul entalpiei specifice (kJ/kg)."""
    cp_air = 1.006  # kJ/(kg*K), aer uscat
    h_fg = 2501  # kJ/kg, căldura de vaporizare
    cp_vapor = 1.86  # kJ/(kg*K), vapori de apă
    return cp_air * temp + W * (h_fg + cp_vapor * temp)

# Generarea graficului
def genereaza_grafic(TI, RH, presiune_atm):
    temperaturi = np.linspace(-30, 80, 100)  # °C

    # Calculăm parametrii
    humidity_ratio = [umiditate_absoluta(RH, temp, presiune_atm) * 1000 for temp in temperaturi]

    # Generăm figura principală
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Graficul principal: Humidity Ratio vs Temperature
    ax1.set_title("Humidity Ratio vs Temperature and Air Density")
    ax1.set_xlabel("Humidity Ratio (g/kg)")
    ax1.set_ylabel("Temperature (°C)")
    ax1.grid(True)

    # Linii parabolice RH
    for rh in range(10, 101, 10):  # RH de la 10% la 100%
        humidity_ratio_ref = [umiditate_absoluta(rh, temp, presiune_atm) * 1000 for temp in temperaturi]
        ax1.plot(humidity_ratio_ref, temperaturi, '--', color='lightgray', linewidth=0.8)
        max_index = np.argmax(humidity_ratio_ref)
        max_x = humidity_ratio_ref[max_index]
        max_y = temperaturi[max_index]
        ax1.text(max_x, max_y + 2, f"RH={rh}%", color='gray', fontsize=8, ha='center')

    # Linia albastră pentru RH măsurat
    ax1.plot(humidity_ratio, temperaturi, label=f"RH={RH}%, Presiune={presiune_atm} hPa", color='blue')

    # Linii de entalpie (cu portocaliu)
    entalpie_values = range(10, 100, 10)
    for h in entalpie_values:
        entalpie_line = []
        for temp in temperaturi:
            W = (h - 1.006 * temp) / (2501 + 1.86 * temp)
            entalpie_line.append(W * 1000)
        ax1.plot(entalpie_line, temperaturi, ':', color='orange', linewidth=0.8)
        low_index = 0
        low_x = entalpie_line[low_index]
        low_y = temperaturi[low_index]
        ax1.text(low_x, low_y - 2, f"H={h} kJ/kg", color='orange', fontsize=8, ha='center', rotation=-30)

    # Forma rectangulară pentru zona de confort
    comfort_zone_x = [
        umiditate_absoluta(30, 18, presiune_atm) * 1000,
        umiditate_absoluta(30, 24, presiune_atm) * 1000,
        umiditate_absoluta(60, 27, presiune_atm) * 1000,
        umiditate_absoluta(60, 21, presiune_atm) * 1000,
        umiditate_absoluta(30, 18, presiune_atm) * 1000
    ]
    comfort_zone_y = [18, 24, 27, 21, 18]
    ax1.fill(comfort_zone_x, comfort_zone_y, color='green', alpha=0.3, label="Comfort Zone")

    corner_labels = ["18°C", "24°C", "27°C", "21°C"]
    for i, (x, y) in enumerate(zip(comfort_zone_x[:-1], comfort_zone_y[:-1])):
        ax1.text(x, y, corner_labels[i], color='black', fontsize=9, ha='center', va='bottom')

    # Linia orizontală pentru TI (roșie)
    ax1.axhline(y=TI, color='red', linestyle='-', linewidth=1.5, label=f"TI={TI}°C")

    # Calculăm intersecția RH-TI
    intersection_x = umiditate_absoluta(RH, TI, presiune_atm) * 1000
    ax1.scatter(intersection_x, TI, color='red', edgecolor='black', s=80, zorder=5, label="Intersecție RH-TI")

    # Restaurăm legenda graficului principal
    ax1.legend(loc="upper left")

    # Calculăm densitatea aerului
    temperaturi_abs = temperaturi + 273.15
    air_density = [(presiune_atm * 100) / (287.05 * T) for T in temperaturi_abs]

    # Afișăm densitatea aerului pe grafic
    ax2 = ax1.twinx()
    ax2.set_ylabel("Air Density (kg/m³)", color='green')
    ax2.plot(temperaturi, air_density, color='green', label="Air Density")
    ax2.set_ylim(min(air_density), max(air_density))
    ax2.legend(loc="center right")

    plt.show()

# Interfața Tkinter
def main():
    root = tk.Tk()
    root.title("Introducerea valorilor pentru grafic")

    ttk.Label(root, text="TI (Temperatura interioară):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text="RH (Umiditatea relativă):").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(root, text="Presiunea atmosferică (hPa):").grid(row=2, column=0, padx=10, pady=10)

    ti_entry = ttk.Entry(root)
    ti_entry.grid(row=0, column=1, padx=10, pady=10)
    rh_entry = ttk.Entry(root)
    rh_entry.grid(row=1, column=1, padx=10, pady=10)
    pres_entry = ttk.Entry(root)
    pres_entry.grid(row=2, column=1, padx=10, pady=10)

    def on_generate():
        try:
            TI = float(ti_entry.get())
            RH = float(rh_entry.get())
            presiune_atm = float(pres_entry.get())
            genereaza_grafic(TI, RH, presiune_atm)
        except ValueError:
            print("Introduceți valori valide!")

    ttk.Button(root, text="Generează Grafic", command=on_generate).grid(row=3, column=0, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

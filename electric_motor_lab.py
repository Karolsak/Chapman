#!/usr/bin/env python3
"""
Laboratorium Modelowania Silników Elektrycznych - GUI
======================================================
Aplikacja do symulacji i badania różnych typów silników elektrycznych.

Typy silników:
- Silnik DC (z wzbudzeniem szeregowym, bocznikowym, obcym)
- Silnik Indukcyjny (asynchroniczny)
- Silnik Synchroniczny

Autor: Lab System
Data: 2025-11-06
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Import modeli silników z osobnego modułu
from motor_models import DCMotor, InductionMotor, SynchronousMotor


class MotorLabGUI:
    """Główny interfejs graficzny laboratorium"""

    def __init__(self, root):
        """Inicjalizacja GUI"""
        self.root = root
        self.root.title("Laboratorium Modelowania Silników Elektrycznych")
        self.root.geometry("1400x900")

        # Inicjalizacja silników
        self.dc_motor = DCMotor('shunt')
        self.induction_motor = InductionMotor()
        self.sync_motor = SynchronousMotor()

        # Tworzenie interfejsu
        self.create_widgets()

    def create_widgets(self):
        """Tworzenie widgetów GUI"""
        # Notebook (zakładki)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Zakładki dla różnych typów silników
        self.create_dc_motor_tab()
        self.create_induction_motor_tab()
        self.create_sync_motor_tab()
        self.create_comparison_tab()

    def create_dc_motor_tab(self):
        """Zakładka silnika DC"""
        dc_frame = ttk.Frame(self.notebook)
        self.notebook.add(dc_frame, text="Silnik DC")

        # Podział na panele
        left_panel = ttk.Frame(dc_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        right_panel = ttk.Frame(dc_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel parametrów
        param_frame = ttk.LabelFrame(left_panel, text="Parametry Silnika DC", padding=10)
        param_frame.pack(fill=tk.BOTH, expand=True)

        # Typ silnika
        ttk.Label(param_frame, text="Typ wzbudzenia:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dc_type_var = tk.StringVar(value='shunt')
        dc_type_combo = ttk.Combobox(param_frame, textvariable=self.dc_type_var,
                                      values=['shunt', 'series', 'separate'],
                                      state='readonly', width=15)
        dc_type_combo.grid(row=0, column=1, pady=5)
        dc_type_combo.bind('<<ComboboxSelected>>', self.update_dc_motor)

        # Parametry
        params = [
            ("Napięcie V [V]:", 'V', 220.0, 0, 500),
            ("Rezystancja Ra [Ω]:", 'Ra', 0.5, 0.01, 10),
            ("Rezystancja Rf [Ω]:", 'Rf', 100.0, 1, 500),
            ("Stała Ke [V·s/rad]:", 'Ke', 0.8, 0.1, 5),
            ("Stała Kt [N·m/A]:", 'Kt', 0.8, 0.1, 5),
        ]

        self.dc_params = {}
        for i, (label, param, default, min_val, max_val) in enumerate(params, start=1):
            ttk.Label(param_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)

            var = tk.DoubleVar(value=default)
            self.dc_params[param] = var

            spinbox = ttk.Spinbox(param_frame, from_=min_val, to=max_val,
                                  textvariable=var, width=15, increment=0.1)
            spinbox.grid(row=i, column=1, pady=5)

        # Przycisk symulacji
        ttk.Button(param_frame, text="Uruchom Symulację",
                   command=self.simulate_dc_motor).grid(row=len(params)+1, column=0,
                                                         columnspan=2, pady=20)

        # Panel wykresów
        self.dc_figure = Figure(figsize=(10, 8), dpi=100)
        self.dc_canvas = FigureCanvasTkAgg(self.dc_figure, right_panel)
        self.dc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = NavigationToolbar2Tk(self.dc_canvas, right_panel)
        toolbar.update()

    def create_induction_motor_tab(self):
        """Zakładka silnika indukcyjnego"""
        ind_frame = ttk.Frame(self.notebook)
        self.notebook.add(ind_frame, text="Silnik Indukcyjny")

        # Podział na panele
        left_panel = ttk.Frame(ind_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        right_panel = ttk.Frame(ind_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel parametrów
        param_frame = ttk.LabelFrame(left_panel, text="Parametry Silnika Indukcyjnego", padding=10)
        param_frame.pack(fill=tk.BOTH, expand=True)

        # Parametry
        params = [
            ("Liczba biegunów P:", 'P', 4, 2, 12),
            ("Napięcie V [V]:", 'V', 400, 100, 1000),
            ("Częstotliwość f [Hz]:", 'f', 50, 25, 100),
            ("Rezystancja Rs [Ω]:", 'Rs', 0.5, 0.01, 10),
            ("Rezystancja Rr [Ω]:", 'Rr', 0.4, 0.01, 10),
            ("Reaktancja Xs [Ω]:", 'Xs', 1.5, 0.1, 10),
            ("Reaktancja Xr [Ω]:", 'Xr', 1.5, 0.1, 10),
            ("Reaktancja Xm [Ω]:", 'Xm', 50, 10, 200),
        ]

        self.ind_params = {}
        for i, (label, param, default, min_val, max_val) in enumerate(params):
            ttk.Label(param_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)

            var = tk.DoubleVar(value=default)
            self.ind_params[param] = var

            spinbox = ttk.Spinbox(param_frame, from_=min_val, to=max_val,
                                  textvariable=var, width=15, increment=0.1)
            spinbox.grid(row=i, column=1, pady=5)

        # Przycisk symulacji
        ttk.Button(param_frame, text="Uruchom Symulację",
                   command=self.simulate_induction_motor).grid(row=len(params), column=0,
                                                                columnspan=2, pady=20)

        # Panel wykresów
        self.ind_figure = Figure(figsize=(10, 8), dpi=100)
        self.ind_canvas = FigureCanvasTkAgg(self.ind_figure, right_panel)
        self.ind_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = NavigationToolbar2Tk(self.ind_canvas, right_panel)
        toolbar.update()

    def create_sync_motor_tab(self):
        """Zakładka silnika synchronicznego"""
        sync_frame = ttk.Frame(self.notebook)
        self.notebook.add(sync_frame, text="Silnik Synchroniczny")

        # Podział na panele
        left_panel = ttk.Frame(sync_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        right_panel = ttk.Frame(sync_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel parametrów
        param_frame = ttk.LabelFrame(left_panel, text="Parametry Silnika Synchronicznego", padding=10)
        param_frame.pack(fill=tk.BOTH, expand=True)

        # Parametry
        params = [
            ("Liczba biegunów P:", 'P', 4, 2, 12),
            ("Napięcie V [V]:", 'V', 400, 100, 1000),
            ("Częstotliwość f [Hz]:", 'f', 50, 25, 100),
            ("Reaktancja Xs [Ω]:", 'Xs', 2.0, 0.1, 10),
            ("Rezystancja Ra [Ω]:", 'Ra', 0.3, 0.01, 5),
            ("SEM wzbudzenia Ef [V]:", 'Ef', 460, 100, 1000),
        ]

        self.sync_params = {}
        for i, (label, param, default, min_val, max_val) in enumerate(params):
            ttk.Label(param_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)

            var = tk.DoubleVar(value=default)
            self.sync_params[param] = var

            spinbox = ttk.Spinbox(param_frame, from_=min_val, to=max_val,
                                  textvariable=var, width=15, increment=0.1)
            spinbox.grid(row=i, column=1, pady=5)

        # Przycisk symulacji
        ttk.Button(param_frame, text="Uruchom Symulację",
                   command=self.simulate_sync_motor).grid(row=len(params), column=0,
                                                           columnspan=2, pady=20)

        # Panel wykresów
        self.sync_figure = Figure(figsize=(10, 8), dpi=100)
        self.sync_canvas = FigureCanvasTkAgg(self.sync_figure, right_panel)
        self.sync_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = NavigationToolbar2Tk(self.sync_canvas, right_panel)
        toolbar.update()

    def create_comparison_tab(self):
        """Zakładka porównania silników"""
        comp_frame = ttk.Frame(self.notebook)
        self.notebook.add(comp_frame, text="Porównanie")

        info_text = """
        LABORATORIUM MODELOWANIA SILNIKÓW ELEKTRYCZNYCH
        ===============================================

        Ta aplikacja umożliwia symulację i analizę trzech głównych typów silników:

        1. SILNIK DC (prądu stałego)
           - Wzbudzenie bocznikowe (shunt)
           - Wzbudzenie szeregowe (series)
           - Wzbudzenie obce (separate)

        2. SILNIK INDUKCYJNY (asynchroniczny)
           - Model oparty na schemacie zastępczym
           - Charakterystyki moment-poślizg
           - Analiza sprawności i współczynnika mocy

        3. SILNIK SYNCHRONICZNY
           - Charakterystyki kąt obciążenia-moment
           - Analiza współczynnika mocy
           - Krzywa V (prąd vs wzbudzenie)

        INSTRUKCJE:
        -----------
        1. Wybierz zakładkę z odpowiednim typem silnika
        2. Ustaw parametry silnika w lewym panelu
        3. Kliknij "Uruchom Symulację"
        4. Analizuj wykresy charakterystyk
        5. Eksperymentuj z różnymi parametrami

        CHARAKTERYSTYKI:
        ----------------
        - Moment vs Prędkość
        - Prąd vs Obciążenie
        - Sprawność vs Obciążenie
        - Współczynnik mocy (silniki AC)

        Wykresy można powiększać, przesuwać i zapisywać używając paska narzędzi.
        """

        text_widget = tk.Text(comp_frame, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert('1.0', info_text)
        text_widget.config(state=tk.DISABLED)

    def update_dc_motor(self, event=None):
        """Aktualizacja typu silnika DC"""
        self.dc_motor.motor_type = self.dc_type_var.get()

    def simulate_dc_motor(self):
        """Symulacja silnika DC"""
        try:
            # Aktualizacja parametrów
            self.dc_motor.motor_type = self.dc_type_var.get()
            self.dc_motor.V = self.dc_params['V'].get()
            self.dc_motor.Ra = self.dc_params['Ra'].get()
            self.dc_motor.Rf = self.dc_params['Rf'].get()
            self.dc_motor.Ke = self.dc_params['Ke'].get()
            self.dc_motor.Kt = self.dc_params['Kt'].get()

            # Obliczenia
            results = self.dc_motor.calculate_characteristics()

            # Rysowanie wykresów
            self.dc_figure.clear()

            # Wykres 1: Moment vs Prędkość
            ax1 = self.dc_figure.add_subplot(2, 2, 1)
            ax1.plot(results['speed_rpm'], results['T_load'], 'b-', linewidth=2)
            ax1.set_xlabel('Prędkość [RPM]')
            ax1.set_ylabel('Moment [N·m]')
            ax1.set_title('Charakterystyka Moment-Prędkość')
            ax1.grid(True, alpha=0.3)

            # Wykres 2: Prąd vs Moment
            ax2 = self.dc_figure.add_subplot(2, 2, 2)
            ax2.plot(results['T_load'], results['current'], 'r-', linewidth=2)
            ax2.set_xlabel('Moment [N·m]')
            ax2.set_ylabel('Prąd twornika [A]')
            ax2.set_title('Charakterystyka Prąd-Moment')
            ax2.grid(True, alpha=0.3)

            # Wykres 3: Sprawność vs Moment
            ax3 = self.dc_figure.add_subplot(2, 2, 3)
            ax3.plot(results['T_load'], results['efficiency'], 'g-', linewidth=2)
            ax3.set_xlabel('Moment [N·m]')
            ax3.set_ylabel('Sprawność [%]')
            ax3.set_title('Charakterystyka Sprawności')
            ax3.set_ylim([0, 100])
            ax3.grid(True, alpha=0.3)

            # Wykres 4: Moc vs Prędkość
            ax4 = self.dc_figure.add_subplot(2, 2, 4)
            power_kw = results['power_out'] / 1000
            ax4.plot(results['speed_rpm'], power_kw, 'm-', linewidth=2)
            ax4.set_xlabel('Prędkość [RPM]')
            ax4.set_ylabel('Moc wyjściowa [kW]')
            ax4.set_title('Charakterystyka Mocy')
            ax4.grid(True, alpha=0.3)

            self.dc_figure.tight_layout()
            self.dc_canvas.draw()

        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas symulacji: {str(e)}")

    def simulate_induction_motor(self):
        """Symulacja silnika indukcyjnego"""
        try:
            # Aktualizacja parametrów
            self.induction_motor.P = int(self.ind_params['P'].get())
            self.induction_motor.V = self.ind_params['V'].get()
            self.induction_motor.f = self.ind_params['f'].get()
            self.induction_motor.Rs = self.ind_params['Rs'].get()
            self.induction_motor.Rr = self.ind_params['Rr'].get()
            self.induction_motor.Xs = self.ind_params['Xs'].get()
            self.induction_motor.Xr = self.ind_params['Xr'].get()
            self.induction_motor.Xm = self.ind_params['Xm'].get()

            # Obliczenia
            results = self.induction_motor.calculate_characteristics()

            # Rysowanie wykresów
            self.ind_figure.clear()

            # Wykres 1: Moment vs Prędkość
            ax1 = self.ind_figure.add_subplot(2, 2, 1)
            ax1.plot(results['speed_rpm'], results['torque'], 'b-', linewidth=2)
            ax1.axvline(x=results['sync_speed'], color='r', linestyle='--',
                        label=f'Prędkość sync. = {results["sync_speed"]:.0f} RPM')
            ax1.set_xlabel('Prędkość [RPM]')
            ax1.set_ylabel('Moment [N·m]')
            ax1.set_title('Charakterystyka Moment-Prędkość')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Wykres 2: Moment vs Poślizg
            ax2 = self.ind_figure.add_subplot(2, 2, 2)
            ax2.plot(results['slip'], results['torque'], 'r-', linewidth=2)
            ax2.set_xlabel('Poślizg s')
            ax2.set_ylabel('Moment [N·m]')
            ax2.set_title('Charakterystyka Moment-Poślizg')
            ax2.grid(True, alpha=0.3)

            # Wykres 3: Sprawność vs Prędkość
            ax3 = self.ind_figure.add_subplot(2, 2, 3)
            ax3.plot(results['speed_rpm'], results['efficiency'], 'g-', linewidth=2)
            ax3.set_xlabel('Prędkość [RPM]')
            ax3.set_ylabel('Sprawność [%]')
            ax3.set_title('Charakterystyka Sprawności')
            ax3.set_ylim([0, 100])
            ax3.grid(True, alpha=0.3)

            # Wykres 4: Współczynnik mocy vs Obciążenie
            ax4 = self.ind_figure.add_subplot(2, 2, 4)
            ax4.plot(results['torque'], results['power_factor'], 'm-', linewidth=2)
            ax4.set_xlabel('Moment [N·m]')
            ax4.set_ylabel('Współczynnik mocy cos(φ)')
            ax4.set_title('Współczynnik Mocy')
            ax4.set_ylim([0, 1])
            ax4.grid(True, alpha=0.3)

            self.ind_figure.tight_layout()
            self.ind_canvas.draw()

        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas symulacji: {str(e)}")

    def simulate_sync_motor(self):
        """Symulacja silnika synchronicznego"""
        try:
            # Aktualizacja parametrów
            self.sync_motor.P = int(self.sync_params['P'].get())
            self.sync_motor.V = self.sync_params['V'].get()
            self.sync_motor.f = self.sync_params['f'].get()
            self.sync_motor.Xs = self.sync_params['Xs'].get()
            self.sync_motor.Ra = self.sync_params['Ra'].get()
            self.sync_motor.Ef = self.sync_params['Ef'].get()

            # Obliczenia
            results = self.sync_motor.calculate_characteristics()

            # Rysowanie wykresów
            self.sync_figure.clear()

            # Wykres 1: Moment vs Kąt obciążenia
            ax1 = self.sync_figure.add_subplot(2, 2, 1)
            ax1.plot(results['load_angle_deg'], results['torque'], 'b-', linewidth=2)
            ax1.set_xlabel('Kąt obciążenia δ [°]')
            ax1.set_ylabel('Moment [N·m]')
            ax1.set_title('Charakterystyka Moment-Kąt obciążenia')
            ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax1.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
            ax1.grid(True, alpha=0.3)

            # Wykres 2: Prąd vs Kąt obciążenia
            ax2 = self.sync_figure.add_subplot(2, 2, 2)
            ax2.plot(results['load_angle_deg'], results['current'], 'r-', linewidth=2)
            ax2.set_xlabel('Kąt obciążenia δ [°]')
            ax2.set_ylabel('Prąd twornika [A]')
            ax2.set_title('Charakterystyka Prąd-Kąt obciążenia')
            ax2.grid(True, alpha=0.3)

            # Wykres 3: Współczynnik mocy vs Moment
            ax3 = self.sync_figure.add_subplot(2, 2, 3)
            ax3.plot(results['torque'], results['power_factor'], 'g-', linewidth=2)
            ax3.set_xlabel('Moment [N·m]')
            ax3.set_ylabel('Współczynnik mocy cos(φ)')
            ax3.set_title('Współczynnik Mocy')
            ax3.axhline(y=1.0, color='r', linestyle='--', label='cos(φ) = 1')
            ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax3.legend()
            ax3.grid(True, alpha=0.3)

            # Wykres 4: Moc vs Kąt obciążenia
            ax4 = self.sync_figure.add_subplot(2, 2, 4)
            power_kw = results['power_out'] / 1000
            ax4.plot(results['load_angle_deg'], power_kw, 'm-', linewidth=2)
            ax4.set_xlabel('Kąt obciążenia δ [°]')
            ax4.set_ylabel('Moc wyjściowa [kW]')
            ax4.set_title('Charakterystyka Mocy')
            ax4.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax4.grid(True, alpha=0.3)

            self.sync_figure.tight_layout()
            self.sync_canvas.draw()

            # Informacja o prędkości synchronicznej
            messagebox.showinfo("Info",
                                f"Prędkość synchroniczna: {results['speed_rpm']:.1f} RPM\n"
                                f"({results['speed_rad_s']:.2f} rad/s)")

        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas symulacji: {str(e)}")


def main():
    """Funkcja główna"""
    root = tk.Tk()
    app = MotorLabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

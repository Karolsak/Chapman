#!/usr/bin/env python3
"""
Modele matematyczne silników elektrycznych
==========================================
Moduł zawiera klasy modelujące różne typy silników elektrycznych:
- Silnik DC (wzbudzenie bocznikowe, szeregowe, obce)
- Silnik Indukcyjny (asynchroniczny)
- Silnik Synchroniczny

Autor: Lab System
Data: 2025-11-06
"""

import numpy as np


class DCMotor:
    """Model silnika DC"""

    def __init__(self, motor_type='shunt'):
        """
        Inicjalizacja silnika DC

        Args:
            motor_type: 'shunt' (bocznikowy), 'series' (szeregowy), 'separate' (obcy)
        """
        self.motor_type = motor_type

        # Parametry domyślne
        self.V = 220.0      # Napięcie zasilania [V]
        self.Ra = 0.5       # Rezystancja twornika [Ω]
        self.Rf = 100.0     # Rezystancja wzbudzenia [Ω]
        self.La = 0.01      # Indukcyjność twornika [H]
        self.Ke = 0.8       # Stała SEM [V·s/rad]
        self.Kt = 0.8       # Stała momentu [N·m/A]
        self.J = 0.01       # Moment bezwładności [kg·m²]
        self.B = 0.001      # Współczynnik tarcia [N·m·s/rad]

    def calculate_characteristics(self, T_load_range=None):
        """
        Oblicz charakterystyki silnika DC

        Returns:
            dict: Słownik z charakterystykami (prędkość, prąd, moment, sprawność)
        """
        if T_load_range is None:
            T_load_range = np.linspace(0, 50, 100)

        omega = np.zeros_like(T_load_range)
        Ia = np.zeros_like(T_load_range)
        efficiency = np.zeros_like(T_load_range)

        for i, T_load in enumerate(T_load_range):
            if self.motor_type == 'shunt' or self.motor_type == 'separate':
                # Wzbudzenie bocznikowe lub obce
                If = self.V / self.Rf
                Ke_eff = self.Ke * If

                # Równanie momentu: T = Kt*If*Ia - B*omega
                # Równanie napięcia: V = Ke_eff*omega + Ra*Ia
                # T_load = Kt*If*Ia - B*omega

                # Rozwiązanie dla omega i Ia
                # Ze względu na sprzężenie, używamy iteracji
                omega_val = (self.V - self.Ra * T_load / (self.Kt * If)) / Ke_eff
                omega_val = max(0, omega_val)  # Prędkość nie może być ujemna

                Ia_val = (self.V - Ke_eff * omega_val) / self.Ra
                Ia_val = max(0, Ia_val)

                # Korekta z uwzględnieniem tarcia
                omega_val = (self.V - self.Ra * Ia_val) / Ke_eff
                omega_val = max(0, omega_val)

            elif self.motor_type == 'series':
                # Wzbudzenie szeregowe - If = Ia
                # Bardziej skomplikowane równania
                if T_load < 0.1:
                    omega_val = 500  # Wysoka prędkość przy małym obciążeniu
                    Ia_val = 0.5
                else:
                    # Przybliżone rozwiązanie
                    Ia_val = np.sqrt(T_load / self.Kt) if T_load > 0 else 0
                    Ke_eff = self.Ke * Ia_val
                    omega_val = (self.V - self.Ra * Ia_val) / (Ke_eff if Ke_eff > 0.01 else 0.01)
                    omega_val = max(0, min(omega_val, 500))

            omega[i] = omega_val
            Ia[i] = Ia_val

            # Oblicz sprawność
            P_in = self.V * Ia_val
            P_out = T_load * omega_val
            if P_in > 0:
                efficiency[i] = (P_out / P_in) * 100
            else:
                efficiency[i] = 0

        # Konwersja omega z rad/s na RPM
        n_rpm = omega * 60 / (2 * np.pi)

        return {
            'T_load': T_load_range,
            'speed_rpm': n_rpm,
            'speed_rad_s': omega,
            'current': Ia,
            'efficiency': efficiency,
            'power_out': T_load_range * omega
        }


class InductionMotor:
    """Model silnika indukcyjnego (asynchronicznego)"""

    def __init__(self):
        """Inicjalizacja silnika indukcyjnego"""
        # Parametry domyślne (model IEEE)
        self.P = 4          # Liczba biegunów
        self.V = 400        # Napięcie fazowe [V]
        self.f = 50         # Częstotliwość [Hz]
        self.Rs = 0.5       # Rezystancja stojana [Ω]
        self.Rr = 0.4       # Rezystancja wirnika [Ω]
        self.Xs = 1.5       # Reaktancja rozproszenia stojana [Ω]
        self.Xr = 1.5       # Reaktancja rozproszenia wirnika [Ω]
        self.Xm = 50        # Reaktancja magnesująca [Ω]
        self.rated_power = 7500  # Moc znamionowa [W]

    def calculate_characteristics(self, slip_range=None):
        """
        Oblicz charakterystyki silnika indukcyjnego

        Returns:
            dict: Słownik z charakterystykami
        """
        if slip_range is None:
            slip_range = np.linspace(0.001, 1.0, 200)

        ns = 120 * self.f / self.P  # Prędkość synchroniczna [RPM]
        omega_s = 2 * np.pi * self.f / (self.P / 2)  # Prędkość synchroniczna [rad/s]

        T_em = np.zeros_like(slip_range)
        I_rotor = np.zeros_like(slip_range)
        efficiency = np.zeros_like(slip_range)
        power_factor = np.zeros_like(slip_range)

        for i, s in enumerate(slip_range):
            if s < 0.0001:
                s = 0.0001  # Unikaj dzielenia przez zero

            # Impedancja wirnika sprowadzona do stojana
            Zr = self.Rr / s + 1j * self.Xr

            # Impedancja równoległa Xm || Zr
            Z_parallel = (1j * self.Xm * Zr) / (1j * self.Xm + Zr)

            # Całkowita impedancja
            Z_total = self.Rs + 1j * self.Xs + Z_parallel

            # Prąd stojana
            I_s = self.V / abs(Z_total)

            # Prąd wirnika
            I_r = self.V * (1j * self.Xm) / (abs(Z_total) * abs(1j * self.Xm + Zr))
            I_rotor[i] = abs(I_r)

            # Moment elektromagnetyczny
            P_gap = 3 * I_rotor[i]**2 * self.Rr / s  # Moc w szczelinie powietrznej
            T_em[i] = P_gap / omega_s

            # Sprawność
            P_out = P_gap * (1 - s)
            P_in = 3 * self.V * I_s
            if P_in > 0:
                efficiency[i] = (P_out / P_in) * 100
            else:
                efficiency[i] = 0

            # Współczynnik mocy
            power_factor[i] = np.cos(np.angle(Z_total))

        # Prędkość wirnika
        n_rpm = ns * (1 - slip_range)
        omega = omega_s * (1 - slip_range)

        return {
            'slip': slip_range,
            'speed_rpm': n_rpm,
            'speed_rad_s': omega,
            'torque': T_em,
            'current': I_rotor,
            'efficiency': efficiency,
            'power_factor': power_factor,
            'sync_speed': ns
        }


class SynchronousMotor:
    """Model silnika synchronicznego"""

    def __init__(self):
        """Inicjalizacja silnika synchronicznego"""
        self.P = 4          # Liczba biegunów
        self.V = 400        # Napięcie fazowe [V]
        self.f = 50         # Częstotliwość [Hz]
        self.Xs = 2.0       # Reaktancja synchroniczna [Ω]
        self.Ra = 0.3       # Rezystancja twornika [Ω]
        self.Ef = 460       # SEM wzbudzenia [V]

    def calculate_characteristics(self, delta_range=None):
        """
        Oblicz charakterystyki silnika synchronicznego

        Args:
            delta_range: Zakres kąta obciążenia [rad]

        Returns:
            dict: Słownik z charakterystykami
        """
        if delta_range is None:
            delta_range = np.linspace(-np.pi/2, np.pi/2, 200)

        ns = 120 * self.f / self.P  # Prędkość synchroniczna [RPM]
        omega_s = 2 * np.pi * self.f / (self.P / 2)  # [rad/s]

        T_em = np.zeros_like(delta_range)
        I_a = np.zeros_like(delta_range)
        power_factor = np.zeros_like(delta_range)
        P_out = np.zeros_like(delta_range)

        for i, delta in enumerate(delta_range):
            # Moc elektromagnetyczna (na fazę)
            P_em = (self.V * self.Ef * np.sin(delta)) / self.Xs

            # Moment elektromagnetyczny
            T_em[i] = 3 * P_em / omega_s  # 3 fazy

            # Prąd twornika (przybliżenie)
            Ia_complex = (self.V - self.Ef * np.exp(1j * delta)) / (self.Ra + 1j * self.Xs)
            I_a[i] = abs(Ia_complex)

            # Współczynnik mocy
            phi = np.angle(Ia_complex)
            power_factor[i] = np.cos(phi)

            # Moc wyjściowa
            P_out[i] = 3 * P_em - 3 * I_a[i]**2 * self.Ra

        return {
            'load_angle_deg': np.degrees(delta_range),
            'load_angle_rad': delta_range,
            'torque': T_em,
            'current': I_a,
            'power_factor': power_factor,
            'power_out': P_out,
            'speed_rpm': ns,
            'speed_rad_s': omega_s
        }


if __name__ == "__main__":
    print("To jest moduł biblioteczny. Import klas:")
    print("  from motor_models import DCMotor, InductionMotor, SynchronousMotor")
    print("\nAby uruchomić testy, użyj:")
    print("  python test_motors_cli.py")

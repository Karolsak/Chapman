#!/usr/bin/env python3
"""
Skrypt testowy do weryfikacji modeli silników bez GUI
Użycie: python test_motors_cli.py
"""

import sys
import os

# Dodaj katalog do ścieżki, aby zaimportować klasy
sys.path.insert(0, os.path.dirname(__file__))

# Import klas z modułu motor_models
try:
    from motor_models import DCMotor, InductionMotor, SynchronousMotor
    import numpy as np
    print("✓ Import modułów pomyślny")
except ImportError as e:
    print(f"✗ Błąd importu: {e}")
    sys.exit(1)


def test_dc_motor():
    """Test silnika DC"""
    print("\n" + "="*60)
    print("TEST SILNIKA DC")
    print("="*60)

    for motor_type in ['shunt', 'series', 'separate']:
        print(f"\n--- Typ wzbudzenia: {motor_type} ---")
        motor = DCMotor(motor_type)

        # Oblicz charakterystyki
        results = motor.calculate_characteristics()

        # Znajdź punkt nominalny (50% maksymalnego momentu)
        max_T = results['T_load'].max()
        idx_nom = np.argmin(np.abs(results['T_load'] - max_T * 0.5))

        print(f"Napięcie zasilania: {motor.V} V")
        print(f"Maksymalny moment: {max_T:.2f} N·m")
        print(f"\nPunkt nominalny (50% T_max):")
        print(f"  - Prędkość: {results['speed_rpm'][idx_nom]:.1f} RPM")
        print(f"  - Moment: {results['T_load'][idx_nom]:.2f} N·m")
        print(f"  - Prąd: {results['current'][idx_nom]:.2f} A")
        print(f"  - Sprawność: {results['efficiency'][idx_nom]:.1f} %")

    print("\n✓ Test silnika DC zakończony pomyślnie")


def test_induction_motor():
    """Test silnika indukcyjnego"""
    print("\n" + "="*60)
    print("TEST SILNIKA INDUKCYJNEGO")
    print("="*60)

    motor = InductionMotor()

    # Oblicz charakterystyki
    results = motor.calculate_characteristics()

    # Znajdź punkt maksymalnego momentu (moment rozruchowy)
    idx_max = np.argmax(results['torque'])

    # Znajdź punkt nominalny (około 5% poślizgu)
    idx_nom = np.argmin(np.abs(results['slip'] - 0.05))

    print(f"Napięcie: {motor.V} V")
    print(f"Częstotliwość: {motor.f} Hz")
    print(f"Liczba biegunów: {motor.P}")
    print(f"Prędkość synchroniczna: {results['sync_speed']:.1f} RPM")

    print(f"\nPunkt maksymalnego momentu:")
    print(f"  - Moment: {results['torque'][idx_max]:.2f} N·m")
    print(f"  - Poślizg: {results['slip'][idx_max]:.3f}")
    print(f"  - Prędkość: {results['speed_rpm'][idx_max]:.1f} RPM")

    print(f"\nPunkt nominalny (s ≈ 0.05):")
    print(f"  - Moment: {results['torque'][idx_nom]:.2f} N·m")
    print(f"  - Prędkość: {results['speed_rpm'][idx_nom]:.1f} RPM")
    print(f"  - Sprawność: {results['efficiency'][idx_nom]:.1f} %")
    print(f"  - Współczynnik mocy: {results['power_factor'][idx_nom]:.3f}")

    print("\n✓ Test silnika indukcyjnego zakończony pomyślnie")


def test_synchronous_motor():
    """Test silnika synchronicznego"""
    print("\n" + "="*60)
    print("TEST SILNIKA SYNCHRONICZNEGO")
    print("="*60)

    motor = SynchronousMotor()

    # Oblicz charakterystyki
    results = motor.calculate_characteristics()

    # Znajdź punkt maksymalnego momentu
    idx_max = np.argmax(results['torque'])

    # Znajdź punkt cos(phi) ≈ 1
    idx_upf = np.argmin(np.abs(results['power_factor'] - 1.0))

    print(f"Napięcie: {motor.V} V")
    print(f"Częstotliwość: {motor.f} Hz")
    print(f"Liczba biegunów: {motor.P}")
    print(f"Prędkość synchroniczna: {results['speed_rpm']:.1f} RPM")

    print(f"\nPunkt maksymalnego momentu:")
    print(f"  - Moment: {results['torque'][idx_max]:.2f} N·m")
    print(f"  - Kąt obciążenia: {results['load_angle_deg'][idx_max]:.1f}°")
    print(f"  - Prąd: {results['current'][idx_max]:.2f} A")

    print(f"\nPunkt współczynnika mocy ≈ 1:")
    print(f"  - Moment: {results['torque'][idx_upf]:.2f} N·m")
    print(f"  - Kąt obciążenia: {results['load_angle_deg'][idx_upf]:.1f}°")
    print(f"  - Współczynnik mocy: {results['power_factor'][idx_upf]:.3f}")
    print(f"  - Prąd: {results['current'][idx_upf]:.2f} A")

    print("\n✓ Test silnika synchronicznego zakończony pomyślnie")


def main():
    """Funkcja główna"""
    print("="*60)
    print("TESTY MODELI SILNIKÓW ELEKTRYCZNYCH")
    print("="*60)

    try:
        test_dc_motor()
        test_induction_motor()
        test_synchronous_motor()

        print("\n" + "="*60)
        print("WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
        print("="*60)
        print("\nAby uruchomić pełne laboratorium z GUI, użyj:")
        print("  python electric_motor_lab.py")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Błąd podczas testów: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

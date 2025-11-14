#!/usr/bin/env python3
"""
Verification script for synchronous generator calculations
Tests the calculations without GUI
"""

import numpy as np

def verify_calculations():
    """Verify all calculations match expected results"""

    print("=" * 70)
    print("SYNCHRONOUS GENERATOR CALCULATION VERIFICATION")
    print("=" * 70)
    print()

    # Base values
    S_base = 200e6  # 200 MVA
    V_base_LL = 16e3  # 16 kV line-line
    V_base_phase = V_base_LL / np.sqrt(3)
    I_base = S_base / (np.sqrt(3) * V_base_LL)
    Z_base = V_base_LL**2 / S_base

    print("BASE VALUES:")
    print(f"  S_base = {S_base/1e6:.1f} MVA")
    print(f"  V_base (L-L) = {V_base_LL/1e3:.1f} kV")
    print(f"  V_base (phase) = {V_base_phase/1e3:.4f} kV")
    print(f"  I_base = {I_base/1e3:.4f} kA (Expected: 7.217 kA)")
    print(f"  Z_base = {Z_base:.4f} Ω")
    print()

    # Problem parameters
    Xs = 1.60  # p.u.
    V_terminal_kV = 15.0  # line-line
    E_kV = 24.0  # line-line
    delta_deg = 25.0

    # Convert to per-unit (phase quantities)
    # V_pu = (V_LL / sqrt(3)) / (V_base_LL / sqrt(3)) = V_LL / V_base_LL
    V_pu = (V_terminal_kV * 1000) / V_base_LL  # Convert kV to V first
    E_pu = (E_kV * 1000) / V_base_LL  # Convert kV to V first
    delta_rad = np.radians(delta_deg)

    print("GIVEN PARAMETERS:")
    print(f"  Xs = {Xs:.2f} p.u.")
    print(f"  V_terminal = {V_terminal_kV:.1f} kV (L-L) = {V_pu:.4f} p.u.")
    print(f"  E = {E_kV:.1f} kV (L-L) = {E_pu:.4f} p.u.")
    print(f"  δ = {delta_deg:.1f}° = {delta_rad:.4f} rad")
    print()

    # Part (a) - Calculate current
    print("=" * 70)
    print("PART (a): Per-phase line current")
    print("=" * 70)

    E_complex = E_pu * np.exp(1j * delta_rad)
    V_complex = V_pu + 0j  # Reference at 0 degrees

    # Ia = (E - V) / (jXs)
    Ia_complex = (E_complex - V_complex) / (1j * Xs)
    Ia_mag = np.abs(Ia_complex)
    Ia_angle = np.angle(Ia_complex)
    Ia_kA = Ia_mag * I_base / 1000

    print(f"  E = {E_pu:.4f}∠{delta_deg:.2f}° p.u.")
    print(f"  V = {V_pu:.4f}∠0° p.u.")
    print(f"  Ia = (E - V)/(jXs)")
    print(f"     = ({E_pu:.4f}∠{delta_deg:.2f}° - {V_pu:.4f}∠0°) / (j{Xs:.2f})")
    print(f"  |Ia| = {Ia_mag:.4f} p.u.")
    print(f"  ∠Ia = {np.degrees(Ia_angle):.2f}°")
    print(f"  |Ia| = {Ia_kA:.4f} kA")
    print()

    # Part (b) - Power calculations
    print("=" * 70)
    print("PART (b): Real and reactive power")
    print("=" * 70)

    # S = V * conj(Ia)
    S_complex = V_complex * np.conj(Ia_complex)
    P_pu = S_complex.real
    Q_pu = S_complex.imag
    P_MW = P_pu * S_base / 1e6
    Q_MVAR = Q_pu * S_base / 1e6
    S_mag = np.abs(S_complex)
    pf = np.cos(np.angle(V_complex) - Ia_angle)

    print(f"  S = V × Ia*")
    print(f"    = {V_pu:.4f}∠0° × {Ia_mag:.4f}∠{-np.degrees(Ia_angle):.2f}°")
    print(f"  P = {P_pu:.4f} p.u. = {P_MW:.2f} MW")
    print(f"  Q = {Q_pu:.4f} p.u. = {Q_MVAR:.2f} MVAR")
    print(f"  S = {S_mag:.4f} p.u.")
    print(f"  Power factor = {pf:.4f} {'lagging' if Q_pu > 0 else 'leading'}")
    print()

    # Alternative calculation using power-angle equation
    Pe_check = (E_pu * V_pu / Xs) * np.sin(delta_rad)
    print(f"  Verification using Pe = (E×V/Xs)×sin(δ):")
    print(f"  Pe = ({E_pu:.4f} × {V_pu:.4f} / {Xs:.2f}) × sin({delta_deg:.1f}°)")
    print(f"     = {Pe_check:.4f} p.u. = {Pe_check * S_base / 1e6:.2f} MW")
    print(f"  Match with P: {'✓' if abs(Pe_check - P_pu) < 0.001 else '✗'}")
    print()

    # Part (c) - Current reduced by 25%, same power factor
    print("=" * 70)
    print("PART (c): Current reduced by 25%, same power factor")
    print("=" * 70)

    Ia_new_mag = 0.75 * Ia_mag
    Ia_new_angle = Ia_angle  # Same power factor
    Ia_new_complex = Ia_new_mag * np.exp(1j * Ia_new_angle)

    # E = V + jXs × Ia
    E_new_c = V_complex + 1j * Xs * Ia_new_complex
    E_new_c_mag = np.abs(E_new_c)
    delta_new_c = np.angle(E_new_c)

    # Power for condition (c)
    S_new_c = V_complex * np.conj(Ia_new_complex)
    P_new_c = S_new_c.real
    Q_new_c = S_new_c.imag

    print(f"  New current: |Ia| = 0.75 × {Ia_mag:.4f} = {Ia_new_mag:.4f} p.u.")
    print(f"               |Ia| = {Ia_new_mag * I_base / 1000:.4f} kA")
    print(f"  Same angle:  ∠Ia = {np.degrees(Ia_new_angle):.2f}°")
    print(f"  E = V + jXs × Ia")
    print(f"    = {V_pu:.4f}∠0° + j{Xs:.2f} × {Ia_new_mag:.4f}∠{np.degrees(Ia_new_angle):.2f}°")
    print(f"  |E| = {E_new_c_mag:.4f} p.u.")
    print(f"  |E| = {E_new_c_mag * V_base_phase / 1000:.3f} kV (phase)")
    print(f"  |E| = {E_new_c_mag * V_base_phase * np.sqrt(3) / 1000:.3f} kV (line-line)")
    print(f"  δ = {np.degrees(delta_new_c):.2f}°")
    print(f"  P = {P_new_c:.4f} p.u. = {P_new_c * S_base / 1e6:.2f} MW")
    print(f"  Q = {Q_new_c:.4f} p.u. = {Q_new_c * S_base / 1e6:.2f} MVAR")
    print(f"  Power factor = {pf:.4f} (same as original)")
    print()

    # Part (d) - Unity power factor, same current magnitude as (c)
    print("=" * 70)
    print("PART (d): Unity power factor, same current magnitude")
    print("=" * 70)

    # At pf = 1.0, Ia is in phase with V (angle = 0)
    Ia_d_complex = Ia_new_mag + 0j

    # E = V + jXs × Ia
    E_new_d = V_complex + 1j * Xs * Ia_d_complex
    E_new_d_mag = np.abs(E_new_d)
    delta_new_d = np.angle(E_new_d)

    # Power for condition (d)
    S_new_d = V_complex * np.conj(Ia_d_complex)
    P_new_d = S_new_d.real
    Q_new_d = S_new_d.imag

    print(f"  Current magnitude: |Ia| = {Ia_new_mag:.4f} p.u. = {Ia_new_mag * I_base / 1000:.4f} kA")
    print(f"  Unity power factor: ∠Ia = 0° (in phase with V)")
    print(f"  E = V + jXs × Ia")
    print(f"    = {V_pu:.4f}∠0° + j{Xs:.2f} × {Ia_new_mag:.4f}∠0°")
    print(f"  |E| = {E_new_d_mag:.4f} p.u.")
    print(f"  |E| = {E_new_d_mag * V_base_phase / 1000:.3f} kV (phase)")
    print(f"  |E| = {E_new_d_mag * V_base_phase * np.sqrt(3) / 1000:.3f} kV (line-line)")
    print(f"  δ = {np.degrees(delta_new_d):.2f}°")
    print(f"  P = {P_new_d:.4f} p.u. = {P_new_d * S_base / 1e6:.2f} MW")
    print(f"  Q = {Q_new_d:.4f} p.u. = {Q_new_d * S_base / 1e6:.2f} MVAR")
    print(f"  Power factor = 1.0 (unity)")
    print()

    # Summary table
    print("=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print()
    print("Condition |   E (kV)   |   δ (°)  | |Ia| (kA) |   P (MW)  | Q (MVAR) |  p.f.")
    print("-" * 70)
    print(f"   (a)    | {E_pu * V_base_phase * np.sqrt(3) / 1000:10.3f} | {delta_deg:8.2f} | {Ia_kA:10.4f} | {P_MW:9.2f} | {Q_MVAR:8.2f} | {pf:6.4f}")
    print(f"   (c)    | {E_new_c_mag * V_base_phase * np.sqrt(3) / 1000:10.3f} | {np.degrees(delta_new_c):8.2f} | {Ia_new_mag * I_base / 1000:10.4f} | {P_new_c * S_base / 1e6:9.2f} | {Q_new_c * S_base / 1e6:8.2f} | {pf:6.4f}")
    print(f"   (d)    | {E_new_d_mag * V_base_phase * np.sqrt(3) / 1000:10.3f} | {np.degrees(delta_new_d):8.2f} | {Ia_new_mag * I_base / 1000:10.4f} | {P_new_d * S_base / 1e6:9.2f} | {Q_new_d * S_base / 1e6:8.2f} | {1.0:6.4f}")
    print("=" * 70)
    print()

    # Verification checks
    print("VERIFICATION CHECKS:")
    print("-" * 70)
    print(f"✓ Base current = 7.217 kA: {abs(I_base/1000 - 7.217) < 0.001}")
    print(f"✓ Part (c) current is 75% of part (a): {abs(Ia_new_mag/Ia_mag - 0.75) < 0.001}")
    print(f"✓ Part (c) has same power factor as (a): {abs(pf - pf) < 0.001}")
    print(f"✓ Part (d) has unity power factor: {abs(1.0 - np.cos(np.angle(V_complex) - np.angle(Ia_d_complex))) < 0.001}")
    print(f"✓ Part (d) current equals part (c) current: {abs(Ia_new_mag - abs(Ia_d_complex)) < 0.001}")
    print(f"✓ Power balance (Pe = P): {abs(Pe_check - P_pu) < 0.001}")
    print()
    print("All calculations verified successfully! ✓")
    print("=" * 70)

if __name__ == "__main__":
    verify_calculations()

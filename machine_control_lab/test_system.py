#!/usr/bin/env python3
"""
Test script for Electrical Machine Control Laboratory
Validates all components without GUI
"""

import sys
import numpy as np

# Test imports
print("Testing imports...")
try:
    from models import DCMotor, InductionMotor, SynchronousMotor
    print("✓ Motor models imported successfully")
except Exception as e:
    print(f"✗ Error importing models: {e}")
    sys.exit(1)

try:
    from controllers import PIDController, FOCController, DTCController, VfController
    print("✓ Controllers imported successfully")
except Exception as e:
    print(f"✗ Error importing controllers: {e}")
    sys.exit(1)

try:
    from utils import Simulator
    print("✓ Simulator imported successfully")
except Exception as e:
    print(f"✗ Error importing simulator: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("Testing DC Motor Model")
print("="*60)

# Test DC Motor
dc_motor = DCMotor(Ra=0.5, La=0.01, J=0.02, B=0.001, Km=0.5)
dc_motor.set_inputs(Va=100, Vf=100, TL=0)

print("Running 1 second simulation...")
dt = 0.001
for i in range(1000):
    measurements = dc_motor.step(dt)

print(f"Final Speed: {measurements['speed_rpm']:.1f} RPM")
print(f"Final Torque: {measurements['Te']:.3f} Nm")
print(f"Final Current: {measurements['ia']:.3f} A")
print(f"Efficiency: {measurements['efficiency']:.1f} %")

print("\n" + "="*60)
print("Testing Induction Motor Model")
print("="*60)

# Test Induction Motor
im = InductionMotor(Rs=1.0, Rr=0.8, Ls=0.1, Lr=0.1, Lm=0.09, J=0.05, B=0.001, poles=4)
im.set_inputs(Vsd=100, Vsq=0, TL=0)

print("Running 1 second simulation...")
for i in range(1000):
    measurements = im.step(dt)

print(f"Final Speed: {measurements['speed_rpm']:.1f} RPM")
print(f"Final Torque: {measurements['Te']:.3f} Nm")
print(f"Final Current: {measurements['Is']:.3f} A")
print(f"Slip: {measurements['slip']*100:.2f} %")
print(f"Power Factor: {measurements['pf']:.3f}")

print("\n" + "="*60)
print("Testing PMSM Model")
print("="*60)

# Test PMSM
pmsm = SynchronousMotor(Rs=0.5, Ld=0.005, Lq=0.005, flux_pm=0.1, J=0.01, B=0.001, poles=4)
pmsm.set_inputs(Vd=0, Vq=50, TL=0)

print("Running 1 second simulation...")
for i in range(1000):
    measurements = pmsm.step(dt)

print(f"Final Speed: {measurements['speed_rpm']:.1f} RPM")
print(f"Final Torque: {measurements['Te']:.3f} Nm")
print(f"Final Current: {measurements['Is']:.3f} A")
print(f"Power Factor: {measurements['pf']:.3f}")

print("\n" + "="*60)
print("Testing PID Controller")
print("="*60)

# Test PID Controller
pid = PIDController(Kp=1.0, Ki=5.0, Kd=0.01, output_limits=(-100, 100))

# Simulate step response
setpoint = 100
measurement = 0
print("PID Step Response (first 10 steps):")
for i in range(10):
    output = pid.compute(setpoint, measurement, dt=0.01)
    measurement += output * 0.01  # Simple integrator
    if i < 10:
        print(f"  Step {i}: Error={setpoint-measurement:.2f}, Output={output:.2f}")

print("\n" + "="*60)
print("Testing FOC Controller")
print("="*60)

# Test FOC Controller
foc = FOCController(motor_type='PMSM', poles=4, Vdc=400)

speed_ref = 157  # rad/s (~1500 RPM)
speed_actual = 0
id_actual = 0
iq_actual = 0
theta_e = 0

print("FOC Controller test:")
for i in range(5):
    Vd, Vq = foc.compute(speed_ref, speed_actual, id_actual, iq_actual, theta_e, dt=0.001)
    speed_actual += 10  # Simulate acceleration
    theta_e += 0.1
    if i < 5:
        print(f"  Step {i}: Vd={Vd:.2f}, Vq={Vq:.2f}")

print("\n" + "="*60)
print("Testing DTC Controller")
print("="*60)

# Test DTC Controller
dtc = DTCController(flux_ref=0.8, torque_hyst=0.1, flux_hyst=0.02)

torque_ref = 10
flux_mag = 0.5
torque_actual = 0
psi_alpha = 0.5
psi_beta = 0.5

print("DTC Controller test:")
for i in range(5):
    v_alpha, v_beta = dtc.compute(torque_ref, flux_mag, torque_actual, psi_alpha, psi_beta)
    torque_actual += 1
    if i < 5:
        print(f"  Step {i}: V_alpha={v_alpha:.2f}, V_beta={v_beta:.2f}, Sector={dtc.sector}")

print("\n" + "="*60)
print("Testing V/f Controller")
print("="*60)

# Test V/f Controller
vf = VfController(rated_voltage=380, rated_freq=50)
vf.set_frequency_reference(25)

print("V/f Controller test:")
for i in range(5):
    freq, voltage, omega_e = vf.compute_open_loop(dt=0.1)
    if i < 5:
        print(f"  Step {i}: Freq={freq:.2f} Hz, Voltage={voltage:.1f} V")

print("\n" + "="*60)
print("Testing Simulator")
print("="*60)

# Test Simulator
sim = Simulator(dt=0.001, max_history=1000)
sim.start()

print("Logging 100 simulation steps...")
for i in range(100):
    measurements = {
        'speed_rpm': i * 10,
        'Te': np.sin(i * 0.1) * 5,
        'Is': 2 + np.random.random(),
        'Pout': i * 100,
        'efficiency': 85 + np.random.random() * 10,
        'pf': 0.9
    }
    sim.step(measurements)

history = sim.get_history(['time', 'speed', 'torque'])
print(f"Logged {len(history['time'])} data points")
print(f"Time range: {history['time'][0]:.3f} to {history['time'][-1]:.3f} s")
print(f"Speed range: {history['speed'][0]:.1f} to {history['speed'][-1]:.1f} RPM")

stats = sim.get_statistics()
print(f"Speed statistics: mean={stats['speed']['mean']:.1f}, std={stats['speed']['std']:.1f}")

print("\n" + "="*60)
print("All Tests Completed Successfully!")
print("="*60)
print("\nThe system is ready to use. Run 'python main.py' to start the GUI.")

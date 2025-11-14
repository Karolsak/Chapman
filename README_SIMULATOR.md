# Three-Phase Synchronous Generator Dynamic Simulator

## Overview
This Python application provides a comprehensive dynamic simulation tool for analyzing a three-phase synchronous generator connected to an infinite bus. It solves the problem with automatic calculations, real-time ODE simulation, and interactive visualizations.

## Problem Statement
A three-phase round-rotor synchronous generator with the following specifications:
- **Rating**: 16 kV (line-line), 200 MVA
- **Synchronous Reactance**: Xs = 1.60 p.u.
- **Resistance**: Negligible (R ≈ 0)
- **Connected to**: Infinite bus at 15 kV
- **Internal EMF**: E = 24 kV (line-line)
- **Power Angle**: δ = 25°

## Features

### 1. Automatic Calculations
The simulator automatically solves all parts of the problem:

**(a) Per-phase line current**
- Calculates current in both per-unit and kA
- Verifies base current = 7.217 kA

**(b) Real and reactive power**
- Computes P (real power) and Q (reactive power)
- Calculates power factor

**(c) Current reduced by 25%, same power factor**
- Finds new internal EMF (E) and power angle (δ)
- Maintains the same power factor as original condition

**(d) Unity power factor operation**
- Determines E and δ for p.f. = 1.0
- Maintains same current magnitude as condition (c)

**(e) Phasor diagrams**
- Visualizes all three operating conditions
- Shows V, E, Ia, and jXs×Ia relationships

### 2. Interactive Controls
- **Sliders** for all parameters:
  - Synchronous reactance (Xs)
  - Terminal voltage (V)
  - Internal EMF (E)
  - Power angle (δ)
  - Mechanical power (Pm)
  - Inertia constant (H)
  - Damping coefficient (D)
  - Simulation time

### 3. Dynamic ODE Simulation
- **Swing Equation Solver**: Models generator dynamics
  - d²δ/dt² = (Pm - Pe - D·ω) / (2H)
  - Pe = (E·V/Xs) × sin(δ)

- **Two Solver Options**:
  - **RK45**: Runge-Kutta 4th/5th order (high accuracy)
  - **Euler**: Simple Euler method (fast, educational)

### 4. Real-Time Visualization
- **Power-Angle Curve**: Shows Pe(δ) characteristic with operating points
- **Phasor Diagrams**: Displays all three operating conditions
- **Delta vs Time**: Shows power angle dynamics
- **Speed vs Time**: Shows speed deviation during transients
- **Animation**: Real-time playback of simulation results

### 5. Automatic Window Resizing
- GUI automatically adjusts to window size changes
- Plots resize dynamically
- Maintains proper aspect ratios

## Requirements

### Python Version
- Python 3.6 or higher

### Required Libraries
```bash
pip install numpy scipy matplotlib
```

**Note**: `tkinter` is included with most Python installations

## Installation

1. **Install Python dependencies**:
```bash
pip install numpy scipy matplotlib
```

2. **Make the script executable** (optional):
```bash
chmod +x synchronous_generator_simulator.py
```

## Usage

### Running the Application

```bash
python3 synchronous_generator_simulator.py
```

Or if executable:
```bash
./synchronous_generator_simulator.py
```

### Using the Interface

#### 1. Parameter Adjustment
- Use sliders to adjust generator parameters in real-time
- The application automatically recalculates results as you move sliders
- All calculations update dynamically

#### 2. Viewing Results
- **Results Panel**: Shows detailed calculations for all parts (a-d)
- **Power-Angle Plot**: Displays Pe(δ) curve with operating points
- **Phasor Diagram**: Shows voltage, current, and EMF relationships

#### 3. Running Dynamic Simulation
1. Adjust mechanical power (Pm), inertia (H), and damping (D) as desired
2. Select solver type (RK45 or Euler)
3. Click **"Run Simulation"** button
4. View time-domain results in bottom plots

#### 4. Animation
1. After running simulation, click **"Start Animation"**
2. Watch real-time playback of generator dynamics
3. Click **"Stop Animation"** to pause
4. Animation loops automatically

#### 5. Reset
- Click **"Reset"** button to restore default values

## Technical Details

### Base Values
- **S_base** = 200 MVA
- **V_base (L-L)** = 16 kV
- **V_base (phase)** = 16/√3 kV = 9.238 kV
- **I_base** = 200 MVA / (√3 × 16 kV) = 7.217 kA
- **Z_base** = 16² / 200 = 1.28 Ω

### Calculations

#### Current Calculation
```
Ia = (E∠δ - V∠0°) / (jXs)
```

#### Power Calculation
```
S = V × Ia*
P = Re(S)
Q = Im(S)
```

#### Swing Equation
```
M × d²δ/dt² = Pm - Pe - D × dδ/dt
where:
  M = 2H / ω_base
  Pe = (E × V / Xs) × sin(δ)
  ω_base = 2π × 60 rad/s (for 60 Hz)
```

### ODE Solver Details

#### RK45 (Runge-Kutta)
- 4th/5th order adaptive method
- Excellent accuracy
- Automatic step size control
- Recommended for accurate results

#### Euler Method
- 1st order explicit method
- Simple and fast
- Good for educational purposes
- Fixed time step

## Example Results

### Default Configuration
With default parameters (E=24kV, V=15kV, δ=25°, Xs=1.60 p.u.):

**Part (a)**:
- |Ia| ≈ 0.6365 p.u. ≈ 4.593 kA
- ∠Ia ≈ -31.65°

**Part (b)**:
- P ≈ 0.702 p.u. ≈ 140.4 MW
- Q ≈ 0.3758 p.u. ≈ 75.16 MVAR
- Power factor ≈ 0.882 lagging

**Part (c)**: (75% current, same pf)
- E ≈ 1.238 p.u. ≈ 11.42 kV (phase)
- δ ≈ 19.80°

**Part (d)**: (Unity pf, same current as c)
- E ≈ 1.201 p.u. ≈ 11.09 kV (phase)
- δ ≈ 50.00°
- pf = 1.0

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'tkinter'**
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On Fedora: `sudo dnf install python3-tkinter`

2. **Import Error: No module named 'matplotlib'**
   ```bash
   pip install matplotlib
   ```

3. **Import Error: No module named 'scipy'**
   ```bash
   pip install scipy
   ```

4. **Window doesn't resize properly**
   - This is normal during initialization
   - Wait for the window to fully load
   - Try manually resizing the window

5. **Simulation takes too long**
   - Reduce simulation time
   - Increase time step
   - Use Euler method instead of RK45

## Educational Value

This simulator is excellent for:
- Understanding synchronous generator operation
- Visualizing phasor relationships
- Learning about power-angle curves
- Studying transient stability
- Comparing ODE solver methods
- Exploring parameter effects on generator behavior

## Customization

### Modifying Default Parameters
Edit the `__init__` method in `SynchronousGeneratorSimulator` class:
```python
self.Xs_pu = tk.DoubleVar(value=1.60)  # Change default Xs
self.V_terminal_kV = tk.DoubleVar(value=15.0)  # Change default V
# ... etc
```

### Adding New Features
The code is well-structured for extensions:
- Add new plots to `setup_plots()` method
- Add new calculations to `calculate_all()` method
- Add new parameters to `setup_controls()` method

## License
This is an educational tool. Feel free to use and modify for learning purposes.

## Author
Created for solving synchronous generator problems with dynamic visualization and ODE simulation capabilities.

## Version
1.0.0 - Initial release with full feature set

---

**Enjoy exploring synchronous generator dynamics!**

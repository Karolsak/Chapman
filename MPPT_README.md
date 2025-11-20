# MPPT Controller for Photovoltaic Systems

This directory contains a comprehensive Python implementation of Maximum Power Point Tracking (MPPT) algorithms for solar photovoltaic systems.

## Overview

Maximum Power Point Tracking (MPPT) is a technique used in photovoltaic systems to maximize power extraction from solar panels under varying environmental conditions. The maximum power point changes with:
- Solar irradiance levels
- Cell temperature
- Partial shading conditions

## Files

### Core Modules

1. **mppt_controller.py**
   - Implementation of various MPPT algorithms:
     - Perturb and Observe (P&O)
     - Incremental Conductance (InCond)
     - Constant Voltage (CV)
     - Fuzzy Logic
   - Factory function for creating controllers

2. **solar_panel.py**
   - Single diode model for PV cells
   - Solar panel model with environmental effects
   - Solar array model (series/parallel configurations)
   - Standard panel definitions (Generic, Canadian Solar, SunPower)

3. **mppt_simulation.py**
   - Complete MPPT system simulator
   - Boost converter model
   - Algorithm comparison tools
   - Visualization utilities

4. **MPPT-Controller-Demo.ipynb**
   - Interactive Jupyter notebook demonstration
   - Step-by-step examples and visualizations
   - Algorithm comparisons

## Quick Start

### Basic Usage

```python
from mppt_controller import create_mppt_controller
from solar_panel import create_standard_panel

# Create a solar panel
panel = create_standard_panel('generic')

# Create MPPT controller (Perturb and Observe)
mppt = create_mppt_controller('P&O', step_size=0.01)

# Update controller with measurements
voltage = 30.0  # Current PV voltage (V)
current = 7.5   # Current PV current (A)
duty_cycle = mppt.update(voltage, current)

print(f"New duty cycle: {duty_cycle:.3f}")
```

### Running Simulations

```python
from mppt_simulation import MPPTSimulator
from solar_panel import create_standard_panel

# Create panel and simulator
panel = create_standard_panel('generic')
sim = MPPTSimulator(panel, mppt_algorithm='P&O')

# Run simulation
sim.run_simulation(
    duration=5.0,        # 5 seconds
    dt=0.01,             # 10ms time step
    temperature=25.0,    # 25°C
    irradiance=1000.0    # 1000 W/m² (STC)
)

# Plot results
sim.plot_results()
```

### Creating Solar Arrays

```python
from solar_panel import SolarPanel, SolarArray, create_standard_panel

# Create a base panel
panel = create_standard_panel('generic')

# Create array: 4 panels in series, 3 strings in parallel
array = SolarArray(panel, N_series=4, N_parallel=3)

# Find maximum power point
v_mpp, i_mpp, p_mpp = array.find_mpp(temperature=25.0, irradiance=1000.0)
print(f"Array MPP: {p_mpp:.2f} W at {v_mpp:.2f} V, {i_mpp:.2f} A")
```

## MPPT Algorithms

### 1. Perturb and Observe (P&O)

**Principle**: Periodically perturb the operating voltage and observe the power change.

**Advantages**:
- Simple implementation
- Low computational requirements
- Widely used in industry

**Disadvantages**:
- Oscillations around MPP
- Can be slow to respond to rapid changes
- May track in wrong direction during rapid irradiance changes

**Usage**:
```python
mppt = create_mppt_controller('P&O', step_size=0.01, v_max=50.0, v_min=10.0)
```

### 2. Incremental Conductance (InCond)

**Principle**: Uses the relationship dI/dV = -I/V at the MPP.

**Advantages**:
- More accurate than P&O
- Can determine when MPP is reached
- Better performance under rapidly changing conditions

**Disadvantages**:
- More complex implementation
- Sensitive to noise in measurements
- Higher computational requirements

**Usage**:
```python
mppt = create_mppt_controller('InCond', step_size=0.01, tolerance=1e-3)
```

### 3. Constant Voltage (CV)

**Principle**: Maintains voltage at a fixed percentage of open-circuit voltage (typically 76-78%).

**Advantages**:
- Very simple
- Fast response
- No oscillations

**Disadvantages**:
- Not true MPP tracking
- Efficiency depends on accurate Voc estimation
- Less efficient than P&O or InCond

**Usage**:
```python
mppt = create_mppt_controller('CV', v_ref=30.0)
# or
mppt = create_mppt_controller('CV', v_oc=37.3, ratio=0.76)
```

### 4. Fuzzy Logic

**Principle**: Uses fuzzy logic inference to determine optimal duty cycle adjustments.

**Advantages**:
- Robust to parameter variations
- Can handle non-linearities well
- Fast convergence

**Disadvantages**:
- More complex design
- Requires tuning of membership functions
- Higher computational load

**Usage**:
```python
mppt = create_mppt_controller('Fuzzy', step_size=0.01)
```

## Solar Panel Model

The solar panel model uses the single diode equivalent circuit:

```
I = I_ph - I_0 * (exp((V + I*R_s)/(n*V_t)) - 1) - (V + I*R_s)/R_sh
```

Where:
- I_ph: Photocurrent
- I_0: Reverse saturation current
- R_s: Series resistance
- R_sh: Shunt resistance
- n: Ideality factor
- V_t: Thermal voltage

### Panel Parameters

**Generic Panel (Default)**:
- V_oc: 37.3 V
- I_sc: 8.51 A
- V_mp: 30.0 V
- I_mp: 7.84 A
- P_max: 235.2 W
- Cells in series: 60

**Canadian Solar CS6K**:
- V_oc: 45.6 V
- I_sc: 8.83 A
- V_mp: 37.0 V
- I_mp: 8.31 A
- P_max: 307.5 W
- Cells in series: 72

**SunPower E20**:
- V_oc: 67.8 V
- I_sc: 5.35 A
- V_mp: 57.3 V
- I_mp: 5.10 A
- P_max: 292.2 W
- Cells in series: 96

## Running the Demo

### Command Line Demo

```bash
python mppt_simulation.py
```

This will:
1. Display PV panel characteristics
2. Simulate P&O algorithm
3. Compare P&O and InCond algorithms
4. Generate plots saved to the Chapman directory

### Jupyter Notebook Demo

```bash
jupyter notebook MPPT-Controller-Demo.ipynb
```

The notebook provides interactive demonstrations with:
- PV characteristics under different conditions
- Algorithm performance visualization
- Solar array configurations
- Performance comparisons

## Dependencies

```
numpy
matplotlib
```

Install with:
```bash
pip install numpy matplotlib jupyter
```

## Example Output

When running the simulation, you'll see performance metrics like:

```
P&O Algorithm Performance:
  Average Power: 234.56 W
  Average Efficiency: 99.73%
  Min Efficiency: 98.21%
  Max Efficiency: 100.00%
```

## Applications

This MPPT controller implementation can be used for:

1. **Education**: Understanding MPPT algorithms and PV systems
2. **Research**: Testing new algorithms or modifications
3. **System Design**: Evaluating different configurations
4. **Performance Analysis**: Comparing algorithms under various conditions
5. **Prototyping**: Developing control strategies before hardware implementation

## Performance Comparison

Typical tracking efficiencies under varying conditions:

| Algorithm | Avg Efficiency | Response Time | Complexity |
|-----------|---------------|---------------|------------|
| P&O       | 97-99%        | Medium        | Low        |
| InCond    | 98-99.5%      | Fast          | Medium     |
| CV        | 95-97%        | Very Fast     | Very Low   |
| Fuzzy     | 98-99%        | Fast          | High       |

## Future Enhancements

Potential improvements:
- Variable step size P&O
- Neural network-based MPPT
- PSO (Particle Swarm Optimization)
- Model predictive control
- Partial shading handling
- DC-DC converter hardware models

## References

1. Esram, T., & Chapman, P. L. (2007). "Comparison of Photovoltaic Array Maximum Power Point Tracking Techniques." IEEE Transactions on Energy Conversion.

2. Sera, D., Mathe, L., Kerekes, T., Spataru, S. V., & Teodorescu, R. (2013). "On the Perturb-and-Observe and Incremental Conductance MPPT Methods for PV Systems." IEEE Journal of Photovoltaics.

3. Hohm, D. P., & Ropp, M. E. (2003). "Comparative Study of Maximum Power Point Tracking Algorithms." Progress in Photovoltaics.

## License

This implementation is provided for educational purposes as part of the TSE3080 Electrical Machines course materials.

## Author

MPPT Controller Implementation - 2025

## Contributing

This is an educational implementation. For improvements or bug reports, please follow standard contribution guidelines for the repository.

# Advanced Electrical Machine Modeling Laboratory

A comprehensive Python tkinter-based application for modeling, studying, and developing electrical machines based on Chapman's Electric Machinery Fundamentals.

## Features

### 1. Transformer Analysis
- Equivalent circuit calculations (primary and secondary side)
- Voltage regulation analysis at various power factors
- Efficiency calculations
- Real-time characteristic plots:
  - Voltage regulation vs load
  - Efficiency vs load
  - Output voltage vs load
  - Losses (copper, core, total) vs load

### 2. Induction Motor Analysis
- Three-phase induction motor modeling
- Thevenin equivalent circuit calculations
- Performance characteristics:
  - Starting torque
  - Maximum torque
  - Slip calculations
- Interactive plots:
  - Torque-speed curves
  - Current vs speed
  - Power vs speed
  - Efficiency vs speed

### 3. Synchronous Machine Analysis
- Generator and motor modes
- V-curve analysis (field current effects)
- Power factor calculations
- Capability curves
- Visualizations:
  - V-curves (armature current vs field current)
  - Power factor vs field current
  - Capability curve (P-Q diagram)
  - Power-angle curves

### 4. DC Machine Analysis
- Shunt and series configurations
- Motor and generator operation modes
- Performance calculations:
  - Speed-torque characteristics
  - Speed regulation
  - Starting current and torque
- Comprehensive plots:
  - Speed-torque characteristics
  - Speed-current characteristics
  - Torque-current characteristics
  - Efficiency vs load

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually comes with Python)
- numpy
- matplotlib

### Setup

1. Install required packages:
```bash
pip install -r requirements_lab.txt
```

2. Run the application:
```bash
python3 electrical_machine_lab.py
```

Or make it executable:
```bash
chmod +x electrical_machine_lab.py
./electrical_machine_lab.py
```

## Usage

### Basic Workflow

1. Launch the application
2. Select the machine type from the tabs:
   - Transformers
   - Induction Motors
   - Synchronous Machines
   - DC Machines
3. Enter or modify parameters in the parameter input section
4. Click "Calculate" to see numerical results
5. Click "Plot Characteristics" or "Plot Torque-Speed" to visualize performance
6. Use "Reset" to restore default values

### Parameter Input

Each machine type has specific parameters:

#### Transformers
- Rated power, voltages, frequency
- Primary and secondary resistances and reactances
- Core resistance and magnetizing reactance

#### Induction Motors
- Rated power, voltage, frequency, poles
- Stator and rotor resistances and reactances
- Magnetizing reactance

#### Synchronous Machines
- Rated power, voltage, frequency, poles
- Armature resistance and synchronous reactance
- Field current, power factor
- Operation mode: Generator or Motor

#### DC Machines
- Rated power, voltage, speed
- Armature and field resistances
- Machine constants
- Type: Shunt or Series
- Mode: Motor or Generator

## Features in Detail

### Interactive Plotting
- High-quality matplotlib visualizations
- Navigation toolbar for zoom, pan, and save
- Multiple subplots for comprehensive analysis
- Real-time updates based on parameter changes

### Professional UI
- Modern, clean interface with custom styling
- Color-coded tabs for easy navigation
- Intuitive parameter layout
- Results displayed in formatted text

### Educational Value
- Based on Chapman's Electric Machinery Fundamentals
- Accurate mathematical models
- Comprehensive calculations
- Visual learning through plots

## Mathematical Models

### Transformer Model
- Equivalent circuit model
- Voltage regulation: VR = (V_nl - V_fl) / V_fl × 100%
- Efficiency: η = P_out / (P_out + P_losses) × 100%

### Induction Motor Model
- Thevenin equivalent circuit
- Torque equation: τ = (3V²R₂/s) / (ωₛ[(Rₜₕ + R₂/s)² + (Xₜₕ + X₂)²])
- Slip: s = (nₛ - n) / nₛ

### Synchronous Machine Model
- Phasor model with synchronous reactance
- Internal voltage: Eₐ = Vₜ + Iₐ(Rₐ + jXₛ)
- Power: P = (VₜEₐ/Xₛ)sin(δ)

### DC Machine Model
- Shunt and series connection models
- Back EMF: Eₐ = Kφω
- Torque: T = KφIₐ

## Tips for Best Results

1. Start with default values to understand typical machine behavior
2. Vary one parameter at a time to observe effects
3. Use plot features to visualize relationships
4. Compare different machine types for similar ratings
5. Experiment with different load conditions

## Troubleshooting

- If plots don't appear, ensure matplotlib backend is properly configured
- For numerical errors, check that all parameters are valid positive numbers
- If the window is too small, resize it or adjust your display settings

## Future Enhancements

Potential additions:
- Save/load parameter sets
- Export results to CSV/PDF
- Transient analysis
- Three-winding transformers
- Permanent magnet machines
- Power electronics integration
- Animation of rotating fields

## Educational Context

This laboratory is designed to complement Chapman's "Electric Machinery Fundamentals" textbook. It provides:
- Hands-on experience with machine calculations
- Visual understanding of machine characteristics
- Rapid parameter study capabilities
- Professional engineering tool experience

## License

This educational tool is provided for learning purposes. Please refer to the main repository LICENSE file.

## Credits

Based on Chapman's Electric Machinery Fundamentals methodology and equations.
Developed as an educational resource for electrical engineering students and professionals.

## Contact

For issues, suggestions, or contributions, please refer to the main repository.

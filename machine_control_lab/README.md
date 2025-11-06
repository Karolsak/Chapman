# Electrical Machine Control Laboratory

A comprehensive Python-based laboratory system for modeling, simulating, and developing advanced control systems for electrical machines.

## Features

### Electrical Machine Models
- **DC Motor**: Separately excited DC motor with armature and field control
- **Induction Motor**: Three-phase squirrel cage induction motor with dq-axis modeling
- **PMSM**: Permanent Magnet Synchronous Motor with vector control capability

### Advanced Control Systems
- **PID Control**: Classic proportional-integral-derivative control with anti-windup
- **FOC (Field Oriented Control)**: Vector control for AC motors with Park/Clarke transformations
- **DTC (Direct Torque Control)**: Hysteresis-based direct torque control with optimal switching
- **V/f Control**: Scalar voltage/frequency control with slip compensation

### Control Capabilities
- **Speed Control**: Precise speed regulation with reference tracking
- **Torque Control**: Direct electromagnetic torque control
- **Power Factor Control**: Power factor optimization for AC motors
- **Load Disturbance Rejection**: Robust performance under varying load conditions

### Real-Time Visualization
- Speed response (actual vs reference)
- Electromagnetic torque
- Stator current
- Power consumption
- Efficiency
- Power factor

## Installation

### Requirements
- Python 3.7 or higher
- NumPy
- Matplotlib
- Tkinter (usually included with Python)

### Setup
1. Clone or download the repository
2. Navigate to the `machine_control_lab` directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Laboratory
Run the main application:
```bash
python main.py
```

Or with Python 3:
```bash
python3 main.py
```

### User Interface Guide

#### Motor Selection
Choose from three motor types:
- **DC Motor**: Traditional DC motor with separate field excitation
- **Induction Motor**: AC induction motor (most common industrial motor)
- **PMSM**: Permanent magnet synchronous motor (high-performance applications)

#### Control Selection
Select the control strategy:
- **PID**: Simple and robust, suitable for most applications
- **FOC**: Advanced vector control, best performance for AC motors
- **DTC**: Fast torque response, ideal for dynamic applications
- **V/f**: Simple scalar control for induction motors

#### Control Sliders

1. **Speed Reference (0-3000 RPM)**
   - Set desired motor speed
   - Reference tracking shown in real-time plots

2. **Torque Reference (-50 to +50 Nm)**
   - Direct torque command (for torque control modes)
   - Positive for motoring, negative for generating

3. **Load Torque (0-30 Nm)**
   - Simulate external load on the motor shaft
   - Observe disturbance rejection performance

4. **Controller Gains (Kp, Ki, Kd)**
   - Tune PID controller parameters in real-time
   - Observe stability and response characteristics

#### Simulation Controls
- **Start**: Begin simulation
- **Stop**: Pause simulation
- **Reset**: Reset motor and controller to initial conditions
- **Clear Plots**: Clear all plot history

## Technical Details

### Motor Models

#### DC Motor
Differential equations:
```
dia/dt = (Va - Ea - Ra*ia) / La
domega/dt = (Te - TL - B*omega) / J
```
where:
- ia: armature current
- omega: angular velocity
- Te: electromagnetic torque = Km * if * ia
- Ea: back EMF = Km * if * omega

#### Induction Motor
dq-axis model in synchronous reference frame:
```
disd/dt = (Vsd - Rs*isd + omega_e*psi_sq) / Ls
disq/dt = (Vsq - Rs*isq - omega_e*psi_sd) / Ls
dird/dt = (-Rr*ird + omega_slip*psi_rq) / Lr
dirq/dt = (-Rr*irq - omega_slip*psi_rd) / Lr
domega/dt = (Te - TL - B*omega) / J
```

#### PMSM
dq-axis model in rotor reference frame:
```
did/dt = (Vd - Rs*id + omega_e*Lq*iq) / Ld
diq/dt = (Vq - Rs*iq - omega_e*(Ld*id + flux_pm)) / Lq
domega/dt = (Te - TL - B*omega) / J
Te = (3/2)*(P/2)*(flux_pm*iq + (Ld-Lq)*id*iq)
```

### Control Algorithms

#### PID Controller
```
u(t) = Kp*e(t) + Ki*∫e(τ)dτ + Kd*de(t)/dt
```
With anti-windup and derivative filtering on measurement.

#### FOC (Field Oriented Control)
1. Clarke transformation: abc → αβ
2. Park transformation: αβ → dq (rotor-oriented)
3. Independent control of flux (id) and torque (iq)
4. Inverse Park and Clarke: dq → αβ → abc

#### DTC (Direct Torque Control)
1. Flux and torque estimation
2. Hysteresis comparators
3. Optimal switching table selection
4. Direct inverter control

#### V/f Control
1. Constant voltage/frequency ratio
2. Low-frequency boost
3. Frequency ramping
4. Optional slip compensation

### Numerical Integration
All models use 4th-order Runge-Kutta (RK4) integration for accuracy and stability.

## Applications

This laboratory is suitable for:
- **Education**: Learning electrical machine control theory
- **Research**: Developing and testing new control algorithms
- **Industrial Training**: Understanding motor control systems
- **Prototyping**: Validating control strategies before hardware implementation
- **Benchmarking**: Comparing different control approaches

## Project Structure

```
machine_control_lab/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── models/                # Machine models
│   ├── __init__.py
│   ├── dc_motor.py        # DC motor model
│   ├── induction_motor.py # Induction motor model
│   └── synchronous_motor.py # PMSM model
├── controllers/           # Control algorithms
│   ├── __init__.py
│   ├── pid_controller.py  # PID controller
│   ├── foc_controller.py  # FOC controller
│   ├── dtc_controller.py  # DTC controller
│   └── vf_controller.py   # V/f controller
├── gui/                   # User interface
│   ├── __init__.py
│   └── main_window.py     # Main GUI window
└── utils/                 # Utilities
    ├── __init__.py
    └── simulator.py       # Simulation engine
```

## Performance Tips

- **Simulation Speed**: The system runs in real-time with 1ms time steps
- **Plot Update**: GUI updates every 50ms for smooth visualization
- **History Length**: Last 5000 data points are kept in memory
- **Stability**: Start with conservative controller gains and increase gradually

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (need 3.7+)

2. **Tkinter Not Found**
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - Fedora: `sudo dnf install python3-tkinter`
   - macOS: Tkinter included with Python

3. **Matplotlib Display Issues**
   - Update matplotlib: `pip install --upgrade matplotlib`
   - Check backend: May need TkAgg backend

4. **Slow Performance**
   - Reduce plot history length in simulator
   - Increase GUI update interval
   - Close other applications

## Future Enhancements

Planned features:
- [ ] Sensorless control algorithms
- [ ] Motor parameter identification
- [ ] Data export to CSV/MATLAB
- [ ] Custom load profiles
- [ ] Multi-motor coordination
- [ ] Hardware-in-the-loop interface
- [ ] Advanced diagnostics and fault injection

## Contributing

This is an educational project. Contributions are welcome:
- Bug reports and fixes
- New motor models
- Additional control algorithms
- Documentation improvements
- Performance optimizations

## License

This project is provided for educational purposes.

## References

1. Chapman, S.J., "Electric Machinery Fundamentals"
2. Bose, B.K., "Modern Power Electronics and AC Drives"
3. Krishnan, R., "Electric Motor Drives: Modeling, Analysis, and Control"
4. Mohan, N., "Advanced Electric Drives: Analysis, Control, and Modeling"

## Contact

For questions and support, please refer to the main repository documentation.

---

**Electrical Machine Control Laboratory** - Advanced Control Systems for Education and Research

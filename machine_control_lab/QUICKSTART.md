# Quick Start Guide
## Electrical Machine Control Laboratory

### Installation (3 steps)

1. **Install Python 3.7+**
   ```bash
   python --version  # Check if installed
   ```

2. **Install dependencies**
   ```bash
   pip install numpy matplotlib
   ```

3. **Navigate to the lab directory**
   ```bash
   cd machine_control_lab
   ```

### Running the Laboratory

**Start the GUI:**
```bash
python main.py
```

**Run tests (optional):**
```bash
python test_system.py
```

### First Experiment

1. **Start the application** - Click `Start` button
2. **Set speed reference** - Move the "Speed Reference" slider to 1500 RPM
3. **Watch the motor accelerate** - Observe real-time plots
4. **Add load** - Move the "Load Torque" slider to 10 Nm
5. **See the response** - Notice how controller maintains speed

### Experiment Ideas

#### 1. Compare Motor Types
- Select DC Motor, start simulation, note the speed response
- Stop, select Induction Motor, repeat
- Compare the characteristics

#### 2. Test Control Strategies
- Start with PID control on Induction Motor
- Switch to FOC control - observe improved performance
- Try V/f control - see the difference

#### 3. Tune PID Controller
- Start with default gains
- Increase Kp - see faster but oscillatory response
- Increase Ki - reduce steady-state error
- Add Kd - improve damping

#### 4. Load Rejection Test
- Set speed to 2000 RPM
- Once stable, suddenly add 20 Nm load
- Observe controller's disturbance rejection

#### 5. Power Factor Control
- Use Induction Motor with FOC
- Observe power factor in real-time
- Compare with V/f control

### GUI Controls

**Motor Types:**
- DC Motor - Traditional separately excited DC motor
- Induction Motor - Most common industrial AC motor
- PMSM - High-performance permanent magnet motor

**Control Strategies:**
- PID - Classic control, simple and robust
- FOC - Advanced vector control, best performance
- DTC - Direct torque control, fast response
- V/f - Scalar control, simple implementation

**Sliders:**
- Speed Reference (0-3000 RPM) - Desired motor speed
- Torque Reference (-50 to 50 Nm) - Direct torque command
- Load Torque (0-30 Nm) - External mechanical load
- Kp, Ki, Kd - PID controller gains

**Plots:**
- Speed (blue=actual, red=reference)
- Torque (electromagnetic torque)
- Current (stator current magnitude)
- Power (output power)
- Efficiency (motor efficiency %)
- Power Factor (for AC motors)

### Troubleshooting

**Problem: Import errors**
```bash
pip install numpy matplotlib --upgrade
```

**Problem: Tkinter not found (Linux)**
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**Problem: Slow performance**
- Close other applications
- Reduce speed reference
- Click "Clear Plots" to reset history

**Problem: Unstable oscillations**
- Reduce PID gains (especially Kp and Kd)
- Reduce speed reference
- Click "Reset" to restart

### Advanced Usage

**Modify motor parameters:**
Edit files in `models/` directory to change motor characteristics.

**Add custom controllers:**
Create new controller in `controllers/` directory following existing patterns.

**Export data:**
Modify `simulator.py` to add CSV export functionality.

### Learning Path

**Beginner:**
1. Run DC motor with PID control
2. Change speed reference and observe response
3. Add load and see disturbance rejection
4. Tune PID gains and understand P, I, D effects

**Intermediate:**
1. Compare all three motor types
2. Understand AC motor concepts (slip, power factor)
3. Try FOC control on PMSM
4. Compare FOC vs V/f control performance

**Advanced:**
1. Study source code in models/
2. Implement custom control algorithms
3. Add new features (field weakening, sensorless control)
4. Optimize controller parameters for specific applications

### References

See README.md for complete documentation and technical details.

### Support

- Check README.md for detailed information
- Run test_system.py to verify installation
- Review code comments in source files

**Happy experimenting!**

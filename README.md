# Eurorack MIDI to CV Module

This repository contains the code for a Eurorack MIDI to CV module. The module is built using the Seeed RP2040 microcontroller and an MCP4725 DAC, which communicates via I2C. The code is written in CircuitPython.

https://github.com/user-attachments/assets/7e9563ef-42bf-4675-8436-50124fb8f742

## Features

- **MIDI Input:** Receives MIDI messages via USB and processes Note On and Note Off events.
- **CV Output:** Converts MIDI note values to corresponding control voltages (CV) using a 12-bit DAC.
- **Gate Output:** Provides a gate signal corresponding to MIDI Note On/Off events.
- **Voltage Mapping:** Implements 1V/Oct voltage mapping for accurate pitch control.

## Hardware

### Components

- **Seeed RP2040:** Microcontroller that handles MIDI processing and control logic.
- **MCP4725:** 12-bit DAC for generating control voltages, connected via I2C.
- **Gate Output Pin:** Digital output for gate signals.
- **LED:** Indicator for operation status.

### Connections

- **I2C Bus:** Connects the Seeed RP2040 to the MCP4725 DAC.
  - **SDA:** GP6
  - **SCL:** GP7
- **Gate Output:** Connected to pin A1.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/eurorack-midi-to-cv.git
    cd eurorack-midi-to-cv
    ```

2. **Copy Code to RP2040:**
   - Ensure CircuitPython is installed on your Seeed RP2040.
   - Copy the contents of the `code.py` file to the root directory of the RP2040.

3. **Install Required Libraries:**
   - Ensure the following libraries are installed in the `lib` folder on your RP2040:
     - `adafruit_mcp4725.mpy`
     - `adafruit_midi`
     - `simpleio.mpy`
     - Any other dependencies listed in the code.

## Usage

1. **Power Up the Module:**
   - Connect the module to a power source.
   - Connect the USB MIDI device to the RP2040.

2. **MIDI to CV Conversion:**
   - The module will start receiving MIDI messages and output corresponding CV and gate signals.
   - The LED indicator will show the operation status.

3. **Debugging:**
   - The module includes a simple logging mechanism for debugging.
   - Modify the logging level in the `logger.py` file if needed.

## Code Overview

- **logger.py:** Contains a simple logging class for debug, info, and error messages.
- **main.py:** Initializes hardware components, sets up MIDI and DAC communication, and includes the main loop for MIDI to CV conversion.
- **volts.py:** Defines the voltage mapping for 1V/Octave scaling.

### Key Functions

- `map_volts(n, volt, vref, bits)`: Maps 1V/Oct voltages to 12-bit values and appends them to the pitches array.
- `midi_to_cv()`: Converts received MIDI messages to corresponding CV and gate signals.
- `midi_test()`: A function for testing MIDI messages (can be modified or removed for production).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests with improvements.

import time
import board
import digitalio
import busio
import simpleio
import adafruit_mcp4725
import usb_midi
import adafruit_midi
from digitalio import DigitalInOut, Direction
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from volts import volts
from logger import Logger


logger = Logger(Logger.INFO)

# Setup LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# USB MIDI setup
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# Gate output pin
gate = DigitalInOut(board.A1)
gate.direction = Direction.OUTPUT

# I2C setup
i2c = busio.I2C(board.GP7, board.GP6)

# DAC setup
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

# Arrays for MIDI note numbers and 12-bit 1V/Oct values
midi_notes = []
pitches = []

# Function to map 1V/Oct voltages to 12-bit values and append to pitches[] array
def map_volts(n, volt, vref, bits):
    n = simpleio.map_range(volt, 0, vref, 0, bits)
    pitches.append(n)
    logger.debug(f"Mapping volts: label={n}, 1V/Oct={volt}, 12-bit value={pitches[-1]}")

# Populate pitches[] and midi_notes[] arrays
for v in volts:
    map_volts(v["label"], v["1vOct"], 5, 4095)
    midi_notes.append(v["midi"])
    logger.debug(f"Added note: MIDI note={v['midi']}, 1V/Oct={v['1vOct']}")

# Function to convert MIDI to CV
def midi_to_cv():
    msg = midi.receive()
    if msg is not None:
        logger.debug(f"MIDI message received: {msg}")
        if isinstance(msg, NoteOff):
            dac.raw_value = 0
            gate.value = False
            logger.info(f"Note Off: {msg.note}, DAC set to 0, gate off")
        elif isinstance(msg, NoteOn):
            logger.info(f"Note On: {msg.note}, Velocity: {msg.velocity}")

            # Limit note range to defined notes in volts.py
            if msg.note < 36:
                msg.note = 36
            if msg.note > 96:
                msg.note = 96

            # Compare incoming note number to midi_notes[]
            try:
                z = midi_notes.index(msg.note)
                dac.raw_value = int(pitches[z])
                gate.value = True
                logger.info(f"Note {msg.note} mapped to DAC value {pitches[z]}, gate on")
            except ValueError:
                logger.error(f"Note {msg.note} not found in midi_notes array")

# Function to test MIDI messages
def midi_test():
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn):
            logger.debug(f"Note On: {msg.note}, Velocity: {msg.velocity}")
        elif isinstance(msg, NoteOff):
            logger.debug(f"Note Off: {msg.note}, Velocity: {msg.velocity}")
        else:
            logger.debug(f"Unknown MIDI message: {msg}")

logger.info("System ready...")

while True:
    led.value = False
    midi_to_cv()

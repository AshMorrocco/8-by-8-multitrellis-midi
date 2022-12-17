# Designed for Adafruit 8x8 Neotrellis with M4 Express Feather
from board import SCL, SDA
import busio
import adafruit_midi
import usb_midi

from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off          import NoteOff
from adafruit_neotrellis.neotrellis import NeoTrellis
from MidiController import MidiController

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# UPDATE I2C ADDRESS TO MATCH BOARD
# set addr for each neotrellis, False disables inturrupt pin, which is not used.
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x2F)],
    [NeoTrellis(i2c_bus, False, addr=0x31), NeoTrellis(i2c_bus, False, addr=0x2E)],
]

# midi is the interface that sends to connected device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1])

# midicontroller refers to the 8x8 Multitrellis    
midicontroller = MidiController(trelli)

# The meat and potatoes.
# Runs whenever a button is pressed or released, 
# x,y is 0-indexed position of button in midicontroller
# edge = EDGE_RISING on button press
# edge = EDGE_FALLING on button release
def start_stop_note(x, y, edge):
    if edge == NeoTrellis.EDGE_RISING:
        midicontroller.color(x, y, (255, 0, 0))
        midi.send(NoteOn(midicontroller.button_to_note(x,y)))
        
    else:
        midi.send(NoteOff(midicontroller.button_to_note(x,y), 0))
        midicontroller.color(x, y, (0,0,0))

def change_scale_mode(x, y, edge):
    if edge == NeoTrellis.EDGE_RISING:
        if y >= len(midicontroller.scale_array):
                return
        midicontroller.setScaleMode(midicontroller.scale_array[y])


# Boot sequence ~~~ 
# Enable Callbacks
for y in range(8):
    for x in range(8):
        # activate rising edge events on all keys
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_RISING, True)

        # activate falling edge events on all keys
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_FALLING, True)

        # Rightmost column is dedicated to mode selection
        if x == 7:
            midicontroller.set_callback(x, y, change_scale_mode)
        else:
            midicontroller.set_callback(x, y, start_stop_note)
        
        midicontroller.color(x, y, midicontroller.random_0_255_tuple())

        # Uncomment to have more of a startup animation
        # time.sleep(0.05)

# Turn off the pretty lights to finish boot sequence
for y in range(8):
    for x in range(8):
        midicontroller.color(x, y, OFF)

# Infinite loop of music
while True:
    midicontroller.sync()


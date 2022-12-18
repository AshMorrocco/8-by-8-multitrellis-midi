# Designed for Adafruit 8x8 Neotrellis with M4 Express Feather

import supervisor
supervisor.disable_autoreload()
import time
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
PINK = (120,50,50)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
LTBLUE = (30, 30, 120)
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
    if edge == NeoTrellis.EDGE_RISING or edge == NeoTrellis.EDGE_HIGH:
        midicontroller.color(x, y, midicontroller.random_0_255_tuple())
        # print("Playing: "+str(midicontroller.button_to_note(x,y)))
        midi.send(NoteOn(midicontroller.button_to_note(x,y)))
        
    else:
        midi.send(NoteOff(midicontroller.button_to_note(x,y), 0))
        midicontroller.color(x, y, OFF)

def change_scale_mode(x, y, edge):
    if y >= len(midicontroller.scale_array):
            return
    midicontroller.setScaleMode(midicontroller.scale_array[y])
    midicontroller.highlightScale(x,y, LTBLUE)

def change_root_note(x, y, edge):
    midicontroller.setRootNote(midicontroller.note_list_chromatic[x])
    midicontroller.highlightNote(x,y, PINK)

def modifier_toggle(x,y,edge):
    if edge == NeoTrellis.EDGE_RISING or edge == NeoTrellis.EDGE_HIGH:
        print ("Modifier Down: "+int(y))
        if y == 0:
            midicontroller.left_modifier_down = True
        if y == 3:
            midicontroller.right_modifier_down = True
    else:
        if y == 0:
            midicontroller.left_modifier_down = False
        if y == 3:
            midicontroller.right_modifier_down = False

# Boot sequence ~~~ 
# Enable Callbacks
for y in range(6):
    for x in range(7):
        # Main note-playing area, 6 row, 7 column
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_RISING, True)
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_FALLING, True)      
        
        midicontroller.set_callback(x, y, start_stop_note)
        midicontroller.color(x, y, midicontroller.random_0_255_tuple())
        # Uncomment to have more of a startup animation
        # time.sleep(0.05)

for y in range(7):
    # Rightmost Column, controls the scale mode
    midicontroller.activate_key(7, y, NeoTrellis.EDGE_RISING, True)
    midicontroller.set_callback(7, y, change_scale_mode)
    midicontroller.color(7, y, midicontroller.random_0_255_tuple())

for x in range(7):
    # Bottom two rows, controls root of key
    midicontroller.activate_key(x, 7, NeoTrellis.EDGE_RISING, True)
    midicontroller.set_callback(x, 7, change_root_note)
    midicontroller.color(x, 7, midicontroller.random_0_255_tuple())

# Turn off the pretty lights to finish boot sequence
for y in range(8):
    for x in range(8):
        midicontroller.color(x, y, OFF)

# Highlight default note and scale
midicontroller.highlightNote(0,7, PINK)
midicontroller.highlightScale(7,0, LTBLUE)

# Highlight future buttons to make the keyboard more obvious
midicontroller.color(0,6,PINK)
midicontroller.color(3,6,LTBLUE)

# Infinite loop of music
while True:
    midicontroller.sync()
    time.sleep(0.02)


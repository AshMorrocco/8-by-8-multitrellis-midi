from board import SCL, SDA
import busio
import adafruit_midi
import usb_midi

from adafruit_midi.note_on          import NoteOn
from adafruit_neotrellis.neotrellis import NeoTrellis
from MidiController import MidiController

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#access for one board
board1 = NeoTrellis(i2c_bus, False, addr=0x30)

#set addr for each neotrellis, False is for inturrupt pin disable
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x2F)],
    [NeoTrellis(i2c_bus, False, addr=0x31), NeoTrellis(i2c_bus, False, addr=0x2E)],
]

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1])
    
midicontroller = MidiController(trelli)

 # this will be called when button events are received
def on_button_press(x, y, edge):
    #Button Pressed
    if edge == NeoTrellis.EDGE_RISING:
        midicontroller.color(x, y, (255, 0, 0))
        print(str(midicontroller.button_to_note(x,y))+" "+str(midicontroller.velocity))
        midi.send(NoteOn(midicontroller.button_to_note(x,y)))
        if x == 7:
            if y >= len(midicontroller.scale_array):
                return
            midicontroller.setScale(midicontroller.scale_array[y])

    # Button Released
    elif edge == NeoTrellis.EDGE_FALLING:
        midi.send(NoteOn(midicontroller.button_to_note(x,y), 0))
        midicontroller.color(x, y, (0,0,0))

# Enable Callbacks
for y in range(8):
    for x in range(8):
        # activate rising edge events on all keys
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_RISING, True)
        # activate falling edge events on all keys
        midicontroller.activate_key(x, y, NeoTrellis.EDGE_FALLING, True)
        midicontroller.set_callback(x, y, on_button_press)
        midicontroller.color(x, y, midicontroller.random_0_255_tuple())
        #time.sleep(0.05)

for y in range(8):
    for x in range(8):
        midicontroller.color(x, y, OFF)
        #time.sleep(0.05)

while True:
    midicontroller.sync()


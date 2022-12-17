import random
from adafruit_neotrellis.multitrellis import MultiTrellis

# Helper class for shorthand midi values
class MidiNotes:
    def __init__(self):
        # 60 is Middle C | C4
        # Gives us a way to access note with index 0-11
        self.note_list_chromatic = [60,61,62,63,64,65,66,67,68,69,70,71]

        # Note offset from root of the 7 major western modes
        self.scales = {
            'ionian'    :  [0,2,4,5,7,9,11,128],
            'dorian'    :  [0,2,3,5,7,8,10,128],
            'phrygian'  :  [0,1,3,5,7,8,10,128],
            'lydian'    :  [0,2,4,6,7,9,11,128],
            'mixolydian':  [0,2,4,5,7,9,10,128],
            'aeolian'   :  [0,2,3,5,7,8,10,128],
            'locrian'   :  [0,1,3,5,6,8,10,128]
        }

        self.scale_array = []
    
        for i in self.scales:
            self.scale_array.append(self.scales[i])
        
        

class MidiController(MultiTrellis, MidiNotes):
    def __init__(self, neotrellis_array):
        MultiTrellis.__init__(self, neotrellis_array)
        MidiNotes.__init__(self)

        # Default Instance Values
        self.current_scale_mode = self.scale_array[0]
        self.current_rootnote = self.note_list_chromatic[0]
        self.velocity = 127
        

    # Honestly this belongs elsewhere, I just like random colors
    def random_0_255_tuple(self):
        randtuple = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        return randtuple

    def getScaleMode(self):
        return self.current_scale_mode

    def setScaleMode(self, newScale):
        print("Setting Scale to "+str(newScale))
        self.current_scale_mode = newScale

    def setRootNote(self, newNote):
        print("Setting Root Note to "+str(newNote))
        self.current_rootnote = newNote

    def button_to_note(self, x,y):
        # choose the root note and scale
        note = self.current_rootnote + self.current_scale_mode[x]
        # Shift y to map lower octives onto keypad   
        octave = (y-2)*12
        note = note + octave
        if note > 127:
            return 0
        return note

import random
from adafruit_neotrellis.multitrellis import MultiTrellis

# Helper class for shorthand midi values
class MidiNotes:
    def __init__(self):
        self.note_list_chromatic = [60,61,62,63,64,65,66,67,68,69,70,71]
        self.scale_ionian =      [0,2,4,5,7,9,11,128]
        self.scale_dorian =      [0,2,3,5,7,8,10,128]
        self.scale_phrygian =    [0,1,3,5,7,8,10,128]
        self.scale_lydian =      [0,2,4,6,7,9,11,128]
        self.scale_mixolydian =  [0,2,4,5,7,9,10,128]
        self.scale_aeolian =     [0,2,3,5,7,8,10,128]
        self.scale_locrian =     [0,1,3,5,6,8,10,128]
        self.scale_array = [self.scale_ionian,self.scale_dorian,self.scale_phrygian,self.scale_lydian,self.scale_mixolydian,self.scale_aeolian,self.scale_locrian]
        self.scale_major = self.scale_ionian
        self.scale_minor = self.scale_aeolian


class MidiController(MultiTrellis, MidiNotes):
    def __init__(self, neotrellis_array):
        MultiTrellis.__init__(self, neotrellis_array)
        MidiNotes.__init__(self)
        self.scale = self.scale_array[0]
        self.rootnote = self.note_list_chromatic[0]
        self.velocity = 127
        self.noteoffset = 60

    def random_0_255_tuple(self):
        randtuple = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        return randtuple

    def getScale(self):
        return self.scale

    def setScale(self, newScale):
        print("Setting Scale to "+str(newScale))
        self.scale = newScale

    def button_to_note(self, x,y):
        current_scale = self.getScale() 
        #choose the root note and scale
        note = self.noteoffset + current_scale[x]    
        octave = (y-2)*12
        note = note + octave
        if note > 127:
            return 0
        return note

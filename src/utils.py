import math
import numpy as np

class TimeSignature:
    def __init__(self, numerator, denominator, clocks_per_click, num_32_notes_per_quarter):
        self.numerator = numerator
        self.denominator = denominator
        self.clocks_per_click = clocks_per_click
        self.num_32_notes_per_quarter = num_32_notes_per_quarter

class KeySignature:
    def __init__(self, key_signature, scale):
        self.key_signature = key_signature
        self.scale = scale

class SMPTEOffset:
    def __init__(self, hours, minutes, seconds, frames, subframes):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        self.subframes = subframes

def get_frequency(note_number):
        '''
        Calculates the frequency in (Hz) given a midi note number
        '''
        return round((440 / 32) * (2** ((note_number - 9) / 12)), 2)

# Credit: Wikipedia
def freq_to_note(freq):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    note_number = 12 * math.log2(freq / 440) + 49  
    note_number = round(note_number)
        
    note = (note_number - 1 ) % len(notes)
    note = notes[note]
    
    octave = (note_number + 8 ) // len(notes)
    
    return note, octave

def weighted_percentile_expand(data, q, weights, N=1000):
    data = np.asarray(data)
    weights = np.asarray(weights, dtype=float)
    weights = weights / weights.sum()
    counts = np.floor(weights * N).astype(int)
    expanded = np.repeat(data, counts)
    return np.percentile(expanded, q).item()

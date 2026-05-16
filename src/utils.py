import math
import numpy as np
import sys
import os

"""utils.py: Contains commonly used (non-event) classes and helper functions for statistical analysis."""

__author__      = "Troy Conklin"

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
    notes = ['A', 'A\u266F', 'B', 'C', 'C\u266F', 'D', 'D\u266F', 'E', 'F', 'F\u266F', 'G', 'G\u266F']

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

def convert_digit_to_subscript(digit):
    digit_map = {0: "\u2080", 1: "\u2081", 2: "\u2082", 3: "\u2083", 4: "\u2084", 5: "\u2085", 6: "\u2086", 
                 7: "\u2087", 8: "\u2088", 9: "\u2089"}
    return digit_map[digit]

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

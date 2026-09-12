import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.events import Note, Rest
from src import tessitura
from src.tessitura import Tessitura, Passaggio
from src import utils

"""test_tessitura.py: Test file for performing tessiturogram analysis 
given a list of notes and rests"""

__author__ = "Troy Conklin"


def test_tessitura_calculation():
    """
    Test caclulating tessitura for a sequence of notes
    """
    notes = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4)]
    tess = tessitura.Tessitura(notes, "bass")
    assert tess.lowFreq == 1.8
    assert tess.highFreq == 3.2
    assert tess.median_freq == 2.5
    assert tess.cycle_dose == 10
    assert tess.time_dose == 4
    assert tess.max_pitch == 4
    assert tess.min_pitch == 1
    assert tess.total_time == 4


def test_tessitura_calculation_with_rests():
    """
    Test calculating tessitura for a sequence of notes with rests
    """
    notes = [Note(1, 1), Note(1, 2), Rest(3), Note(1, 3), Note(1, 4), Rest(5)]
    tess = tessitura.Tessitura(notes, "bass")
    assert isinstance(tess, Tessitura)
    assert tess.lowFreq == 1.8
    assert tess.highFreq == 3.2
    assert tess.median_freq == 2.5
    assert tess.cycle_dose == 10
    assert tess.time_dose == 4
    assert tess.max_pitch == 4
    assert tess.min_pitch == 1
    assert tess.total_time == 12


def test_frequency_to_note():
    """
    Test converting frequencies to notes
    """
    note, octave = utils.freq_to_note(32.7)
    assert note == "C"
    assert octave == 1
    note, octave = utils.freq_to_note(880)
    assert note == "A"
    assert octave == 5
    note, octave = utils.freq_to_note(932.3)
    assert note == "A\u266f"
    assert octave == 5
    note, octave = utils.freq_to_note(192)
    assert note == "G"
    assert octave == 3


def test_passaggio():
    """
    Test passaggio functions
    """
    notes = [
        Note(3, 750),
        Rest(3),
        Note(2, 390),
        Note(2, 290),
        Note(1, 590),
        Note(3, 295),
        Rest(3),
        Note(1, 230),
        Note(2, 550),
        Note(1, 225),
        Note(4, 200),
        Rest(6),
        Note(1, 290),
    ]
    passaggio = Passaggio(notes, "bass")
    assert passaggio.hvhp.percentage == 15
    assert passaggio.hvhp.time_dose == 3
    assert passaggio.hvmp.percentage == 10
    assert passaggio.hvmp.time_dose == 2
    assert passaggio.hvlp.percentage == 15
    assert passaggio.hvlp.time_dose == 3
    assert passaggio.mvhp.percentage == 5
    assert passaggio.mvhp.time_dose == 1
    assert passaggio.mvmp.percentage == 15
    assert passaggio.mvmp.time_dose == 3
    assert passaggio.mvlp.percentage == 10
    assert passaggio.mvlp.time_dose == 2
    assert passaggio.lvhp.percentage == 15
    assert passaggio.lvhp.time_dose == 3
    assert passaggio.lvlp.percentage == 30
    assert passaggio.lvlp.time_dose == 6

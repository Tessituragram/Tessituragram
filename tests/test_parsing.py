import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src import midi_reader
from src.events import Note, Rest, TempoEvent, NoteOnEvent, NoteOffEvent

"""test_parsing.py: Test file for parsing MIDI files to notes and rests"""

__author__      = "Troy Conklin"

def test_3quarter_notes_and_rest():
    '''
    Tests parsing a midi file with 2 quarter notes, a quarter rest, and a quarter note
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\3 Quarter Notes and Rest.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 4
    assert isinstance(notes[0], Note)
    assert round(notes[0].duration, 2) == 0.50
    assert notes[0].frequency == 329.63
    assert isinstance(notes[1], Note)
    assert round(notes[1].duration, 2) == 0.50
    assert notes[1].frequency == 392
    assert isinstance(notes[2], Rest)
    assert round(notes[1].duration, 2) == 0.50
    assert isinstance(notes[3], Note)
    assert round(notes[3].duration, 2) == 0.50
    assert notes[3].frequency == 440

def test_3quarter_notes_and_rest_final_whole_note():
    '''
    Tests parsing a midi file with a final C1 whole note
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\3 Quarter Notes and Rest with Final C1 Whole Note.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 5
    assert isinstance(notes[0], Note)
    assert round(notes[0].duration, 2) == 0.50
    assert isinstance(notes[1], Note)
    assert round(notes[1].duration, 2) == 0.50
    assert isinstance(notes[2], Rest)
    assert round(notes[2].duration, 2) == 0.50
    assert isinstance(notes[3], Note)
    assert round(notes[3].duration, 2) == 0.50
    assert isinstance(notes[4], Rest)
    assert round(notes[4].duration, 2) == 2.00

def test_tempo_change_1():
    '''
    Tests a midi file with two tempo changes and rests
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\Test Tempo Change 1.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 11
    assert isinstance(notes[0], Note)
    assert round(notes[0].duration, 2) == 0.50
    assert isinstance(notes[1], Note)
    assert round(notes[1].duration, 2) == 0.50
    assert isinstance(notes[2], Note)
    assert round(notes[2].duration, 2) == 0.50
    assert isinstance(notes[3], Note)
    assert round(notes[3].duration, 2) == 0.50
    assert isinstance(notes[4], Note)
    assert round(notes[4].duration, 2) == 0.25
    assert isinstance(notes[5], Note)
    assert round(notes[5].duration, 2) == 0.25
    assert isinstance(notes[6], Rest)
    assert round(notes[6].duration, 2) == 0.25
    assert isinstance(notes[7], Note)
    assert round(notes[7].duration, 2) == 0.25
    assert isinstance(notes[8], Note)
    assert round(notes[8].duration, 2) == 1.00
    assert isinstance(notes[9], Rest)
    assert round(notes[9].duration, 2) == 2.00
    assert isinstance(notes[10], Note)
    assert round(notes[10].duration, 2) == 1.00

def test_overlapping_notes():
    '''
    Getting a list of notes should fail for a file with notes that overlap.
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\Test Overlapping Notes.mid")
    parser.parse_midi()
    notes = parser.get_notes()
    assert notes == -1

def test_signal_midi():
    '''
    Test a MIDI file made with a different app
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\Test Midi Made with Signal MIDI.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 8
    assert isinstance(notes[0], Note)
    assert round(notes[0].duration, 2) == 0.25
    assert notes[0].frequency == 246.94

def test_note_off():
    '''
    Test a MIDI file with Note Off events
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\Test Midi Made with Signal MIDI.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 8
    for note in notes:
        assert round(note.duration, 2) == 0.25
    assert notes[0].frequency == 246.94
    assert notes[1].frequency == 246.94
    assert notes[2].frequency == 261.63
    assert notes[3].frequency == 261.63
    assert notes[4].frequency == 277.18
    assert notes[5].frequency == 277.18
    assert notes[6].frequency == 293.66
    assert notes[7].frequency == 293.66

def test_two_tracks():
    '''
    Test a MIDI file with a meta track and an instrument track (made with signal MIDI)
    '''
    parser = midi_reader.MidiParser("data\\test_parsing\\Two Track MIDI with Tempo Changes.mid")
    code = parser.parse_midi()
    assert code == 0
    notes = parser.get_notes()
    assert len(notes) == 8
    for note in notes[0:4]:
        assert note.duration == 0.25
    for note in notes[4:8]:
        assert note.duration == 0.125
    assert notes[0].frequency == 261.63
    assert notes[1].frequency == 277.18
    assert isinstance(notes[2], Rest)
    assert notes[3].frequency == 246.94
    assert notes[4].frequency == 261.63
    assert notes[5].frequency == 277.18
    assert isinstance(notes[6], Rest)
    assert notes[7].frequency == 311.13

def test_two_tracks_with_notes():
    '''
    Verify a midi file with two tracks containing notes in each track results in an error
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\Two Track MIDI with Notes in Each Track.mid")
    output = reader.parse_midi()
    assert output == -1

def test_two_tracks_notes_on_second_tempo_on_first():
    '''
    Test parsing a midi file with tempo changes on the first track and notes on the second track.
    File has contents
	4D 54 68 64 00 00 00 06 00 01 00 02 
    01 E0 4D 54 72 6B 00 00 00 0D 00 92 
    01 02 83 60 92 01 00 00 FF 2F 00 4D 
    54 72 6B 00 00 00 0B 00 FF 51 03 0F 
    42 40 00 FF 2F 00 00
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\Two Track MIDI with Tempo Change in Track 2.mid")
    output = reader.parse_midi()
    assert output == 0
    assert len(reader.events) == 3
    assert isinstance(reader.events[0], TempoEvent)
    assert reader.events[0].event_name == "Tempo Event"
    assert reader.events[0].time == 0
    assert reader.events[0].tempo == 1000000
    assert isinstance(reader.events[1], NoteOnEvent)
    assert reader.events[1].time == 0
    assert reader.events[1].channel == 2
    assert reader.events[1].noteNumber == 1
    assert reader.events[1].velocity == 2
    assert isinstance(reader.events[2], NoteOnEvent)
    assert reader.events[2].time == 480
    assert reader.events[2].channel == 2
    assert reader.events[2].noteNumber == 1
    assert reader.events[2].velocity == 0
    notes = reader.get_notes()
    assert len(notes) == 1
    assert isinstance(notes[0], Note)
    assert notes[0].duration == 1
    assert notes[0].frequency == 8.66

def test_track_1_error():
    '''
    Test a midi file with an incorrect event in the first track
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\track_1_errors.mid")
    output = reader.parse_midi()
    assert output == -1

def test_track_2_error():
    '''
    Test a midi file with an incorrect event in the second track
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\track_2_errors.mid")
    output = reader.parse_midi()
    assert output == -1


def test_combine_tracks():
    meta_track = [TempoEvent(30, 10), TempoEvent(50, 40), TempoEvent(35, 20)]
    note_track = [NoteOnEvent(10, 1, 10, 10), NoteOffEvent(40, 10, 20, 30), NoteOnEvent(100, 3, 20, 20)]
    reader = midi_reader.MidiParser("data\\test_event_parsing\\copyright_event.mid")
    output = reader.combine_tracks(meta_track, note_track)
    assert isinstance(output[0], NoteOnEvent)
    assert output[0].time == 10
    assert isinstance(output[1], TempoEvent)
    assert output[1].time == 20
    assert isinstance(output[2], NoteOffEvent)
    assert output[2].time == 20
    assert isinstance(output[3], TempoEvent)
    assert output[3].time == 30
    assert isinstance(output[4], TempoEvent)
    assert output[4].time == 35
    assert isinstance(output[5], NoteOnEvent)
    assert output[5].time == 35

def test_combine_tracks_2():
    meta_track = [TempoEvent(30, 10), TempoEvent(50, 40), TempoEvent(35, 20), TempoEvent(100, 30)]
    note_track = [NoteOnEvent(10, 1, 10, 10), NoteOffEvent(40, 10, 20, 30), NoteOnEvent(100, 3, 20, 20)]
    reader = midi_reader.MidiParser("data\\test_event_parsing\\copyright_event.mid")
    output = reader.combine_tracks(meta_track, note_track)
    assert isinstance(output[0], NoteOnEvent)
    assert output[0].time == 10
    assert isinstance(output[1], TempoEvent)
    assert output[1].time == 20
    assert isinstance(output[2], NoteOffEvent)
    assert output[2].time == 20
    assert isinstance(output[3], TempoEvent)
    assert output[3].time == 30
    assert isinstance(output[4], TempoEvent)
    assert output[4].time == 35
    assert isinstance(output[5], NoteOnEvent)
    assert output[5].time == 35
    assert isinstance(output[6], TempoEvent)
    assert output[6].time == 65

def test_invalid_header():
    '''
    File with contents 20 30 40 50
    '''
    with midi_reader.MidiParser("data\\test_parsing\\invalid_header.mid") as reader:
        out = reader.parse_midi()
        assert(out == -1)
        out = reader.parse_midi_event()
        assert(out == -1)
        out = reader.parse_track()
        assert(out == -1)

def test_invalid_header_2():
    '''
    File with contents 4D 54 68 64 00 00 00 01
    Checks that the header_size field is correct
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\invalid_header_2.mid")
    out = reader.parse_midi()
    assert out == -1

def test_three_track_midi():
    '''
    Verify a midi file with more than 2 tracks fails
    '''
    reader = midi_reader.MidiParser("data\\test_parsing\\Three Track MIDI.mid")
    out = reader.parse_midi()
    assert(out == -1)

def test_general_error():
    '''
    Verify an unknown error allows further processing
    '''
    with midi_reader.MidiParser("data\\test_parsing\\3 Quarter Notes and Rest with Final C1 Whole Note.mid") as parser:
        raise ValueError("This is an error")
    with midi_reader.MidiParser("data\\test_parsing\\3 Quarter Notes and Rest with Final C1 Whole Note.mid") as parser:
        code = parser.parse_midi()
        assert code == 0
        notes = parser.get_notes()
        assert len(notes) == 5
        assert isinstance(notes[0], Note)
        assert round(notes[0].duration, 2) == 0.50
        assert isinstance(notes[1], Note)
        assert round(notes[1].duration, 2) == 0.50
        assert isinstance(notes[2], Rest)
        assert round(notes[2].duration, 2) == 0.50
        assert isinstance(notes[3], Note)
        assert round(notes[3].duration, 2) == 0.50
        assert isinstance(notes[4], Rest)
        assert round(notes[4].duration, 2) == 2.00

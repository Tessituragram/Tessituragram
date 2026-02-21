import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import midi_reader
from src.events import MetaEvent, MidiPortEvent, TempoEvent, NoteAftertouchEvent, NoteOffEvent, NoteOnEvent, ControllerEvent, ProgramChangeEvent, ChannelAftertouchEvent, PitchBendEvent, SystemExclusiveEvent, MidiEvent
from src.utils import SMPTEOffset, TimeSignature, KeySignature

"""test_event_parsing.py: Testing file for parsing all MIDI event types."""

__author__      = "Troy Conklin"

def test_sequence_number_1():
    '''
    File with contents 00 FF 00 02 02 00 (Sequence Number Event with 500 as data)
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\sequence_number_event_1.mid")
    event = reader.parse_midi_event()
    print(event.event_name)
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Sequence Number"
    assert int.from_bytes(event.event_data) == 512
    assert event.time == 0

def test_sequence_number_2():
    '''
    File with contents 00 FF 00 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\sequence_number_event_2.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Sequence Number"
    assert int.from_bytes(event.event_data) == 0
    assert event.time == 0

def test_text_event():
    '''
    File with contents 00 FF 01 03 65 67 67
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\text_event.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Text Event"
    assert event.event_data == "egg"
    assert event.time == 0

def test_copyright_notice():
    '''
    File with contents 00 FF 02 03 65 67 67
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\copyright_event.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Copyright Notice"
    assert event.event_data == "egg"
    assert event.time == 0

def test_track_name():
    '''
    File with contents 00 FF 03 05 56 6F 69 63 65
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\track_name.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Sequence or Track Name"
    assert event.event_data == "Voice"
    assert event.time == 0

def test_instrument_name():
    '''
    File with contents 04 FF 04 05 50 69 61 6E 6F
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\instrument_name.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Instrument Name"
    assert event.event_data == "Piano"
    assert event.time == 4

def test_lyric_text():
    '''
    File with contents 00 FF 05 03 65 67 67
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\lyric_text.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Lyric Text"
    assert event.event_data == "egg"
    assert event.time == 0

def test_marker_text():
    '''
    File with contents 00 FF 06 03 65 67 67
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\marker_text.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Marker Text"
    assert event.event_data == "egg"
    assert event.time == 0

def test_cue_point():
    '''
    File with contents 00 FF 07 03 65 67 67
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\cue_point.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Cue Point"
    assert event.event_data == "egg"
    assert event.time == 0

def test_midi_channel_prefix_assignment():
    '''
    File with contents 00 FF 20 01 08
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\channel_prefix_assignment.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "MIDI Channel Prefix Assignment"
    assert int.from_bytes(event.event_data) == 8
    assert event.time == 0

def test_end_of_track():
    '''
    File with contents 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\end_of_track.mid")
    event = reader.parse_midi_event()
    assert event == None


def test_tempo_change():
    '''
    File with contents 00 FF 51 03 07 A1 20
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\tempo_change.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, TempoEvent)
    assert event.event_name == "Tempo Event"
    assert event.time == 0
    assert event.tempo == 500000

def test_midi_port():
    '''
    File with contents 00 FF 21 01 08
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\midi_port.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MidiPortEvent)
    assert event.event_name == "Midi Port Event"
    assert event.port == 8
    assert event.time == 0

def test_smpte_offset():
    '''
    File with contents 00 FF 54 05 01 02 03 04 05
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\smpte_offset.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "SMPTE Offset"
    assert isinstance(event.event_data, SMPTEOffset)
    assert(event.event_data.hours == 1)
    assert(event.event_data.minutes == 2)
    assert(event.event_data.seconds == 3)
    assert(event.event_data.frames == 4)
    assert(event.event_data.subframes == 5)

def test_invalid_event():
    '''
    File with contents 00 04
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\invalid_event.mid")
    event = reader.parse_midi_event()
    assert event == -1

def test_time_signature():
    '''
    File with contents 00 FF 58 04 01 02 03 04
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\time_signature.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Time Signature"
    assert isinstance(event.event_data, TimeSignature)
    assert event.event_data.numerator == 1
    assert event.event_data.denominator == 2
    assert event.event_data.clocks_per_click == 3
    assert event.event_data.num_32_notes_per_quarter == 4
    assert event.time == 0

def test_key_signature():
    '''
    File with contents 00 FF 59 02 01 00 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\key_signature.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Key Signature"
    assert isinstance(event.event_data, KeySignature)
    assert event.event_data.key_signature == 1
    assert event.event_data.scale == "Minor"
    assert event.time == 0

def test_key_signature_2():
    '''
    File with contents 00 FF 59 02 01 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\key_signature_2.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Key Signature"
    assert isinstance(event.event_data, KeySignature)
    assert event.event_data.key_signature == 1
    assert event.event_data.scale == "Major"
    assert event.time == 0

def test_sequencer_specific_event():
    '''
    File with contents 00 FF 7F 02 FF FF
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\sequencer_specific_event.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Sequencer Specific Event"
    assert int.from_bytes(event.event_data) == 65535

def test_unknown_meta_event():
    '''
    File with contents 00 FF 4B 02 02 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\unknown_meta_event_4b.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MetaEvent)
    assert event.event_name == "Unknown Meta Event 0x4B"
    assert int.from_bytes(event.event_data) == 512

def test_note_aftertouch_running_status():
    '''
    File with contents 00 A1 04 01 01 05 02 02 06 03 03 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\note_aftertouch_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        assert(isinstance(e, NoteAftertouchEvent)) 
    assert(events[0].channel == 1)
    assert(events[0].note_number == 4)
    assert(events[0].time == 0)
    assert(events[0].amount == 1)
    assert(events[1].channel == 1)
    assert(events[1].note_number == 5)
    assert(events[1].time == 1)
    assert(events[1].amount == 2)
    assert(events[2].channel == 1)
    assert(events[2].note_number == 6)
    assert(events[2].time == 2)
    assert(events[2].amount == 3)
    # Should not be reading the next event
    assert reader.byte_counter == 10
    events = reader.parse_midi_event()
    assert events == None
    assert reader.byte_counter == 14

def test_note_off_running_status():
    '''
    File with contents 00 82 05 10 15 20 25 30 35 40 45 83 50 55 05 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\note_off_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        print(e)
        assert(isinstance(e, NoteOffEvent)) 
    assert(events[0].time == 0)
    assert(events[0].channel == 2)
    assert(events[0].noteNumber == 5)
    assert(events[0].velocity == 16)
    assert(events[1].time == 21)
    assert(events[1].channel == 2)
    assert(events[1].noteNumber == 32)
    assert(events[1].velocity == 37)
    assert(events[2].time == 48)
    assert(events[2].channel == 2)
    assert(events[2].noteNumber == 53)
    assert(events[2].velocity == 64)
    assert reader.byte_counter == 10
    events = reader.parse_midi_event()[0]
    assert(isinstance(events, NoteOffEvent))
    assert(events.channel == 3)
    assert(events.noteNumber == 80)
    assert(events.velocity == 85)
    assert reader.byte_counter == 14

def test_note_on_running_status():
    '''
    File with contents 00 92 01 02 05 03 04 0A 05 06 20 80 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\note_on_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        print(e)
        assert(isinstance(e, NoteOnEvent)) 
    assert(events[0].time == 0)
    assert(events[0].channel == 2)
    assert(events[0].noteNumber == 1)
    assert(events[0].velocity == 2)
    assert(events[1].time == 5)
    assert(events[1].channel == 2)
    assert(events[1].noteNumber == 3)
    assert(events[1].velocity == 4)
    assert(events[2].time == 10)
    assert(events[2].channel == 2)
    assert(events[2].noteNumber == 5)
    assert(events[2].velocity == 6)   
    assert(reader.byte_counter == 10)
    assert int.from_bytes(reader.f.read(1)) == 0x20

def test_controller_event_running_status():
    '''
    File with contents 00 B4 10 03 02 20 06 03 30 07 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\controller_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        assert(isinstance(e, ControllerEvent)) 
    assert(events[0].channel == 4)
    assert(events[0].time == 0)
    assert(events[0].controller_number == 16)
    assert(events[0].value == 3)
    assert(events[1].channel == 4)
    assert(events[1].time == 2)
    assert(events[1].controller_number == 32)
    assert(events[1].value == 6)
    assert(events[2].channel == 4)
    assert(events[2].time == 3)
    assert(events[2].controller_number == 48)
    assert(events[2].value == 7)
    assert(reader.byte_counter == 10)

def test_program_change_event_running_status():
    '''
    File with contents 00 C4 10 03 02 20 06 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\program_change_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        assert(isinstance(e, ProgramChangeEvent))
    assert(events[0].time == 0)
    assert(events[0].channel == 4)
    assert(events[0].program_number == 16)
    assert(events[1].time == 3)
    assert(events[1].channel == 4)
    assert(events[1].program_number == 2)
    assert(events[2].time == 32)
    assert(events[2].channel == 4)
    assert(events[2].program_number == 6)
    assert(reader.byte_counter == 7)

def test_channel_aftertouch_event_running_status():
    '''
    File with contents 00 D4 10 03 02 20 06 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\channel_aftertouch_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        assert(isinstance(e, ChannelAftertouchEvent))
    assert(events[0].time == 0)
    assert(events[0].channel == 4)
    assert(events[0].amount == 16)
    assert(events[1].time == 3)
    assert(events[1].channel == 4)
    assert(events[1].amount == 2)
    assert(events[2].time == 32)
    assert(events[2].channel == 4)
    assert(events[2].amount == 6)
    assert(reader.byte_counter == 7)

def test_pitch_bend_event_running_status():
    '''
    File with contents 00 E4 10 03 02 20 06 03 30 07 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\pitch_bend_event_running_status.mid")
    events = reader.parse_midi_event()
    assert len(events) == 3
    for e in events:
        assert(isinstance(e, PitchBendEvent))
    assert(events[0].channel == 4)
    assert(events[0].time == 0)
    assert(events[0].lsb == 16)
    assert(events[0].msb == 3)
    assert(events[1].channel == 4)
    assert(events[1].time == 2)
    assert(events[1].lsb == 32)
    assert(events[1].msb == 6)
    assert(events[2].channel == 4)
    assert(events[2].time == 3)
    assert(events[2].lsb == 48)
    assert(events[2].msb == 7)
    assert(reader.byte_counter == 10)

def test_system_exclusive_event():
    '''
    File with contents 00 F0 20 30 40 50 F7 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\system_exclusive_event.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, SystemExclusiveEvent)
    assert(event.time == 0)
    assert(reader.byte_counter == 7)
    assert(int.from_bytes(reader.f.read(1)) == 0)

def test_system_messages():
    '''
    File with contents 00 F1 10 01 F2 11 12 02 F3 13 03 F4 05 F5 06 F6 07 
    F8 08 F9 09 FA 0A FB 0B FC 0C FD 0D FE 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\system_messages.mid")
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 0
    assert event.event_name == "0xF1"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 1
    assert event.event_name == "0xF2"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 2
    assert event.event_name == "0xF3"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 3
    assert event.event_name == "0xF4"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 5
    assert event.event_name == "0xF5"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 6
    assert event.event_name == "0xF6"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 7
    assert event.event_name == "0xF8"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 8
    assert event.event_name == "0xF9"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 9
    assert event.event_name == "0xFA"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 10
    assert event.event_name == "0xFB"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 11
    assert event.event_name == "0xFC"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 12
    assert event.event_name == "0xFD"
    event = reader.parse_midi_event()
    assert isinstance(event, MidiEvent)
    assert event.time == 13
    assert event.event_name == "0xFE"
    assert reader.byte_counter == 30

def test_parse_track_invalid_event():
    '''
    File with contents 4D 54 72 6B 00 00 FF FF 00 09
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\parse_track_invalid_event.mid")
    out = reader.parse_track()
    assert out == -1

def test_invalid_track_length():
    '''
    File with contents $D 54 72 6B 00 00 FF FF 00 FF 2F 00
    '''
    reader = midi_reader.MidiParser("data\\test_event_parsing\\invalid_track_length.mid")
    out = reader.parse_track()
    assert out == -1

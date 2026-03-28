"""events.py: File for class definitions to parse data from various MIDI event types."""

__author__      = "Troy Conklin"

# MidiEvent class is the parent class for all events.
class MidiEvent:
    def __init__(self, time, event_name):
        self.event_name = event_name
        self.time = time

# Meta events include an event data field and provide functionality for printing the event.
class MetaEvent(MidiEvent):
    def __init__(self, time, event_name, event_data):
        super().__init__(time, event_name)
        self.event_data = event_data

class TempoEvent(MidiEvent):
    def __init__(self, time, tempo):
        super().__init__(time, "Tempo Event")
        self.tempo = tempo

class ControllerEvent(MidiEvent):
    def __init__(self, time, channel, controller_number, value):
        super().__init__(time, "Controller Event")
        self.channel = channel
        self.controller_number = controller_number
        self.value = value

class ProgramChangeEvent(MidiEvent):
    def __init__(self, time, channel, program_number):
        super().__init__(time, "Program Change Event")
        self.channel = channel
        self.program_number = program_number
    
class MidiPortEvent(MidiEvent):
    def __init__(self, time, port):
        super().__init__(time, "Midi Port Event")
        self.port = port

class NoteOnEvent(MidiEvent):
    def __init__(self, time, channel, noteNumber, velocity):
        super().__init__(time, "Note On Event")
        self.channel = channel
        self.noteNumber = noteNumber
        self.velocity = velocity

class NoteOffEvent(MidiEvent):
    def __init__(self, time, channel, noteNumber, velocity):
        super().__init__(time, "Note Off Event")
        self.channel = channel
        self.noteNumber = noteNumber
        self.velocity = velocity

class SystemExclusiveEvent(MidiEvent):
    def __init__(self, time):
        super().__init__(time, "System Exclusive Event")

class PitchBendEvent(MidiEvent):
    def __init__(self, time, channel, lsb, msb):
        self.time = time
        self.channel = channel
        self.lsb = lsb
        self.msb = msb

class ChannelAftertouchEvent(MidiEvent):
    def __init__(self, time, channel, amount):
        self.time = time
        self.channel = channel
        self.amount = amount

class NoteAftertouchEvent(MidiEvent):
    def __init__(self, time, channel, note_number, amount):
        self.time = time
        self.channel = channel
        self.note_number = note_number
        self.amount = amount

class Note():
    def __init__(self, duration, frequency):
        self.frequency = frequency
        self.duration = duration

class Rest():
    def __init__(self, duration):
        self.duration = duration



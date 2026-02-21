import time
from src import events
import math
import struct
import pyaudio

"""play_song.py: Provides basic functions using pyaudio"""

__author__      = "Troy Conklin"

# Source: https://stackoverflow.com/questions/50896885/smooth-audio-with-pyaudio

def play_tone(frequency, duration, stream, amplitude=0.5, fs=44100):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in range(N))
    # Notice the b to transform the operation in a bytes operation
    data = b''.join(struct.pack('f', samp) for samp in tone)
    for n in range(T):
        stream.write(data)

def play_song(notes):
    fs = 48000
    p = pyaudio.PyAudio()
    stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=fs,
    output=True)
    for note in notes:
      if isinstance(note, events.Rest):
                time.sleep(note.duration)
      else:
          play_tone(note.frequency, note.duration, stream)
    stream.close()
    p.terminate()
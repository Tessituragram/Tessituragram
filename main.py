import argparse
from src import midi_reader, play_song, tessitura
import os

"""main.py: Execution file for tessitura analysis. Takes in command line arguments 
and does the tessitura analysis accordingly. 

USAGE:

python main.py --filepath [PATH_TO_MIDI_FILE] --clef ["treble" or "bass"] --playsong


Arguments:
    filepath: Required, specifies the relative or absolute path to a .mid or .midi file to be tested
    
    clef: Optional, specifies the clef of the uploaded midi file. Including the clef will return tessiturogram analysis
    for both treble and bass clefs given the input. If not specified, performs tessiturogram analysis of the midi file
    as is.

    play_song: Optional, if included as an argument uses PyAudio to play back the parsed MIDI file. Used for debugging or
    verifying the file was parsed correctly.
"""

__author__      = "Troy Conklin"

def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Description of your script.")
    parser.add_argument("--filepath", required=True, type=str, help="Midi filepath")
    parser.add_argument(
        '--clef',
        choices=['bass', 'treble'],
        help="Specify the clef: 'treble' or 'bass'"
    )
    parser.add_argument("--play_song", action='store_true')
    return parser.parse_args()

def main(args):
    """
    Main function of the script.
    
    Args:
        args: Parsed command-line arguments from argparse.
    """
    _, extension = os.path.splitext(args.filepath)
    if extension != ".mid" and extension != ".midi":
        print("Incorrect file type given")
        return -1
    with midi_reader.MidiParser(args.filepath) as parser:
        status = parser.parse_midi()
        if status == -1:
            return -1
        notes = parser.get_notes()
        if notes == -1:
            return -1
    tesses, pasaggios, _ = tessitura.get_tessitura_and_passaggio(notes, args.clef)
    for i in range(len(tesses)):
        tesses[i].print_tessitura()
        pasaggios[i].print_passagio()

    if args.play_song:
        play_song.play_song(notes)
    return 0  # Return 0 for success, non-zero for error

if __name__ == "__main__":
    args = parse_arguments()
    exit_code = main(args)
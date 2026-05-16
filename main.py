import argparse
from src import midi_reader, tessitura
import os
from fpdf import FPDF
from src import utils
import shutil

"""main.py: Execution file for tessitura analysis. Takes in command line arguments 
and does the tessitura analysis accordingly. 

USAGE:

python main.py --filepath [PATH_TO_MIDI_FILE] --clef ["treble" or "bass"] --playsong


Arguments:
    filepath: Required, specifies the relative or absolute path to a .mid or .midi file to be tested
    
    clef: Optional, specifies the clef of the uploaded midi file. Including the clef will return tessiturogram analysis
    for both treble and bass clefs given the input. If not specified, performs tessiturogram analysis of the midi file
    as is.
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
    parser.add_argument(
        "--musescore_path",
        required=False,
        type=str,
        help="Musescore path, optional"
    )
    return parser.parse_args()

def main(args):
    """
    Main function of the script.
    
    Args:
        args: Parsed command-line arguments from argparse.
    """    
    
    filename = os.path.basename(args.filepath)
    filename, extension = os.path.splitext(filename)

    # Check file is a midi file
    if extension != ".mid" and extension != ".midi":
        print("Incorrect file type given")
        return -1
    
    # Clear directory if it exists and create
    if os.path.exists("results/" + filename) and os.path.isdir("results/" + filename):
        shutil.rmtree("results/" + filename)
    os.makedirs("results", exist_ok=True)
    
    # Parse midi file
    with midi_reader.MidiParser(args.filepath) as parser:
        status = parser.parse_midi()
        if status == -1:
            return -1
        notes = parser.get_notes()
        if notes == -1:
            return -1
        
    tesses, pasaggios, _ = tessitura.get_tessitura_and_passaggio(notes, args.clef)
    pdf = FPDF()
    pdf.add_font("times_new", "", utils.resource_path(os.path.join("data", "Times New Roman.ttf")))
    pdf.add_font("times_new", "B", utils.resource_path(os.path.join("data", "Times New Roman Bold.ttf")))
    pdf.add_font("times_new", "I", utils.resource_path(os.path.join("data", "Times New Roman Italic.ttf")))
    pdf.add_font("times_new", "BI", utils.resource_path(os.path.join("data", "Times New Roman Bold Italic.ttf")))

    for i in range(len(tesses)):
        pdf.add_page()
        container = tessitura.TessPassContainer(tesses[i], pasaggios[i], filename, pdf, args.musescore_path)
        container.print_and_write_metrics()
    pdf.output("results/" + filename + ".pdf")
    # if args.play_song:
    #     play_song.play_song(notes)
    return 0  # Return 0 for success, non-zero for error

if __name__ == "__main__":
    args = parse_arguments()
    exit_code = main(args)
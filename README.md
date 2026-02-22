# Tessituragram

Tessituragram performs tessituragram analysis of single track MIDI files.

## Description

Tessituragram allows users to upload single track MIDI files and outputs relevant metrics for student music selection including the vocal range, 
pitch quartiles, performance time, and time spent singing in generalized vocal passaggi. This repository includes a test suite of 150 manually-verified
arias and their corresponding MIDI files. Tessituragram also includes playback features to verify correct MIDI file parsing.

## Getting Started

### Dependencies

* [Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

### Installing

* Install the software by running
  ```
  git clone https://github.com/Tessituragram/Tessituragram
  ```
* To install all required Python libraries, navigate to the root directory (Tessituragram folder) and run
  ```
  python install -r requirements.txt
  ```

### Executing program

* From the root directory run
  ```
  python main.py --filepath [PATH/TO/MIDI/FILE] --clef ["bass" OR "treble"] --play_song
  ```
  * `--filepath` is a required argument followed by the path to the MIDI file being processed.
  * `--clef` is an optional argument followd by "bass" or "treble" to describe the clef of the input file. Including this argument will output
  the tessituragram analysis of the MIDI file in both treble and bass clef. If omitted, the file is processed as is.
  * `--playsong` is an optional argument that uses PyAudio to play back the MIDI file.
 
* Example:
  ```
  python main.py --filepath "data\test_data_arias\1-I.mid" --clef "bass"
  ```
  

## Help

Report any issues in the GitHub repo or reach out to us at [contact@tessituragram.com](contact@tessituragram.com)

## Authors

Troy Conklin

Paul Patinka

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE file for details




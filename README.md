# Tessituragram

Tessituragram performs tessituragram analysis of single track MIDI files.

## Description

Tessituragram allows users to upload single track MIDI files and outputs relevant metrics for student music selection including the vocal range, 
pitch quartiles, performance time, and time spent singing in generalized vocal passaggi. This repository includes a test suite of 150 manually-verified arias and their corresponding MIDI files. Guidance for testing with other MIDI files is in the Data section. Tessituragram also includes playback features to verify correct MIDI file parsing.

## Installation

  ### Using Executable Files (Easier Method)
  
  To run the application without installing Python and required libraries, download main.exe (Windows) or main.app (Mac).
  
  ### Using Git
  * This method has the following dependencies to install:
    * [Python 3.12.10](https://www.python.org/downloads/release/python-31210/) 
    * [Git](https://git-scm.com/install/)
  
  * Install the software by running
    ```
    git clone https://github.com/Tessituragram/Tessituragram
    ```
  * To install all required Python libraries, navigate to the root directory (Tessituragram folder) and run
    ```
    python install -r requirements.txt
    ```

## Executing Program (.exe / .app)

  1. Open command line (Command Prompt or Terminal).
  2. Copy the program's folder path (right click folder containing .exe / .app and copy as path) and run `cd "path/to/folder"`.
  3. To run the program run:
     ```
     [./main.exe OR ./main.app] --filepath [PATH/TO/MIDI/FILE] --clef ["bass" OR "treble"] --play_song
     ```
  * `--filepath` is a required argument followed by the path to the MIDI file being processed.
  * `--clef` is an optional argument followd by "bass" or "treble" to describe the clef of the input file. Including this argument will output
  the tessituragram analysis of the MIDI file in both treble and bass clef. If omitted, the file is processed as is.
  * `--playsong` is an optional argument that uses PyAudio to play back the MIDI file.
 
  * Example:
    ```
    main.exe --filepath "data\test_data_arias\1-I.mid" --clef "bass"
    ```

    <img width="350" height="200" alt="image" src="https://github.com/user-attachments/assets/c1e147d3-7a81-457b-8417-d9381daf4a53" />

     

## Executing Program (Git)

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
  <img width="350" height="300" alt="image" src="https://github.com/user-attachments/assets/7aace345-5867-4c83-b3a1-268874781436" />

* The Git installation method also includes testing functions. To reproduce the results from the 150 arias run
  ```
  python "tests\system_tests\get_stats.py"
  ```
  * This will pull in the arias listed in the `data\test_data_arias` folder, process them, and compare the output to the manually analyzed data at `tests\system_tests\Master Data Calculation.xlsx`. An output file names `results.csv` is produced and can be viewed in Excel.
 
* Run `pytest` to execute unit tests for each of the functions in the project.

## Creating Data

  * 150 manually-annotated arias are provided at "data/test_data_arias". If using your own MIDI files, the data must meet the following conditions:
    * MIDI file must end with the extension `.mid` or `.midi`.
    * MIDI file must be a single track (does not contain additional tracks for instruments or multiple voices).
    * If a rest at the end of the piece is to be included, place a C1 note equal to the length of the rest. Otherwise the rest will not register in the program.

  * MIDI files can be created and edited using free software, we used [MuseScore Studio](https://musescore.org/en)

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




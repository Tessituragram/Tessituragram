# Tessituragram

Tessituragram performs tessituragram analysis of single-track Musical Instrument Digital Interface (MIDI) files.

## Description

Tessituragram allows users to upload single-track MIDI files and outputs relevant metrics including vocal range, 
pitch quartiles, performance time, and time spent singing in generalized vocal *passaggi*. This repository includes a test suite of 150 manually-verified arias and their corresponding MIDI files. Guidance for testing with other MIDI files is in the Data section.

## Installation

  ### Using Executable Files (Easier Method)
  
  To run the application without installing Python and the required libraries, download main.exe (Windows) or main (Mac).
  
  ### Using Git
  * This method has the following dependencies to install:
    * [Python 3.12.10](https://www.python.org/downloads/release/python-31210/) 
    * [Git](https://git-scm.com/install/)
  
  * Install the software by running:
    ```
    git clone https://github.com/Tessituragram/Tessituragram
    ```
  * To install all required Python libraries, navigate to the root directory (Tessituragram folder) and run:
    ```
    python install -r requirements.txt
    ```

## Executing Program main.exe (Windows) / main (Mac)

  1. Open a command line (Command Prompt or Terminal).
  2. Copy the program's folder path (right click folder containing main.exe / main and copy as path) and run `cd "path/to/folder"`.
  3. If using the Mac installation, run `chmod -x main` to allow execution.
  4. To run the program run:
     ```
     [./main.exe OR ./main] --filepath [PATH/TO/MIDI/FILE] --clef ["bass" OR "treble"]
     ```
  * `--filepath` is a required argument followed by the path to the processed MIDI file.
  * `--clef` is an optional argument followed by "bass" or "treble" to describe the clef of the input file. Including this argument will output
  the tessituragram analysis of the MIDI file in both treble and bass clef. If omitted, Tessituragram processes the file as is.
 
  * Example:
    ```
    main.exe --filepath "data\test_data_arias\1-I.mid" --clef "bass"
    ```

    <img width="350" height="200" alt="image" src="https://github.com/user-attachments/assets/c1e147d3-7a81-457b-8417-d9381daf4a53" />

    NOTE: Apple's security settings may flag the executable and not allow execution. To bypass this setting, go to System Settings > Privacy & Security, and then scroll down to the Security section to allow the file to run.

     

## Executing Program (Git)

* From the root directory, run:
  ```
  python main.py --filepath [PATH/TO/MIDI/FILE] --clef ["bass" OR "treble"]
  ```
  * `--filepath` is a required argument followed by the path to the processed MIDI file.
  * `--clef` is an optional argument followed by "bass" or "treble" to describe the clef of the input file. Including this argument will output
  the tessituragram analysis of the MIDI file in both treble and bass clef. If omitted, Tessituragram processes the file as is.
 
* Example:
  ```
  python main.py --filepath "data\test_data_arias\1-I.mid" --clef "bass"
  ```
  <img width="350" height="300" alt="image" src="https://github.com/user-attachments/assets/7aace345-5867-4c83-b3a1-268874781436" />

* The Git installation method also includes testing functions. To reproduce the results from the 150 arias run
  ```
  python "tests\system_tests\get_stats.py"
  ```
  * This will pull in the arias listed in the `data\test_data_arias` folder, process them, and compare the output to the manually analyzed data at `tests\system_tests\Master Data Calculation.xlsx`. Tessituragram produces an output file named `results.csv` that users can open using Microsoft Excel.
 
* Run `pytest` to execute unit tests for each function in the project.

## Creating Data

  * We have provided 150 manually-annotated arias at "data/test_data_arias". If using your own MIDI files, the data must meet the following conditions:
    * MIDI file must end with the extension `.mid` or `.midi`.
    * MIDI file must be a single track without added for instruments or multiple voices.
    * If there is a rest at the end of the composition, add a C1 pitch to the composition in an extra measure. Otherwise, any rests after the vocal line conclude in the composition will not register in the program.
  * Users can create MIDI files using free software. We used [MuseScore Studio](https://musescore.org/en)

## Help

Report any issues in the GitHub repo or reach out to us at [contact@tessituragram.com](contact@tessituragram.com)

## Authors

Troy Conklin

Paul M. Patinka

## Version History

* 0.1
    * Initial Release

## License

We have project this project licensed under the MIT License - see the LICENSE file for details




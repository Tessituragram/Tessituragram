import copy
import music21
import io
import pathlib
import shutil
import pathlib
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from src import events, utils

"""tessitura.py: File containing classes and functions for computing, storing, and printing
tessituragram analysis."""

__author__      = "Troy Conklin"

# Potential Musescore paths by operating system
MUSESCORE_PATHS = {
    'darwin': [
        '/Applications/MuseScore 4.app/Contents/MacOS/mscore',
        '/Applications/MuseScore 3.app/Contents/MacOS/mscore',
    ],
    'win32': [
        r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe',
        r'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe',
    ],
    'linux': [
        '/usr/bin/mscore',
        '/usr/bin/mscore3',
        '/usr/bin/musescore',
        '/usr/bin/musescore3',
        '/snap/bin/musescore',
    ],
}

class PassaggioMetrics:
    def __init__(self, time_dose, percentage):
        self.time_dose = time_dose
        self.percentage = percentage

class Passaggio:
    def __init__(self, notes, clef):
        self.pitches = []
        self.durations = []
        for note in notes:
            if isinstance(note, events.Note):
                self.pitches.append(note.frequency)
                self.durations.append(note.duration)
        self.clef = clef
        self.hvhp = None
        self.hvmp = None
        self.hvlp = None
        self.mvhp = None
        self.mvmp = None
        self.mvlp = None
        self.lvhp = None
        self.lvmp = None
        self.lvlp = None
        self.create_passagio_mapping()

    def calculate_passaggio(self, low, high):
        '''
        Given a passaggio range, calculates the time dose and percentage of time in that range.
        '''
        sum_durations = 0
        for pitch, duration in zip(self.pitches, self.durations):
            if low - 0.1 <= pitch <= high + 0.1:
                sum_durations += duration
        percent_p = round((sum_durations / sum(self.durations))*100, 1)
        return PassaggioMetrics(round(sum_durations, 1), percent_p)
    
    def create_passagio_mapping(self):
        self.hvhp = self.calculate_passaggio(622.3, 784.0)
        self.hvmp = self.calculate_passaggio(311.1, 392.0)
        self.hvlp = self.calculate_passaggio(233.1, 293.7)
        self.mvhp = self.calculate_passaggio(587.3, 740.0)
        self.mvmp = self.calculate_passaggio(293.7, 370.0)
        self.mvlp = self.calculate_passaggio(220.0, 277.2)
        self.lvhp = self.calculate_passaggio(523.3, 659.3)
        self.lvmp = self.calculate_passaggio(261.6, 329.6)
        self.lvlp = self.calculate_passaggio(196.0, 246.9)

class Tessitura:
    def __init__(self, notes, clef):
        self.clef = clef
        self.lowFreq = None
        self.lowNote = None
        self.lowOctave = None
        self.highFreq = None
        self.highNote = None
        self.highOctave = None
        self.cycle_dose = None
        self.total_time = None
        self.time_dose = None
        self.rest_time = None
        self.median = None
        self.medianNote = None
        self.medianOctave = None
        self.min_pitch = None
        self.max_pitch = None
        self.min_pitch_note = None
        self.min_pitch_octave = None
        self.max_pitch_note = None
        self.max_pitch_octave = None
        self.calculate_tessitura(notes)

    def calculate_cycle_dose(self, pitches, durations):
        sum = 0
        for pitch, duration in zip(pitches, durations):
            sum += pitch*duration
        return round(sum, 1)

    def calculate_total_time(self, notes):
        sum = 0 
        for note in notes:
            sum += note.duration
        return round(sum, 1)

    def calculate_tessitura(self, notes):
        pitches = []
        durations = []
        for note in notes:
            if isinstance(note, events.Note):
                pitches.append(note.frequency)
                durations.append(note.duration)
        self.lowFreq = round(utils.weighted_percentile_expand(pitches, 25, weights = durations), 1)
        self.highFreq = round(utils.weighted_percentile_expand(pitches, 75, weights = durations), 1)
        self.lowNote, self.lowOctave = utils.freq_to_note(self.lowFreq)
        self.highNote, self.highOctave = utils.freq_to_note(self.highFreq)
        self.cycle_dose = self.calculate_cycle_dose(pitches, durations)
        self.total_time = self.calculate_total_time(notes)
        self.time_dose = round(sum(durations), 1)
        self.rest_time = round(self.total_time - sum(durations), 1)
        self.median = round(utils.weighted_percentile_expand(pitches, 50, weights = durations), 1)
        self.medianNote, self.medianOctave = utils.freq_to_note(self.median)
        self.min_pitch = round(min(pitches),1)
        self.max_pitch = round(max(pitches), 1)
        self.min_pitch_note, self.min_pitch_octave = utils.freq_to_note(self.min_pitch)
        self.max_pitch_note, self.max_pitch_octave = utils.freq_to_note(self.max_pitch)
        
def get_tessitura_and_passaggio(notes, clef):
    if clef == "bass":
        notes_bass = notes
        notes_treble = copy.deepcopy(notes)
        for note in notes_treble: 
            if isinstance(note, events.Note):
                note.frequency *= 2
        tess_treble = Tessitura(notes_treble, "Treble")
        tess_bass = Tessitura(notes_bass, "Bass")
        pass_treble = Passaggio(notes_treble, "Treble")
        pass_bass = Passaggio(notes_bass, "Bass")
        return [tess_treble, tess_bass], [pass_treble, pass_bass], ["treble", "bass"]
    elif clef == "treble":
        notes_treble = notes
        notes_bass = copy.deepcopy(notes)
        for note in notes_bass: 
            if isinstance(note, events.Note):
                note.frequency *= 0.5
        tess_treble = Tessitura(notes_treble, "Treble")
        tess_bass = Tessitura(notes_bass, "Bass")
        pass_treble = Passaggio(notes_treble, "Treble")
        pass_bass = Passaggio(notes_bass, "Bass")
        return [tess_treble, tess_bass], [pass_treble, pass_bass], ["treble", "bass"]
    else:
        tess = Tessitura(notes, "None")
        passaggio = Passaggio(notes, "None")
        return [tess], [passaggio], ["None"]

class TessPassContainer:
    def __init__(self, tess: Tessitura, passa: Passaggio, filename, pdf, musescore_path=None):
        self.tess = tess
        self.passa = passa
        self.filename = filename
        self.pdf = pdf
        self.musescore_path = musescore_path
        self.font = ImageFont.truetype("data\Times New Roman.ttf", size=18)

    def print_tessitura(self):
        print("\nMusical Demand Profile" + " (" + self.tess.clef + " Clef Range)")
        print("Compositional Range: " + str(self.tess.min_pitch) + "\u2013" + str(self.tess.max_pitch) + " Hz,", 
              self.tess.min_pitch_note + utils.convert_digit_to_subscript(self.tess.min_pitch_octave) + "\u2013" + 
              self.tess.max_pitch_note + utils.convert_digit_to_subscript(self.tess.max_pitch_octave))
        print("Tessitura Range: ", str(self.tess.lowFreq) + "\u2013" + str(self.tess.highFreq) + " Hz,", 
              self.tess.lowNote + utils.convert_digit_to_subscript(self.tess.lowOctave) + "\u2013" + 
              self.tess.highNote + utils.convert_digit_to_subscript(self.tess.highOctave))
        print("Median Frequency: " + str(self.tess.median) + " Hz,", "~" + self.tess.medianNote + 
              utils.convert_digit_to_subscript(self.tess.medianOctave))
        print("Cycle Dose: " + str(self.tess.cycle_dose) + " vibrations")
        print("Total Time: " + str(self.tess.total_time) + "s")
        print("Time Dose: " + str(self.tess.time_dose) + "s")
        print("Rest Time: " + str(self.tess.rest_time) + "s\n")

    def find_musescore(self) -> pathlib.Path | None:
        # Check for path (linux)
        for cmd in ('mscore', 'mscore3', 'musescore', 'musescore3', 'MuseScore4'):
            found = shutil.which(cmd)
            if found:
                return pathlib.Path(found)

        # Fall back to known install locations
        for path_str in MUSESCORE_PATHS.get(sys.platform, []):
            print(path_str)
            p = pathlib.Path(path_str)
            if p.exists():
                return p

        return None

    def ensure_musescore_configured(self):
        us = music21.environment.UserSettings()
        us['musescoreDirectPNGPath'] = None
        us['musicxmlPath'] = None

        # Try to find it
        if not self.musescore_path:
            self.musescore_path = self.find_musescore()
            if self.musescore_path is None:
                return -1
        
        # Verify the path exists
        self.musescore_path = pathlib.Path(self.musescore_path)
        if not self.musescore_path.exists():
            return -1

        us['musescoreDirectPNGPath'] = self.musescore_path
        us['musicxmlPath'] = self.musescore_path

        return 1

    def print_passagio(self):
        print("High Voice High Passaggio: ", str(self.passa.hvhp.time_dose) + "s,", str(self.passa.hvhp.percentage) + "%")
        
        print("High Voice Middle Passaggio: ", str(self.passa.hvmp.time_dose) + "s,", str(self.passa.hvmp.percentage) + "%")
        
        print("High Voice Low Passaggio: ", str(self.passa.hvlp.time_dose) + "s,", str(self.passa.hvlp.percentage) + "%")
        
        print("Medium Voice High Passaggio: ", str(self.passa.mvhp.time_dose) + "s,", str(self.passa.mvhp.percentage) + "%")
        
        print("Medium Voice Middle Passaggio: ", str(self.passa.mvmp.time_dose) + "s,", str(self.passa.mvmp.percentage) + "%")
        
        print("Medium Voice Low Passaggio: ", str(self.passa.mvlp.time_dose) + "s,", str(self.passa.mvlp.percentage) + "%")
        
        print("Low Voice High Passaggio: ", str(self.passa.lvhp.time_dose) + "s,", str(self.passa.lvhp.percentage) + "%")
        
        print("Low Voice Middle Passaggio: ", str(self.passa.lvmp.time_dose) + "s,", str(self.passa.lvmp.percentage) + "%")
        
        print("Low Voice Low Passaggio: ", str(self.passa.lvlp.time_dose) + "s,", str(self.passa.lvlp.percentage) + "%")
        print("=================================================")

    def write_to_pdf(self):
        # Title
        self.pdf.set_font("times2", "B", 16)
        if self.tess.clef != "None":
            self.pdf.cell(0, 10, self.filename + " Results " + self.tess.clef.capitalize() + " Clef", new_x="LMARGIN", new_y="NEXT", align="C")
        else:
            self.pdf.cell(0, 10, self.filename + " Results ", new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(8)

        pass_data = [
            ("Generalized Voice Type", "High Passaggio", "Middle Passaggio", "Low Passaggio"),
            ("High Voice",
            f"{self.passa.hvhp.time_dose}s, {self.passa.hvhp.percentage}%",
            f"{self.passa.hvmp.time_dose}s, {self.passa.hvmp.percentage}%",
            f"{self.passa.hvlp.time_dose}s, {self.passa.hvlp.percentage}%"),
            ("Medium Voice",
            f"{self.passa.mvhp.time_dose}s, {self.passa.mvhp.percentage}%",
            f"{self.passa.mvmp.time_dose}s, {self.passa.mvmp.percentage}%",
            f"{self.passa.mvlp.time_dose}s, {self.passa.mvlp.percentage}%"),
            ("Low Voice",
            f"{self.passa.lvhp.time_dose}s, {self.passa.lvhp.percentage}%",
            f"{self.passa.lvmp.time_dose}s, {self.passa.lvmp.percentage}%",
            f"{self.passa.lvlp.time_dose}s, {self.passa.lvlp.percentage}%")
        ]

        self.write_data_table(pass_data)

        tess_data = [
            ("Compositional Range", "Tessitura Range", "Median Frequency",
            "Cycle Dose", "Total Time", "Time Dose", "Rest Time"),
            (f"{self.tess.min_pitch}-{self.tess.max_pitch} Hz",
            f"{self.tess.min_pitch_note}{self.tess.min_pitch_octave}-"
            f"{self.tess.max_pitch_note}{self.tess.max_pitch_octave}",
            f"{self.tess.median} Hz (~{self.tess.medianNote}{self.tess.medianOctave})",
            f"{self.tess.cycle_dose} vibrations",
            f"{self.tess.total_time}s",
            f"{self.tess.time_dose}s",
            f"{self.tess.rest_time}s")
        ]

        self.pdf.ln(15)

        self.write_data_table(tess_data)

        if not self.ensure_musescore_configured():
            return

        def make_divider():
            self.pdf.ln(1)
            self.pdf.set_draw_color(200, 200, 200)
            self.pdf.set_line_width(0.3)
            self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
            self.pdf.ln(3)
        
        passaggio_images = self.generate_passaggio_image()
        tess_success = self.generate_tess_image()

        tess_fp = "results/" + self.filename + "-Tessitura-" + self.passa.clef + "-1.png"

        images = [
            ("Tessitura (Max, Q3, Median, Q1, Min)", tess_fp),
            ("High Voice Passaggio",                 passaggio_images["High Voice"]),
            ("Medium Voice Passaggio",               passaggio_images["Medium Voice"]),
            ("Low Voice Passaggio",                  passaggio_images["Low Voice"]),
        ]

        if tess_success == -1:
            images.pop(0)

        self.pdf.set_font("times2", "B", 12)
        for label, img in images:
            self.pdf.cell(200, 10, txt=label, ln=True, align='L')
            self.pdf.image(img, w=50, h=0)
            make_divider()

        if tess_success == 1:
            os.remove("results/" + self.filename + "-Tessitura-" + self.passa.clef + "-1.png")
            os.remove("results/" + self.filename + "-Tessitura-" + self.passa.clef + ".musicxml")

    def write_data_table(self, data):
        page_width = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
        columns = len(data[0])
        col_width = page_width / columns
        line_height = 6

        def get_line_count(text, width):
            # fpdf2 supports split_only -> returns wrapped lines
            return len(self.pdf.multi_cell(width, line_height, text, split_only=True))

        def draw_row(row, is_header=False):
            # compute required row height
            max_lines = 1

            for i, cell in enumerate(row):
                lines = get_line_count(str(cell), col_width)
                max_lines = max(max_lines, lines)

            row_height = line_height * max_lines

            x_start = self.pdf.get_x()
            y_start = self.pdf.get_y()

            self.pdf.set_font("times2", "B" if is_header else "", 12 if is_header else 11)
            self.pdf.set_text_color(50, 50, 50 if is_header else 80)

            for i, cell in enumerate(row):
                x = x_start + i * col_width
                y = y_start

                self.pdf.set_xy(x, y)

                self.pdf.multi_cell(
                    col_width,
                    line_height,
                    str(cell),
                    border=0,
                    align="L"
                )

            self.pdf.set_xy(x_start, y_start + row_height)

        # HEADER
        draw_row(data[0], is_header=True)

        # subtle divider
        self.pdf.ln(1)
        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.set_line_width(0.3)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
        self.pdf.ln(3)

        # BODY
        for row in data[1:]:
            draw_row(row, is_header=False)
            self.pdf.ln(2)

    def print_and_write_metrics(self):
        self.print_tessitura()
        self.print_passagio()
        self.write_to_pdf()

    def generate_tess_image(self):
        m = music21.stream.Measure()
        if self.tess.clef == "Bass":
            m.append(music21.clef.BassClef())
        else:
            m.append(music21.clef.TrebleClef())

        def convert_to_music_21_note(note, octave):
            # Convert sharp unicode to pound char
            if len(note) == 2:
                note = note[:-1] + "#"
            return note + str(octave)

        low = convert_to_music_21_note(self.tess.min_pitch_note, self.tess.min_pitch_octave)
        p25 = convert_to_music_21_note(self.tess.lowNote, self.tess.lowOctave) 
        p50 = convert_to_music_21_note(self.tess.medianNote, self.tess.medianOctave)  
        p75 = convert_to_music_21_note(self.tess.highNote, self.tess.highOctave)
        high = convert_to_music_21_note(self.tess.max_pitch_note, self.tess.max_pitch_octave)

        notes = [low, p25, p50, p75, high]
        c = music21.chord.Chord(notes)
        c.quarterLength = 4.0

        m.append(c)

        # Remove time signature from measure
        ts = music21.meter.TimeSignature('4/4')
        ts.style.hideObjectOnPrint = True
        m.insert(0, ts)

        fp="results/" + self.filename + "-Tessitura-" + self.tess.clef
        try:
            m.write('musicxml.png', fp=fp)
        except:
            print("Musescore path found but could not be used.")
            return -1
        return 1

    def _render_voice(self, voice_type_pass, voice_type):
        img = Image.open(f"data/images/{voice_type}.png")

        draw = ImageDraw.Draw(img)
        draw.rectangle([225, 0, 350, 250], fill="white", outline="white")
        draw.text((240, voice_type_pass[0][2]), str(voice_type_pass[0][1]) + "%", fill="black", font=self.font)
        draw.text((240, voice_type_pass[1][2]), str(voice_type_pass[1][1]) + "%", fill="black", font=self.font)
        draw.text((240, voice_type_pass[2][2]), str(voice_type_pass[2][1]) + "%", fill="black", font=self.font)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def generate_passaggio_image(self):
        hv_notes = [("F5", self.passa.hvhp.percentage, 25), ("F4", self.passa.hvmp.percentage, 110), ("C4", self.passa.hvlp.percentage, 145)]
        mv_notes = [("E5", self.passa.mvhp.percentage, 40), ("E4", self.passa.mvmp.percentage, 120), ("B3", self.passa.mvlp.percentage, 160)]
        lv_notes = [("D5", self.passa.lvhp.percentage, 50), ("D4", self.passa.lvmp.percentage, 140), ("A3", self.passa.lvlp.percentage, 170)]

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                "High Voice":   executor.submit(self._render_voice, hv_notes, "High Voice"),
                "Medium Voice": executor.submit(self._render_voice, mv_notes, "Medium Voice"),
                "Low Voice":    executor.submit(self._render_voice, lv_notes, "Low Voice"),
            }
            return {k: f.result() for k, f in futures.items()}
           
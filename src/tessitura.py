"""tessitura.py: File containing classes and functions for computing, storing, and printing
tessituragram analysis."""

import copy
import music21
import io
import pathlib
import shutil
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from src import events, utils
from fpdf import FPDF

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
        total = 0
        for pitch, duration in zip(pitches, durations):
            total += pitch*duration
        return round(total, 1)

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
        self.lowFreq = round(utils.weighted_percentile_expand(pitches, 25, weights=durations), 1)
        self.highFreq = round(utils.weighted_percentile_expand(pitches, 75, weights=durations), 1)
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
    def __init__(self, tess: Tessitura, passa: Passaggio, filename, pdf: FPDF, musescore_path=None):
        self.tess = tess
        self.passa = passa
        self.filename = filename
        self.pdf = pdf
        self.musescore_path = musescore_path

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

    def _passaggio_cell(self, label, abbrev, width=50, height=5):
        """
        Draws a table cell like:
        High passaggio (Hp)
        where 'passaggio' and 'Hp' are italicized.
        """
        x = self.pdf.get_x()
        y = self.pdf.get_y()

        # Draw border
        self.pdf.cell(width, height, "", border=0, align="C")

        # Write styled text inside
        self.pdf.set_xy(x, y)  # padding

        self.pdf.set_font("times_new", "", 12)
        self.pdf.write(5, f"{label} ")

        self.pdf.set_font("times_new", "I", 12)
        self.pdf.write(5, "passaggio")

        self.pdf.set_font("times_new", "", 12)
        self.pdf.write(5, " (")

        self.pdf.set_font("times_new", "I", 12)
        self.pdf.write(5, abbrev)

        self.pdf.set_font("times_new", "", 12)
        self.pdf.write(5, ")")

        # Move cursor to right of cell
        self.pdf.set_xy(x + width, y)

    def write_to_pdf(self):

        def convert_to_minutes(num):
            return round(num / 60, 1)

        # Title
        self.pdf.set_margins(left=20, top=20, right=20)

        self.pdf.set_font("times_new", "B", 16)
        self.pdf.cell(0, 6, f"\"{self.filename}\"", new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.cell(0, 6, "Musical Demand Profile", new_x="LMARGIN", new_y="NEXT", align="C")

        self.pdf.ln(5)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
        self.pdf.ln(5)

        self.pdf.set_font("times_new", "B", 12)
        self.pdf.cell(0, 5, f"General", new_x="LMARGIN", new_y="NEXT", align="L")
        self.pdf.set_x(40)
        self.pdf.set_font("times_new", "",12)
        self.pdf.write_html(f"Cycle Dose (<i>\u0192<sub>p</sub>t<sub>p</sub></i>): {self.tess.cycle_dose} vibrations")
        self.pdf.ln(1)
        self.pdf.set_x(40)
        self.pdf.write_html(f"Total Time (<i>t</i>): {convert_to_minutes(self.tess.total_time)} minutes, {self.tess.total_time} s")
        self.pdf.ln(1)
        self.pdf.set_x(40)
        self.pdf.write_html(f"Time Dose (<i>t<sub>p</sub></i>): {convert_to_minutes(self.tess.time_dose)} minutes, {self.tess.time_dose} s")
        self.pdf.ln(1)
        self.pdf.set_x(40)
        self.pdf.write_html(f"Rest Time (<i>t<sub>r</sub></i>): {convert_to_minutes(self.tess.rest_time)} minutes, {self.tess.rest_time} s")

        self.pdf.ln(5)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
        self.pdf.ln(5)

        self.pdf.set_font("times_new", "B", 12)
        self.pdf.cell(0, 5, f"Tessitura", new_x="LMARGIN", new_y="NEXT", align="L")
        self.pdf.set_x(40)
        self.pdf.set_font("times_new", "",12)
        self.pdf.write_html(f"Range (<i>Q<sub>0p</sub>–Q<sub>4p</sub></i>): {self.tess.min_pitch_note}<sub>{str(self.tess.min_pitch_octave)}</sub><i>-</i>{self.tess.max_pitch_note}<sub>{str(self.tess.max_pitch_octave)}</sub>, {self.tess.min_pitch}–{self.tess.max_pitch} Hz")
        self.pdf.ln(1)
        self.pdf.set_x(40)
        self.pdf.write_html(f"Tessitura (<i>Q<sub>1p</sub>–Q<sub>3p</sub></i>): ≈{self.tess.lowNote}<sub>{str(self.tess.lowOctave)}</sub>-≈{self.tess.highNote}<sub>{str(self.tess.highOctave)}</sub>, {self.tess.lowFreq}–{self.tess.highFreq} Hz")
        self.pdf.ln(1)
        self.pdf.set_x(40)
        self.pdf.write_html(f"Median \u0192<sub>o</sub> (<i>Q<sub>2p</sub></i>): ≈{self.tess.medianNote}<sub>{str(self.tess.medianOctave)}</sub>, {self.tess.median} Hz")
        self.pdf.ln(3)

        passaggio_images = self.generate_passaggio_image()
        tess_success = self.generate_tess_image()

        if tess_success == 1:
            tess_fp = "results/" + self.filename + "-Tessitura-" + self.passa.clef + "-1.png"
            self.pdf.image(tess_fp, w=65, h=0, x="C")
        else:
            self.pdf.set_font("times_new", "B", 12)
            self.pdf.set_fill_color(255, 255, 0)
            self.pdf.cell(0, 5, "NO TESSITURA / RANGE IMAGE: MUSESCORE FILEPATH NOT FOUND.", align="C", fill=True)
            self.pdf.ln(5)

        self.pdf.ln(5)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
        self.pdf.ln(5)

        self.pdf.set_font("times_new", "BI", 12)
        self.pdf.cell(0, 5, f"Passaggi", new_x="LMARGIN", new_y="NEXT", align="L")

        # ======================= WRITE TABLE =====================

        margin_offset = 30

        # Header
        self.pdf.set_x(margin_offset)
        self.pdf.set_font("times_new", "", 12)
        self.pdf.cell(50, 5, "", border=0, align="L")
        self.pdf.cell(35, 5, "High Voice (HV)", border=0, align="C")
        self.pdf.cell(35, 5, "Medium Voice (MV)", border=0, align="C")
        self.pdf.cell(35, 5, "Low Voice (LV)", border=0, align="C")
        self.pdf.ln()

        # Row 1
        self.pdf.set_x(margin_offset)
        self._passaggio_cell("High", "Hp")
        self.pdf.cell(35, 5, f"{self.passa.hvhp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.mvhp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.lvhp.percentage}%", border=0, align="C")
        self.pdf.ln()

        # Row 2
        self.pdf.set_x(margin_offset)
        self._passaggio_cell("Middle", "Mp")
        self.pdf.cell(35, 5, f"{self.passa.hvmp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.mvmp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.lvmp.percentage}%", border=0, align="C")
        self.pdf.ln()

        # Row 3
        self.pdf.set_x(margin_offset)
        self._passaggio_cell("Low", "Lp")
        self.pdf.cell(35, 5, f"{self.passa.hvlp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.mvlp.percentage}%", border=0, align="C")
        self.pdf.cell(35, 5, f"{self.passa.lvlp.percentage}%", border=0, align="C")
        self.pdf.ln()

        # Total row divider
        self.pdf.ln(5)

        # Row 4
        self.pdf.set_x(margin_offset)
        self.pdf.cell(50, 5, f"Total", border=0, align="L")
        hv_arr = [self.passa.hvhp.percentage, self.passa.hvmp.percentage, self.passa.hvlp.percentage]
        self.pdf.cell(35, 5, f"{round(sum(hv_arr), 1)}%", border=0, align="C")
        mv_arr = [self.passa.mvhp.percentage, self.passa.mvmp.percentage, self.passa.mvlp.percentage]
        self.pdf.cell(35, 5, f"{round(sum(mv_arr), 1)}%", border=0, align="C")
        lv_arr = [self.passa.lvhp.percentage, self.passa.lvmp.percentage, self.passa.lvlp.percentage]
        self.pdf.cell(35, 5, f"{round(sum(lv_arr), 1)}%", border=0, align="C")
        self.pdf.ln()

        # ================================================================

        self.pdf.ln(15)

        images = [(passaggio_images["High Voice"], "HV"),(passaggio_images["Medium Voice"], "MV"),(passaggio_images["Low Voice"], "LV")]

        page_width = self.pdf.w - 2 * self.pdf.l_margin

        img_width = 40
        gap = 15

        total_width = 3 * img_width + 2 * gap
        start_x = self.pdf.l_margin + (page_width - total_width) / 2

        y = self.pdf.get_y()

        x = start_x
        for img, txt in images:
            self.pdf.text(x=x+16, y=y-2, text=txt)
            self.pdf.image(img, x=x, y=y, w=img_width)
            x += img_width + gap

        if tess_success == 1:
            os.remove(os.path.join("results", self.filename + "-Tessitura-" + self.passa.clef + "-1.png"))
        if os.path.exists(os.path.join("results", self.filename + "-Tessitura-" + self.passa.clef + ".musicxml")):
            os.remove(os.path.join("results", self.filename + "-Tessitura-" + self.passa.clef + ".musicxml"))

        self.pdf.ln(5)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y() + 25, self.pdf.w - self.pdf.r_margin, self.pdf.get_y() + 25)
        self.pdf.ln(5)

    def print_and_write_metrics(self):
        self.ensure_musescore_configured()
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
        p75 = convert_to_music_21_note(self.tess.highNote, self.tess.highOctave)
        high = convert_to_music_21_note(self.tess.max_pitch_note, self.tess.max_pitch_octave)

        notes = [low, p25, p75, high]
        c = music21.chord.Chord(notes)
        c.quarterLength = 4.0

        m.append(c)

        # Remove time signature from measure
        ts = music21.meter.TimeSignature('4/4')
        ts.style.hideObjectOnPrint = True
        m.insert(0, ts)

        fp = os.path.join("results", self.filename + "-Tessitura-" + self.tess.clef)
        try:
            m.write('musicxml.png', fp=fp)
        except Exception:
            print("WARNING: Musescore path not found or could not be used.")
            return -1
        return 1

    def _render_voice(self, voice_type_pass, voice_type):

        font = ImageFont.truetype(utils.resource_path(os.path.join("data", "Times New Roman.ttf")), size=48)

        img = Image.open(utils.resource_path(f"data/images/{voice_type}.png"))

        draw = ImageDraw.Draw(img)
        draw.rectangle([535, 0, 700, 350], fill="white", outline="white")
        draw.text((550, voice_type_pass[0][1]), str(voice_type_pass[0][0]) + "%", fill="black", font=font)
        draw.text((550, voice_type_pass[1][1]), str(voice_type_pass[1][0]) + "%", fill="black", font=font)
        draw.text((550, voice_type_pass[2][1]), str(voice_type_pass[2][0]) + "%", fill="black", font=font)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def generate_passaggio_image(self):
        hv_notes = [(self.passa.hvhp.percentage, 50), (self.passa.hvmp.percentage, 195), (self.passa.hvlp.percentage, 260)]
        mv_notes = [(self.passa.mvhp.percentage, 70), (self.passa.mvmp.percentage, 217), (self.passa.mvlp.percentage, 285)]
        lv_notes = [(self.passa.lvhp.percentage, 90), (self.passa.lvmp.percentage, 237), (self.passa.lvlp.percentage, 305)]

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                "High Voice":   executor.submit(self._render_voice, hv_notes, "High Voice"),
                "Medium Voice": executor.submit(self._render_voice, mv_notes, "Medium Voice"),
                "Low Voice":    executor.submit(self._render_voice, lv_notes, "Low Voice"),
            }
            return {k: f.result() for k, f in futures.items()}
           
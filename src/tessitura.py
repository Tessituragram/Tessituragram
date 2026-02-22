from src import events, utils
import copy

class PassaggioMetrics:
    def __init__(self, time_dose, percentage):
        self.time_dose = time_dose
        self.percentage = percentage

class Passaggio:
    def __init__(self, notes, clef, time_dose):
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
        self.time_dose = time_dose
        self.create_passagio_mapping()

    def calculate_passaggio(self, low, high):
        '''
        Given a passaggio range, calculates the time dose and percentage of time in that range.
        '''
        sum_durations = 0
        for pitch, duration in zip(self.pitches, self.durations):
            if low - 0.1 <= pitch <= high + 0.1:
                sum_durations += duration
        percent_p = round((sum_durations / sum(self.durations))*100, 2)
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

    def print_passagio(self):
        print("High Voice High Passaggio: ", str(self.hvhp.time_dose) + "s,", str(round((self.hvhp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("High Voice Middle Passaggio: ", str(self.hvmp.time_dose) + "s,", str(round((self.hvmp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("High Voice Low Passaggio: ", str(self.hvlp.time_dose) + "s,", str(round((self.hvlp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Medium Voice High Passaggio: ", str(self.mvhp.time_dose) + "s,", str(round((self.mvhp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Medium Voice Middle Passaggio: ", str(self.mvmp.time_dose) + "s,", str(round((self.mvmp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Medium Voice Low Passaggio: ", str(self.mvlp.time_dose) + "s,", str(round((self.mvlp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Low Voice High Passaggio: ", str(self.lvhp.time_dose) + "s,", str(round((self.lvhp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Low Voice Middle Passaggio: ", str(self.lvmp.time_dose) + "s,", str(round((self.lvmp.time_dose / self.time_dose)*100,1)) + "%")
        
        print("Low Voice Low Passaggio: ", str(self.lvlp.time_dose) + "s,", str(round((self.lvlp.time_dose / self.time_dose)*100,1)) + "%")
        print("=================================================")

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

    def print_tessitura(self):
        print("\nMusical Demand Profile" + " (" + self.clef + " Clef Range)")
        print("Compositional Range: " + str(self.min_pitch) + "\u2013" + str(self.max_pitch) + " Hz,", 
              self.min_pitch_note + utils.convert_digit_to_subscript(self.min_pitch_octave) + "\u2013" + 
              self.max_pitch_note + utils.convert_digit_to_subscript(self.max_pitch_octave))
        print("Tessitura Range: ", str(self.lowFreq) + "\u2013" + str(self.highFreq) + " Hz,", 
              self.lowNote + utils.convert_digit_to_subscript(self.lowOctave) + "\u2013" + 
              self.highNote + utils.convert_digit_to_subscript(self.highOctave))
        print("Median Frequency: " + str(self.median) + " Hz,", "~" + self.medianNote + 
              utils.convert_digit_to_subscript(self.medianOctave))
        print("Cycle Dose: " + str(self.cycle_dose) + " vibrations")
        print("Total Time: " + str(self.total_time) + "s")
        print("Time Dose: " + str(self.time_dose) + "s")
        print("Rest Time: " + str(self.rest_time) + "s\n")


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
        pass_treble = Passaggio(notes_treble, "Treble", tess_treble.time_dose)
        pass_bass = Passaggio(notes_bass, "Bass", tess_bass.time_dose)
        return [tess_treble, tess_bass], [pass_treble, pass_bass], ["treble", "bass"]
    elif clef == "treble":
        notes_treble = notes
        notes_bass = copy.deepcopy(notes)
        for note in notes_bass: 
            if isinstance(note, events.Note):
                note.frequency *= 0.5
        tess_treble = Tessitura(notes_treble, "Treble")
        tess_bass = Tessitura(notes_bass, "Bass")
        pass_treble = Passaggio(notes_treble, "Treble", tess_treble.time_dose)
        pass_bass = Passaggio(notes_bass, "Bass", tess_bass.time_dose)
        return [tess_treble, tess_bass], [pass_treble, pass_bass], ["treble", "bass"]
    else:
        tess = Tessitura(notes, "None")
        passaggio = Passaggio(notes, "None", tess.time_dose)
        return [tess], [passaggio], ["None"]

    
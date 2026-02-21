from src import events, utils
import copy

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
        percent_p = round((sum_durations / sum(self.durations))*100, 2)
        return PassaggioMetrics(round(sum_durations, 2), percent_p)
    
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
        print("\nPassagio: ")
        print("Clef: ", self.clef)
        print("High Voice High Passagio: ", str(self.hvhp.time_dose) + "s")
        print("High Voice Middle Passagio: ", str(self.hvmp.time_dose) + "s")
        print("High Voice Low Passagio: ", str(self.hvlp.time_dose) + "s")
        print("Middle Voice High Passagio: ", str(self.mvhp.time_dose) + "s")
        print("Middle Voice Middle Passagio: ", str(self.mvmp.time_dose) + "s")
        print("Middle Voice Low Passagio: ", str(self.mvlp.time_dose) + "s")
        print("Low Voice High Passagio: ", str(self.lvhp.time_dose) + "s")
        print("Low Voice Middle Passagio: ", str(self.lvmp.time_dose) + "s")
        print("Low Voice Low Passagio: ", str(self.lvlp.time_dose) + "s")
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
        self.min_pitch = None
        self.max_pitch = None
        self.calculate_tessitura(notes)

    def print_tessitura(self):
        print("\nTessitura: ")
        print("Clef: ", self.clef)
        print("Minimum Frequency: ", str(self.lowFreq) + "Hz")
        print("Minimum Note: ", self.lowNote + str(self.lowOctave))
        print("Maximum Frequency: ", str(self.highFreq) + "Hz")
        print("Maximum Note: ", self.highNote + str(self.highOctave))
        print("Cycle Dose: " + str(self.cycle_dose) + " vibrations")
        print("Total Time: " + str(self.total_time) + "(s)")
        print("Time Dose: " + str(self.time_dose) + "(s)")
        print("Rest Time: " + str(self.rest_time) + "(s)")
        print("Compositional Range: " + str(self.min_pitch) + "-" + str(self.max_pitch) + "Hz")
        print("Median: " + str(self.median) + "Hz")
        print("=================================================")

    def calculate_cycle_dose(self, pitches, durations):
        sum = 0
        for pitch, duration in zip(pitches, durations):
            sum += pitch*duration
        return round(sum, 2)

    def calculate_total_time(self, notes):
        sum = 0 
        for note in notes:
            sum += note.duration
        return round(sum, 2)

    def calculate_tessitura(self, notes):
        pitches = []
        durations = []
        for note in notes:
            if isinstance(note, events.Note):
                pitches.append(note.frequency)
                durations.append(note.duration)
        self.lowFreq = round(utils.weighted_percentile_expand(pitches, 25, weights = durations), 2)
        self.highFreq = round(utils.weighted_percentile_expand(pitches, 75, weights = durations), 2)
        self.lowNote, self.lowOctave = utils.freq_to_note(self.lowFreq)
        self.highNote, self.highOctave = utils.freq_to_note(self.highFreq)
        self.cycle_dose = self.calculate_cycle_dose(pitches, durations)
        self.total_time = self.calculate_total_time(notes)
        self.time_dose = round(sum(durations), 2)
        self.rest_time = round(self.total_time - sum(durations), 2)
        self.median = round(utils.weighted_percentile_expand(pitches, 50, weights = durations), 2)
        self.min_pitch = round(min(pitches),2)
        self.max_pitch = round(max(pitches), 2)
        
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

    
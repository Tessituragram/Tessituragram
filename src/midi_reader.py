"""midi_reader.py: Defines the MidiParser class, which opens a midi file and reads it. Converts
    the binary midi file to notes and rests with durations."""

from src import utils, events

__author__      = "Troy Conklin"

# Sources used: 
# https://ccrma.stanford.edu/~craig/14q/midifile/MidiFileFormat.html
# http://midi.teragonaudio.com/tech/midifile/time.htm#:~:text=Time%20signature%20is%20expressed%20as,clocks%20in%20a%20metronome%20click.
# https://www.recordingblogs.com/wiki/midi-key-signature-meta-message


class MidiParser:
    def __init__(self, filepath):
        """
        Initializes the MidiParser object and reads the filepath provided as a BufferedReader

        Args:
            filepath (str): The filepath for a midi file
        
        """
        self.f = open(filepath, mode = 'rb')
        self.byte_counter = 0
        self.events = []
        self.division = None
        self.number_tracks = None
        self.error_message = None

    def parse_varlen_value(self):
        """
        Reads the next variable length value in MidiParser and returns the value and the number of bytes read.

        Args:
            self (MidiParser): The MidiParser object with a BufferedReader field f

        Returns:
            int: The next variable length value in f
            int: The number of bytes read

        """
        length = 1
        result = 0
        # Masks for getting the last 7 bits and first bit
        end_mask = 0b01111111
        start_mask = 0b10000000
        # Read in the varlen number
        number = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        # Determine if the next byte should be read
        continuation = start_mask & number
        result += end_mask & number
        # Loop until the number ends
        while continuation:
            length += 1
            result = result << 7
            number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            continuation = start_mask & number
            result = result | (end_mask & number)
        return result, length

    def parse_controller_event(self, channel_number, v_time):
        """
        Parses the controller event(s) at the current midi file position. The calling function will have encountered
        a controller event of 0xB_.

        Args:
            channel_number (int): The channel number for the event (determined by event byte)
            v_time (int): The elapsed time from the previous event to this event

        Returns:
            [ControllerEvent]: A list of ControllerEvent(s) at the current midi file position.

        """
        times = []
        controller_numbers = []
        values = []
        while True:
            controller_number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            if controller_number >= 0x80:
                break
            value = int.from_bytes(self.f.read(1)) 
            self.byte_counter += 1
            controller_numbers.append(controller_number)
            values.append(value)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.ControllerEvent(time, channel_number, controller_number, value)
            for time, controller_number, value in zip(times, controller_numbers, values)]
    
    def parse_program_change_event(self, channel_number, v_time):
        """
        Parses the program change event at the current midi file position. The calling function will have encountered
        an event number of 0xC_.

        Args:
            channel_number (int): The channel number for the event (determined by event byte)
            v_time (int): The elapsed time from the previous event to this event

        Returns:
            [ProgramChangeEvent]: A list of ProgramChangeEvent(s) at the current midi file position.

        """
        times = []
        program_numbers = []
        while True:
            program_number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            if program_number >= 0x80:
                break
            program_numbers.append(program_number)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.ProgramChangeEvent(time, channel_number, program_number)
            for time, program_number in zip(times, program_numbers)]
    
    def parse_midi_port_event(self, v_time):
        """
        Parses the midi port event at the current midi file position. The calling function will have encountered
        an event number of 0x21.

        Returns:
            MidiPortEvent: The MidiPortEvent at the current position

        """
        port = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        return events.MidiPortEvent(v_time, port)
    
    def parse_key_signature(self, v_time):
        """
        Parses the key signature at the current midi file position. The calling function will have encountered
        an event number 0x59. The key signature in the MidiParser class is updated.

        Returns:
            MetaEvent: A MetaEvent with name Key Signature.

        """
        key_signature = int.from_bytes(self.f.read(1), signed=True)
        self.byte_counter += 1
        scale = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        if scale:
            scale = "Major"
        else:
            scale = "Minor"
        key_signature = utils.KeySignature(key_signature, scale)
        return events.MetaEvent(v_time, "Key Signature", key_signature)
    
    def parse_note_on_event(self, channel_number, v_time):
        """
        Parses the note on event at the current midi file position. The calling function will have encountered
        an event number of 0x9_.

        Args:
            channel_number (int): The channel number for the event (determined by event byte)
            v_time (int): The elapsed time from the previous event to this event

        Returns:
            [NoteOnEvent]: A list of NoteOnEvent(s) at the current midi file position.

        """
        times = []
        note_numbers = []
        velocities = []
        note_number = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        while True:
            if note_number >= 0x80:
                break
            velocity = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            velocities.append(velocity)
            note_numbers.append(note_number)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
            note_number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.NoteOnEvent(time, channel_number, note_number, velocity)
            for time, note_number, velocity in zip(times, note_numbers, velocities)]
    
    def parse_note_off_event(self, channel_number, v_time):
        """
        Parses the note off event at the current midi file position. The calling function will have encountered
        an event number of 0x8_.

        Args:
            channel_number (int): The channel number for the event (determined by event byte)
            v_time (int): The elapsed time from the previous event to this event

        Returns:
            [NoteOnEvent]: A list of NoteOffEvent(s) at the current midi file position.

        """
        times = []
        note_numbers = []
        velocities = []
        note_number = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        while True:
            if note_number >= 0x80:
                break
            velocity = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            velocities.append(velocity)
            note_numbers.append(note_number)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
            note_number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.NoteOffEvent(time, channel_number, note_number, velocity)
            for time, note_number, velocity in zip(times, note_numbers, velocities)]
    
    def parse_channel_aftertouch_event(self, channel_number, v_time):
        """
        Parses the ChannelAftertouchEvent at the current MIDI position and returns it.
        """
        times = []
        amounts = []
        amount = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        while True:
            if amount >= 0x80:
                break
            amounts.append(amount)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
            amount = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.ChannelAftertouchEvent(time, channel_number, amount)
            for time, amount in zip(times, amounts)]
    
    def parse_note_aftertouch_event(self, channel_number, v_time):
        """Parses the NoteAfterTouchEvent the current MIDI position and returns it."""
        times = []
        note_numbers = []
        amounts = []
        note_number = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        while True:
            if note_number >= 0x80:
                break
            amount = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            amounts.append(amount)
            note_numbers.append(note_number)
            times.append(v_time)
            v_time, length = self.parse_varlen_value()
            note_number = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.NoteAftertouchEvent(time, channel_number, note_number, amount)
            for time, note_number, amount in zip(times, note_numbers, amounts)]
    
    def parse_meta(self, v_time, name, v_length, decode=False):
        """
        Parses the generic meta event at the current MIDI position and returns it.
        """
        data = self.f.read(v_length)
        self.byte_counter += v_length
        if decode:
            data = data.decode('utf-8')
        return events.MetaEvent(v_time, name, data)
    
    def parse_time_signature(self, v_time):
        """
        Parses the time signature MetaEvent at the current MIDI position and returns it.
        """
        numerator = int.from_bytes(self.f.read(1))
        denominator = int.from_bytes(self.f.read(1))
        num_midi_clocks = int.from_bytes(self.f.read(1))
        num_32_notes = int.from_bytes(self.f.read(1))
        self.byte_counter += 4
        ts = utils.TimeSignature(numerator, denominator, num_midi_clocks, num_32_notes)
        return events.MetaEvent(v_time, "Time Signature", ts)
    
    def parse_smpte_offset(self, v_time):
        """
        Parses the SMPTEOffset MetaEvent at the current MIDI position and returns it.
        """
        hours = int.from_bytes(self.f.read(1))
        minutes = int.from_bytes(self.f.read(1))
        seconds = int.from_bytes(self.f.read(1))
        frames = int.from_bytes(self.f.read(1))
        subframes = int.from_bytes(self.f.read(1))
        self.byte_counter += 5
        return events.MetaEvent(v_time, "SMPTE Offset",utils.SMPTEOffset(hours, minutes, seconds, frames, subframes))
    
    def parse_tempo_event(self, v_time):
        """
        Parses the TempoEvent at the current MIDI position and returns it.
        """
        tempo = int.from_bytes(self.f.read(3))
        self.byte_counter += 3
        return events.TempoEvent(v_time, tempo)
    
    def parse_system_exclusive_event(self, v_time):
        """
        Parses the SystemExclusiveEvent at the current MIDI position and returns it.
        """
        while True:
            self.byte_counter += 1
            if int.from_bytes(self.f.read(1)) == 0xF7:
                break
        return events.SystemExclusiveEvent(v_time)
    
    def parse_pitch_bend_event(self, channel_number, v_time):
        """
        Parses the pitch bend event at the current midi file position. The calling function will have encountered
        an event number of 0xE_.

        Args:
            channel_number (int): The channel number for the event (determined by event byte)
            v_time (int): The elapsed time from the previous event to this event

        Returns:
            [PitchBendEvent]: A list of PitchBendEvent(s) at the current midi file position.
        """
        times = []
        lsbs = []
        msbs = []
        lsb = int.from_bytes(self.f.read(1))
        msb = int.from_bytes(self.f.read(1))
        self.byte_counter += 2
        times.append(v_time)
        lsbs.append(lsb)
        msbs.append(msb)
        v_time, length = self.parse_varlen_value()
        next_byte = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        # If using running status:
        while next_byte < 0x80:
            lsb = next_byte
            msb = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            times.append(v_time)
            lsbs.append(lsb)
            msbs.append(msb)
            v_time, length = self.parse_varlen_value()
            next_byte = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
        self.f.seek(-1 - length, 1)
        self.byte_counter -= (length + 1)
        return [events.PitchBendEvent(time, channel_number, lsb, msb)
                for time, lsb, msb in zip(times, lsbs, msbs)]
    
    def skip_system_message(self, event: int, v_time):
        """
        Skip over a system message (0xF1–0xFE) without parsing it.
        Ensures byte alignment is maintained.
        """
        # Map of system message -> number of data bytes that follow
        system_message_lengths = {
            0xF1: 1,
            0xF2: 2,
            0xF3: 1,
            0xF4: 0, 
            0xF5: 0,
            0xF6: 0,
            0xF8: 0,
            0xF9: 0,
            0xFA: 0,
            0xFB: 0,
            0xFC: 0,
            0xFD: 0,
            0xFE: 0,
        }

        # Find how many bytes to skip
        length = system_message_lengths.get(event, 0)

        # Skip the appropriate number of bytes
        if length > 0:
            _ = self.f.read(length)
            self.byte_counter += length
        return events.MidiEvent(
            event_name=f"0x{event:02X}",
            time=v_time,
        )

    def parse_midi_event(self) -> events.MidiEvent:
        """
        Parses the event at the current midi file position. Increments the reader
        location to the next event.

        Returns:
            MidiEvent: A MidiEvent for the event at the current midi file position.

        """
        v_time, _ = self.parse_varlen_value()
        event = int.from_bytes(self.f.read(1))
        self.byte_counter += 1
        if event < 0x80:
            self.error_message = f"Found an invalid event in the MIDI file (status byte {event}). The file may be corrupted."
            print("Could not read MIDI file. Found an event with invalid status " + str(event) + ".")
            return -1
        if event == 0xFF:
            meta_type = int.from_bytes(self.f.read(1))
            self.byte_counter += 1
            v_length, _ = self.parse_varlen_value()
            match meta_type:
                case 0x00:
                    return self.parse_meta(v_time, "Sequence Number", v_length)
                case 0x01:
                    return self.parse_meta(v_time, "Text Event", v_length, decode=True)
                case 0x02:
                    return self.parse_meta(v_time, "Copyright Notice", v_length, decode = True)
                case 0x03:
                    return self.parse_meta(v_time, "Sequence or Track Name", v_length, decode=True)
                case 0x04:
                    return self.parse_meta(v_time, "Instrument Name", v_length, decode=True)
                case 0x05:
                    return self.parse_meta(v_time, "Lyric Text", v_length, decode=True)
                case 0x06:
                    return self.parse_meta(v_time, "Marker Text", v_length, decode=True)
                case 0x07:
                    return self.parse_meta(v_time, "Cue Point", v_length, decode=True) 
                case 0x20:
                    return self.parse_meta(v_time, "MIDI Channel Prefix Assignment", v_length)
                case 0x21:
                    return self.parse_midi_port_event(v_time)
                case 0x2F:
                    # End of track
                    return
                case 0x51:
                    return self.parse_tempo_event(v_time)
                case 0x54:
                    return self.parse_smpte_offset(v_time)
                case 0x58:
                    return self.parse_time_signature(v_time)
                case 0x59:
                    outputs = self.parse_key_signature(v_time)
                    return outputs
                case 0x7F:
                    return self.parse_meta(v_time, "Sequencer Specific Event", v_length)
                case _:
                    # Skip unknown meta events
                    print(f"Skipped unknown meta event 0x{meta_type:02X} of length {v_length}")
                    return self.parse_meta(v_time, f"Unknown Meta Event 0x{meta_type:02X}", v_length)
        if event >= 0xA0 and event <= 0xAF:
            channel_number = 0b1111 & event
            outputs = self.parse_note_aftertouch_event(channel_number, v_time)
            return outputs
        if event >= 0xB0 and event <= 0xBF:
            channel_number = 0b1111 & event
            outputs = self.parse_controller_event(channel_number, v_time)
            return outputs
        if event >= 0xC0 and event <= 0xCF:
            channel_number = 0b1111 & event
            outputs = self.parse_program_change_event(channel_number, v_time)
            return outputs
        if event >= 0xD0 and event <= 0xDF:
            channel_number = 0b1111 & event
            outputs = self.parse_channel_aftertouch_event(channel_number, v_time)
            return outputs
        if event >= 0xE0 and event <= 0xEF:
            channel_number = 0b1111 & event
            outputs = self.parse_pitch_bend_event(channel_number, v_time)
            return outputs
        if event == 0xF0:
            return self.parse_system_exclusive_event(v_time)
        if 0xF1 <= event <= 0xFE and event not in (0xF0, 0xF7, 0xFF):
             return self.skip_system_message(event, v_time)
        if event >= 0x80 and event <= 0x8F:
            return self.parse_note_off_event(0b1111 & event, v_time)
        if event >= 0x90 and event <= 0x9F:
            return self.parse_note_on_event(0b1111 & event, v_time)

    def parse_track(self) -> list[events.MidiEvent]:
        """
        Parses the track at the current position and returns a list of MidiEvents for the
        track. Returns -1 on error.
        """
        self.byte_counter = 0
        events_list = []
        is_track = self.f.read(4)
        if is_track != bytes('MTrk', 'utf-8'):
            self.error_message = "Could not find a valid track in the MIDI file. The file may be corrupted or not a standard MIDI file."
            print("Could not find a track.")
            return -1
        track_length = int.from_bytes(self.f.read(4))
        while True:
            event = self.parse_midi_event()
            # If there is an error
            if event == -1:
                return -1
            if not event:
                break
            if isinstance(event, list):
                for e in event:
                    events_list.append(e)
            else:
                events_list.append(event)
        if self.byte_counter != track_length:
            self.error_message = "The MIDI file appears to be incomplete or corrupted (unexpected end of track data)."
            print("Could not read the full file")
            return -1
        return events_list

    def contains_notes(self, event_list):
        """
        Given a list of midi events checks if that list contains notes
        """
        for event in event_list:
            if isinstance(event, events.NoteOnEvent):
                return True
        return False
    
    def combine_tracks(self, meta_track, inst_track):
        """
        Merge the tempo change events from meta_track into the
        events in in inst_track.
        """
        output_track = []
        cur_inst = 0
        cur_meta = 0
        while cur_inst < len(inst_track) and cur_meta < len(meta_track):
            cur_inst_event = inst_track[cur_inst]
            cur_meta_event = meta_track[cur_meta]
            if cur_inst_event.time < cur_meta_event.time:
                output_track.append(cur_inst_event)
                cur_meta_event.time -= cur_inst_event.time
                cur_inst += 1
            else:
                if isinstance(cur_meta_event, events.TempoEvent):
                    output_track.append(cur_meta_event)
                    cur_inst_event.time -= cur_meta_event.time
                cur_meta += 1
        if cur_inst < len(inst_track):
            output_track = output_track + inst_track[cur_inst:]
        if cur_meta < len(meta_track):
            for meta_event in meta_track[cur_meta:]:
                if isinstance(meta_event, events.TempoEvent):
                    output_track.append(meta_event)  
        return output_track

    def parse_header(self):
        """
        Parses the midi file header. Fails if the file type is invalid or the number of tracks is != 1 or 2.

        Returns:
            int: -1 on failure, 1 on passing.
        """
        is_midi = self.f.read(4)
        if is_midi != bytes('MThd', 'utf-8'):
            self.error_message = "This doesn't appear to be a valid MIDI file -- MIDI header invalid."
            print("Invalid file type.")
            return -1
        header_size = int.from_bytes(self.f.read(4))
        if header_size != 6:
            self.error_message = "This doesn't appear to be a valid MIDI file (unexpected header size)."
            print("Invalid file type.")
            return -1
        format_mapping = {0: "Single Track", 1: "Multiple Tracks", 2: "Multiple Songs"}
        file_format = format_mapping[int.from_bytes(self.f.read(2))]
        self.number_tracks = int.from_bytes(self.f.read(2))
        if self.number_tracks != 1 and self.number_tracks != 2:
            self.error_message = f"This MIDI file has {self.number_tracks} tracks, but only files with 1 or 2 tracks are supported."
            print("Incorrect number of tracks. There should only be 1 or 2 tracks. Found " + str(self.number_tracks) + " tracks.")
            return -1
        division = int.from_bytes(self.f.read(2))
        self.division = division
        return 1
            
    def parse_midi(self):
        """
        Parses all midi events in the midi file. Returns -1 on failure

        Returns:
            int: -1 if a failure has occurred. 0 if passed.

        """
        # Parse track information
        if self.parse_header() == -1:
            return -1
        events_track_1 = self.parse_track()
        if events_track_1 == -1:
            return -1
        if self.number_tracks == 1:
            self.events = events_track_1
        if self.number_tracks == 2:
            events_track_2 = self.parse_track()
            if events_track_2 == -1:
                return -1
            instrument_track = None
            meta_track = None
            if self.contains_notes(events_track_1) and self.contains_notes(events_track_2):
                self.error_message = "This MIDI file has notes on two separate tracks. Please combine them into a single melodic line."
                print("Incorrect number of tracks. Found 2 tracks with notes.")
                return -1
            if self.contains_notes(events_track_1):
                instrument_track = events_track_1
                meta_track = events_track_2
            else:
                instrument_track = events_track_2
                meta_track = events_track_1
            self.events = self.combine_tracks(meta_track, instrument_track)
        if not self.f.closed:
            self.f.close()
        return 0
        
    def find_micro_rest(self, note_list, eps=0.02):
        """
        Finds microrests if they exist. Assumes all microrests in the piece
        have the same duration.

        Args:
            eps: Time (in seconds) to be considered a microrest

        Returns: The corresponding microrest duration (in seconds)
        """
        for note in note_list:
            if isinstance(note, events.Rest) and note.duration <= eps:
                return note.duration
        return -1
    
    def remove_micro_rests(self, note_list, eps=0.02):
        """
        Normalizes the duration of notes in the midi file by removing short
        rests under the threshold eps. A second pass filters the list to remove
        notes that have a duration less than 0.001 seconds.
        """
        micro_dur = self.find_micro_rest(note_list, eps)
        if micro_dur != -1:
            for note in note_list:
                if isinstance(note, events.Note):
                    note.duration += micro_dur
                if isinstance(note, events.Rest):
                    note.duration -= micro_dur
        note_list = [note for note in note_list if note.duration > 0.001]
        return note_list

    def get_notes(self):
        note_list = []
        current_time_ticks = 0
        current_time_secs = 0.0
        last_event_time_secs = 0.0
        note_number = None
        note_start_time_secs = None
        current_tempo = 500000     # µs per quarter note
        ticks_per_beat = self.division
        def ticks_to_seconds(ticks, tempo, ticks_per_beat):
            # tempo: µs per quarter note
            return ticks * (tempo / 1_000_000.0) / ticks_per_beat
        for event in self.events:
            delta_ticks = event.time
            # convert delta ticks -> seconds using the tempo that was in effect during this delta
            delta_secs = ticks_to_seconds(delta_ticks, current_tempo, ticks_per_beat)
            current_time_ticks += delta_ticks
            current_time_secs += delta_secs
            # update tempo if this is a set_tempo meta-event
            if isinstance(event, events.TempoEvent):
                # tempo change affects subsequent deltas
                current_tempo = event.tempo
                continue
            if isinstance(event, events.NoteOnEvent) and event.velocity > 0:
                if note_number:
                    self.error_message = "This MIDI file contains overlapping notes (a new note starts before the previous one ends). " \
                    "Please ensure the melody is a single monophonic line."
                    print("Found overlapping notes.")
                    return -1
                if current_time_secs > last_event_time_secs:
                    rest_duration_secs = current_time_secs - last_event_time_secs
                    note_list.append(events.Rest(rest_duration_secs))
                note_start_time_secs = current_time_secs
                note_number = event.noteNumber
            elif isinstance(event, events.NoteOffEvent) or (
                isinstance(event, events.NoteOnEvent) and event.velocity == 0):
                if note_start_time_secs is not None:
                    duration_secs = current_time_secs - note_start_time_secs
                    frequency = utils.get_frequency(note_number)
                    note_list.append(events.Note(duration_secs, frequency))
                    last_event_time_secs = current_time_secs
                    note_start_time_secs = None
                    note_number = None
        return note_list

    def post_process(self, notes):
        '''
        Removes micro rests from note_list. Validates and removes C1 from end of track.
        '''
        notes = self.remove_micro_rests(notes)
        if (notes and isinstance(notes[-1], events.Note) and round(notes[-1].frequency, 2) == 32.70):
            notes.pop()
        else:
            self.error_message = "The MIDI file is missing the required trailing C1 note used for reference."
            print("Need to include a C1 note at the end of file.")
            return -1
        return notes
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True
           
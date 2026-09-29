from django import forms
from .models import Record

class SimpleSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    larger_work = forms.CharField(max_length=200, required=False)
    composer = forms.CharField(max_length=200, required=False, label="Musical Composer")
    author = forms.CharField(max_length=200, required=False)
    submitter = forms.CharField(required=False, label="Submitter")

    style = forms.ChoiceField(
        choices=[("", "Any")] + Record.STYLE_CHOICES,
        required=False,
    )

    q1_freq_min = forms.FloatField(
        required=False,
        label="Low freq (min)",
    )
    q1_freq_max = forms.FloatField(
        required=False,
        label="Low freq (max)",
    )

    q3_freq_min = forms.FloatField(
        required=False,
        label="High freq (min)",
    )
    q3_freq_max = forms.FloatField(
        required=False,
        label="High freq (max)",
    )

    median_freq_min = forms.FloatField(
        required=False,
        label="Median freq (min)",
    )
    median_freq_max = forms.FloatField(
        required=False,
        label="Median freq (max)",
    )

    min_freq_min = forms.FloatField(
        required=False,
        label="Min freq — lower bound",
    )
    min_freq_max = forms.FloatField(
        required=False,
        label="Min freq — upper bound",
    )

    max_freq_min = forms.FloatField(
        required=False,
        label="Max freq — lower bound",
    )
    max_freq_max = forms.FloatField(
        required=False,
        label="Max freq — upper bound",
    )

PITCH_CHOICES = [
    ("", "Any"),
    ("C", "C"), ("C#", "C#"), ("D", "D"), ("D#", "D#"),
    ("E", "E"), ("F", "F"), ("F#", "F#"), ("G", "G"),
    ("G#", "G#"), ("A", "A"), ("A#", "A#"), ("B", "B"),
]

OCTAVE_CHOICES = [("", "Any")] + [(str(i), str(i)) for i in range(0, 9)]


class AdvancedSearchForm(forms.Form):
    # General
    title = forms.CharField(max_length=200, required=False)
    larger_work = forms.CharField(max_length=200, required=False)
    composer = forms.CharField(max_length=200, required=False)
    author = forms.CharField(max_length=200, required=False)
    initial_key = forms.ChoiceField(
        choices=[("", "Any")] + Record.INITIAL_KEY_CHOICES,
        required=False,
    )
    style = forms.ChoiceField(
        choices=[("", "Any")] + Record.STYLE_CHOICES,
        required=False,
    )
    style_other = forms.CharField(max_length=100, required=False)
    submitter = forms.CharField(required=False, label="Submitter")
    clef_range = forms.ChoiceField(
        choices=[("Treble", "Treble"), ("Bass", "Bass"), ("Unknown", "Unknown")],
        required=False,
    )
    voice_part = forms.ChoiceField(
        choices=[("", "Any")] + Record.VOICE_PART_CHOICES,
        required=False,
    )

    # Tessitura
    tessitura_bottom_note = forms.ChoiceField(
        choices=PITCH_CHOICES, required=False, label="Tessitura bottom (note)"
    )
    tessitura_bottom_octave = forms.ChoiceField(
        choices=OCTAVE_CHOICES, required=False, label="Tessitura bottom (octave)"
    )

    median_pitch_note = forms.ChoiceField(
        choices=PITCH_CHOICES, required=False, label="Median pitch (note)"
    )
    median_pitch_octave = forms.ChoiceField(
        choices=OCTAVE_CHOICES, required=False, label="Median pitch (octave)"
    )

    tessitura_top_note = forms.ChoiceField(
        choices=PITCH_CHOICES, required=False, label="Tessitura top (note)"
    )
    tessitura_top_octave = forms.ChoiceField(
        choices=OCTAVE_CHOICES, required=False, label="Tessitura top (octave)"
    )

    # Timing
    cycle_dose_min = forms.FloatField(required=False, label="Cycle dose (min)")
    cycle_dose_max = forms.FloatField(required=False, label="Cycle dose (max)")

    time_dose_min_minutes = forms.IntegerField(required=False, min_value=0, label="Time dose min (minutes)")
    time_dose_min_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Time dose min (seconds)")
    time_dose_max_minutes = forms.IntegerField(required=False, min_value=0, label="Time dose max (minutes)")
    time_dose_max_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Time dose max (seconds)")

    rest_time_min_minutes = forms.IntegerField(required=False, min_value=0, label="Rest time min (minutes)")
    rest_time_min_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Rest time min (seconds)")
    rest_time_max_minutes = forms.IntegerField(required=False, min_value=0, label="Rest time max (minutes)")
    rest_time_max_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Rest time max (seconds)")

    total_time_min_minutes = forms.IntegerField(required=False, min_value=0, label="Total time min (minutes)")
    total_time_min_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Total time min (seconds)")
    total_time_max_minutes = forms.IntegerField(required=False, min_value=0, label="Total time max (minutes)")
    total_time_max_seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label="Total time max (seconds)")

    # hvhp_time_dose_min = forms.FloatField(
    #     required=False, label="HV High passaggio (min)"
    # )
    # hvhp_time_dose_max = forms.FloatField(
    #     required=False, label="HV High passaggio (max)"
    # )

    # hvmp_time_dose_min = forms.FloatField(
    #     required=False, label="HV Middle passaggio (min)"
    # )
    # hvmp_time_dose_max = forms.FloatField(
    #     required=False, label="HV Middle passaggio (max)"
    # )

    # hvlp_time_dose_min = forms.FloatField(
    #     required=False, label="HV Low passaggio (min)"
    # )
    # hvlp_time_dose_max = forms.FloatField(
    #     required=False, label="HV Low passaggio (max)"
    # )

    # mvhp_time_dose_min = forms.FloatField(
    #     required=False, label="MV High passaggio (min)"
    # )
    # mvhp_time_dose_max = forms.FloatField(
    #     required=False, label="MV High passaggio (max)"
    # )

    # mvmp_time_dose_min = forms.FloatField(
    #     required=False, label="MV Middle passaggio (min)"
    # )
    # mvmp_time_dose_max = forms.FloatField(
    #     required=False, label="MV Middle passaggio (max)"
    # )

    # mvlp_time_dose_min = forms.FloatField(
    #     required=False, label="MV Low passaggio (min)"
    # )
    # mvlp_time_dose_max = forms.FloatField(
    #     required=False, label="MV Low passaggio (max)"
    # )

    # lvhp_time_dose_min = forms.FloatField(
    #     required=False, label="LV High passaggio (min)"
    # )
    # lvhp_time_dose_max = forms.FloatField(
    #     required=False, label="LV High passaggio (max)"
    # )

    # lvmp_time_dose_min = forms.FloatField(
    #     required=False, label="LV Middle passaggio (min)"
    # )
    # lvmp_time_dose_max = forms.FloatField(
    #     required=False, label="LV Middle passaggio (max)"
    # )

    # lvlp_time_dose_min = forms.FloatField(
    #     required=False, label="LV Low passaggio (min)"
    # )
    # lvlp_time_dose_max = forms.FloatField(
    #     required=False, label="LV Low passaggio (max)"
    # )

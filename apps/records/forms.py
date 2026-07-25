from django import forms
from .models import Record


class AdvancedSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    composer = forms.CharField(max_length=200, required=False)
    author = forms.CharField(max_length=200, required=False)
    style = forms.ChoiceField(
    choices=[("", "Any")] + Record.STYLE_CHOICES,
        required=False,
    )
    submitter = forms.CharField(required=False, label="Submitted by")

    clef_range = forms.ChoiceField(
        choices=[("", "Any"), ("Treble", "Treble"), ("Bass", "Bass"), ("None", "None")],
        required=False,
    )

    q1_freq_min = forms.FloatField(required=False, label="Low freq (min)")
    q1_freq_max = forms.FloatField(required=False, label="Low freq (max)")

    q3_freq_min = forms.FloatField(required=False, label="High freq (min)")
    q3_freq_max = forms.FloatField(required=False, label="High freq (max)")

    median_freq_min = forms.FloatField(required=False, label="median_freq freq (min)")
    median_freq_max = forms.FloatField(required=False, label="median_freq freq (max)")

    min_freq_min = forms.FloatField(required=False, label="Min freq — lower bound")
    min_freq_max = forms.FloatField(required=False, label="Min freq — upper bound")

    max_freq_min = forms.FloatField(required=False, label="Max freq — lower bound")
    max_freq_max = forms.FloatField(required=False, label="Max freq — upper bound")

    cycle_dose_min = forms.FloatField(required=False, label="Cycle dose (min)")
    cycle_dose_max = forms.FloatField(required=False, label="Cycle dose (max)")

    time_dose_min = forms.FloatField(required=False, label="Time dose (min)")
    time_dose_max = forms.FloatField(required=False, label="Time dose (max)")

    rest_time_min = forms.FloatField(required=False, label="Rest time (min)")
    rest_time_max = forms.FloatField(required=False, label="Rest time (max)")

    total_time_min = forms.FloatField(required=False, label="Total time (min)")
    total_time_max = forms.FloatField(required=False, label="Total time (max)")

    hvhp_time_dose_min = forms.FloatField(required=False, label="HV High passaggio (min)")
    hvhp_time_dose_max = forms.FloatField(required=False, label="HV High passaggio (max)")

    hvmp_time_dose_min = forms.FloatField(required=False, label="HV Middle passaggio (min)")
    hvmp_time_dose_max = forms.FloatField(required=False, label="HV Middle passaggio (max)")

    hvlp_time_dose_min = forms.FloatField(required=False, label="HV Low passaggio (min)")
    hvlp_time_dose_max = forms.FloatField(required=False, label="HV Low passaggio (max)")

    mvhp_time_dose_min = forms.FloatField(required=False, label="MV High passaggio (min)")
    mvhp_time_dose_max = forms.FloatField(required=False, label="MV High passaggio (max)")

    mvmp_time_dose_min = forms.FloatField(required=False, label="MV Middle passaggio (min)")
    mvmp_time_dose_max = forms.FloatField(required=False, label="MV Middle passaggio (max)")

    mvlp_time_dose_min = forms.FloatField(required=False, label="MV Low passaggio (min)")
    mvlp_time_dose_max = forms.FloatField(required=False, label="MV Low passaggio (max)")

    lvhp_time_dose_min = forms.FloatField(required=False, label="LV High passaggio (min)")
    lvhp_time_dose_max = forms.FloatField(required=False, label="LV High passaggio (max)")

    lvmp_time_dose_min = forms.FloatField(required=False, label="LV Middle passaggio (min)")
    lvmp_time_dose_max = forms.FloatField(required=False, label="LV Middle passaggio (max)")

    lvlp_time_dose_min = forms.FloatField(required=False, label="LV Low passaggio (min)")
    lvlp_time_dose_max = forms.FloatField(required=False, label="LV Low passaggio (max)")
from django import forms
from apps.records.models import Record

MAX_MIDI_SIZE = 5 * 1024 * 1024


class SubmissionForm(forms.Form):
    title = forms.CharField(max_length=255, label="Title of the piece")
    composer = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200, required=False)
    style = forms.ChoiceField(choices=[("", "Select a style")] + Record.STYLE_CHOICES)
    clef_range = forms.ChoiceField(
        choices=[("", "Not specified"), ("treble", "Treble"), ("bass", "Bass")],
        required=False,
    )
    midi_file = forms.FileField(label="MIDI file")
    keep_private = forms.BooleanField(
        required=False,
        label="Keep this submission private (skip public review)",
    )

    def clean_midi_file(self):
        if midi_file.size > MAX_MIDI_SIZE:
            raise forms.ValidationError("File is too large. Maximum size is 5MB.")
        midi_file = self.cleaned_data["midi_file"]
        if not midi_file.name.lower().endswith((".mid", ".midi")):
            raise forms.ValidationError("File must be a .mid or .midi file.")
        return midi_file


class ReviewerEditForm(forms.Form):
    midi_file = forms.FileField(required=False, label="Replace MIDI file (optional)")
    title = forms.CharField(max_length=255)
    composer = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200, required=False)
    style = forms.ChoiceField(choices=Record.STYLE_CHOICES)
    clef_range = forms.ChoiceField(
        choices=[("Treble", "Treble"), ("Bass", "Bass"), ("None", "None")]
    )

    def clean_midi_file(self):
        midi_file = self.cleaned_data.get("midi_file")
        if midi_file and not midi_file.name.lower().endswith((".mid", ".midi")):
            raise forms.ValidationError("File must be a .mid or .midi file.")
        return midi_file

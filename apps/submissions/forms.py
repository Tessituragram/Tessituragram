from django import forms
from apps.records.models import Record

from apps.submissions.widgets import KeySignatureWidget

MAX_MIDI_SIZE = 5 * 1024 * 1024


class SubmissionForm(forms.Form):
    title = forms.CharField(max_length=255, label="Title")
    larger_work = forms.CharField(max_length=255, label="Larger Work")
    composer = forms.CharField(max_length=200, label="Musical Composer")
    author = forms.CharField(max_length=200, label="Text Author")
    initial_key = forms.ChoiceField(
        choices=Record.INITIAL_KEY_CHOICES,
        widget=KeySignatureWidget(),
        label="Initial Musical Key",
    )
    style = forms.ChoiceField(
        choices=[("", "Select a style")] + Record.STYLE_CHOICES,
        label="Performance Style",
    )
    clef_range = forms.ChoiceField(
        choices=[("", "Not specified"), ("treble", "Treble"), ("bass", "Bass")],
        required=False,
    )

    performing_forces = forms.ChoiceField(
          choices=Record.PERFORMING_FORCES_CHOICES,
          widget=forms.RadioSelect,
          initial='',
          label='Is this MIDI file from an ensemble piece, or a soloistic piece?',
    )

    voice_part = forms.ChoiceField(
      choices=Record.VOICE_PART_CHOICES,
      required=False,
      label='Voice Part',
    )

    midi_file = forms.FileField(label="MIDI File")
    keep_private = forms.BooleanField(
        required=False,
        label="Keep this submission private (skip public review)",
    )

    def clean_midi_file(self):
        midi_file = self.cleaned_data["midi_file"]
        if midi_file.size > MAX_MIDI_SIZE:
            raise forms.ValidationError("File is too large. Maximum size is 5MB.")
        midi_file = self.cleaned_data["midi_file"]
        if not midi_file.name.lower().endswith((".mid", ".midi")):
            raise forms.ValidationError("File must be a .mid or .midi file.")
        return midi_file

    class Meta:
        model = Record
        fields = [
            'title',
            'larger_work',
            'composer',
            'author',
            'initial_key',
            'style',
            'clef_range',
            'performing_forces',
            'voice_part',
        ]

    def clean(self):
        cleaned_data = super().clean()
        performing_forces = cleaned_data.get('performing_forces')
        voice_part = cleaned_data.get('voice_part')

        if performing_forces == 'ensemble' and not voice_part:
            self.add_error(
                'voice_part', 'Please select a voice part for ensemble pieces.')
        return cleaned_data
    

class ReviewerEditForm(forms.ModelForm):
    midi_file = forms.FileField(
        required=False, 
        label="Replace MIDI file (optional)"
    )

    initial_key = forms.ChoiceField(
        choices=Record.INITIAL_KEY_CHOICES,
        widget=KeySignatureWidget(),
        label="Initial Musical Key",
        required=False,
    )
    style = forms.ChoiceField(
        choices=[("", "Select a style")] + list(Record.STYLE_CHOICES),
        required=False,
    )
    clef_range = forms.ChoiceField(
        choices=[("", "Not specified"), ("treble", "Treble"), ("bass", "Bass")],
        required=False,
    )
    performing_forces = forms.ChoiceField(
        choices=Record.PERFORMING_FORCES_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Is this MIDI file from an ensemble piece, or a soloistic piece?",
    )
    voice_part = forms.ChoiceField(
        choices=Record.VOICE_PART_CHOICES,
        required=False,
        label="Voice Part",
    )

    class Meta:
        model = Record
        fields = [
            'title',
            'larger_work',
            'composer',
            'author',
            'initial_key',
            'style',
            'clef_range',
            'performing_forces',
            'voice_part',
        ]

    def clean_midi_file(self):
        midi_file = self.cleaned_data.get("midi_file")
        if midi_file:
            if midi_file.size > MAX_MIDI_SIZE:
                raise forms.ValidationError("File is too large. Maximum size is 5MB.")
            if not midi_file.name.lower().endswith((".mid", ".midi")):
                raise forms.ValidationError("File must be a .mid or .midi file.")
        return midi_file

    def clean(self):
        cleaned_data = super().clean()
        performing_forces = cleaned_data.get("performing_forces")
        voice_part = cleaned_data.get("voice_part")

        if performing_forces == "ensemble" and not voice_part:
            self.add_error(
                "voice_part", "Please select a voice part for ensemble pieces."
            )
        return cleaned_data

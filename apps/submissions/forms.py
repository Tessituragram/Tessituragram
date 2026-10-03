from django import forms
from apps.records.models import Record

from apps.submissions.widgets import KeySignatureWidget


MAX_MIDI_SIZE = 5 * 1024 * 1024

UNKNOWN = "unknown"
NA = "n/a"
EXTRA_CHOICES = [(UNKNOWN, "Unknown"), (NA, "N/A")]
UNKNOWN_CHOICES = [(UNKNOWN, "Unknown")]

UNKNOWN_NA_FIELDS = [
    "title", "larger_work", "composer", "author",
    "style", "voice_part",
]

UNKNOWN_FIELDS = [
    "written_clef_range", "initial_key"
]


class UnknownNAMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in UNKNOWN_NA_FIELDS:
            field = self.fields[name]

            if isinstance(field, forms.ChoiceField):
                existing = {str(v) for v, _ in field.choices}
                field.choices = list(field.choices) + [
                    c for c in EXTRA_CHOICES
                    if c[0] not in existing
                ]

            field.widget.attrs["data-unknown-na"] = "1"

        for name in UNKNOWN_FIELDS:
            field = self.fields[name]

            if isinstance(field, forms.ChoiceField):
                existing = {str(v) for v, _ in field.choices}
                field.choices = list(field.choices) + [
                    c for c in UNKNOWN_CHOICES
                    if c[0] not in existing
                ]

            field.widget.attrs["data-unknown"] = "1"


class SubmissionForm(UnknownNAMixin, forms.Form):
    title = forms.CharField(
        max_length=255,
        label="Title",
    )

    larger_work = forms.CharField(
        max_length=255,
        label="Larger Work",
    )

    composer = forms.CharField(
        max_length=200,
        label="Musical Composer",
    )

    author = forms.CharField(
        max_length=200,
        label="Text Author",
    )

    initial_key = forms.ChoiceField(
        choices=Record.INITIAL_KEY_CHOICES,
        widget=KeySignatureWidget(),
        label="Initial Musical Key",
    )

    style = forms.ChoiceField(
        choices=[("", "Select a style")] + Record.STYLE_CHOICES,
        label="Performance Style",
    )

    style_other = forms.CharField(
        required=False,
        label="Specify Other Style",
        widget=forms.TextInput(
            attrs={
                "id": "style_other",
                "placeholder": "Enter performance style...",
            }
        ),
    )

    written_clef_range = forms.ChoiceField(
        choices=[
            ("", "Select clef range"),
            ("treble", "Treble"),
            ("bass", "Bass"),
            ("unknown", "Unknown"),
        ],
        required=True,
        label="Original Clef",
    )

    # performing_forces = forms.ChoiceField(
    #     choices=Record.PERFORMING_FORCES_CHOICES,
    #     widget=forms.RadioSelect,
    #     initial="solo",
    # )

    voice_part = forms.ChoiceField(
        choices=Record.VOICE_PART_CHOICES,
        required=False,
        label="Voice Part",
    )

    midi_file = forms.FileField(
        label="MIDI File",
    )

    additional_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": (
                    "Add any notes or context for the reviewer "
                    "(optional)..."
                ),
            }
        ),
        label="Additional Comments "
              "(these will only be viewable by website admin)",
    )

    def clean_midi_file(self):
        midi_file = self.cleaned_data["midi_file"]

        if midi_file.size > MAX_MIDI_SIZE:
            raise forms.ValidationError(
                "File is too large. Maximum size is 5MB."
            )

        if not midi_file.name.lower().endswith((".mid", ".midi")):
            raise forms.ValidationError(
                "File must be a .mid or .midi file."
            )

        return midi_file

    def clean(self):
        cleaned_data = super().clean()

        performing_forces = cleaned_data.get("performing_forces")
        voice_part = cleaned_data.get("voice_part")

        if performing_forces == "ensemble":
            if not voice_part:
                self.add_error(
                    "voice_part",
                    "Please select a voice part for ensemble pieces.",
                )
        else:
            cleaned_data["voice_part"] = ""

        style = cleaned_data.get("style")
        style_other = (cleaned_data.get("style_other") or "").strip()

        if style == "other":
            if not style_other:
                self.add_error(
                    "style_other",
                    "You must specify the performance style when "
                    "'Other' is selected.",
                )
            else:
                cleaned_data["style_other"] = style_other
        else:
            cleaned_data["style_other"] = ""

        return cleaned_data
    

class ReviewerEditForm(UnknownNAMixin, forms.Form):
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

    style_other = forms.CharField(
        required=False,
        label="Specify Other Style",
        widget=forms.TextInput(
            attrs={
                "id": "style_other",
                "placeholder": "Enter performance style...",
            }
        ),
    )

    written_clef_range = forms.ChoiceField(
        choices=[
            ("", "Select clef range"),
            ("treble", "Treble"),
            ("bass", "Bass"),
            ("unknown", "Unknown"),
        ],
        required=True,
        label="Original Clef",
    )

    performing_forces = forms.ChoiceField(
        choices=Record.PERFORMING_FORCES_CHOICES,
        widget=forms.RadioSelect,
    )

    voice_part = forms.ChoiceField(
        choices=Record.VOICE_PART_CHOICES,
        required=False,
        label="Voice Part",
    )

    midi_file = forms.FileField(
        required=False,
        label="Replace MIDI File",
    )

    additional_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Add any notes or context for the reviewer...",
            }
        ),
        label="Additional Comments",
    )

    def clean_midi_file(self):
        midi_file = self.cleaned_data.get("midi_file")

        if not midi_file:
            return None

        if midi_file.size > MAX_MIDI_SIZE:
            raise forms.ValidationError(
                "File is too large. Maximum size is 5MB."
            )

        if not midi_file.name.lower().endswith((".mid", ".midi")):
            raise forms.ValidationError(
                "File must be a .mid or .midi file."
            )

        return midi_file

    def clean(self):
        cleaned_data = super().clean()

        performing_forces = cleaned_data.get("performing_forces")
        voice_part = cleaned_data.get("voice_part")

        if performing_forces == "ensemble":
            if not voice_part:
                self.add_error(
                    "voice_part",
                    "Please select a voice part for ensemble pieces.",
                )
        else:
            cleaned_data["voice_part"] = ""

        style = cleaned_data.get("style")
        style_other = (cleaned_data.get("style_other") or "").strip()

        if style == "other":
            if not style_other:
                self.add_error(
                    "style_other",
                    "You must specify the performance style when 'Other' is selected.",
                )
            else:
                cleaned_data["style_other"] = style_other
        else:
            cleaned_data["style_other"] = ""

        return cleaned_data

# apps/submissions/widgets.py
from django import forms


class KeySignatureWidget(forms.RadioSelect):
  template_name = "submissions/widgets/key_signature_radio.html"

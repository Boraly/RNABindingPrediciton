from django import forms


class TextInputForm(forms.Form):
    text_input = forms.CharField(
        label='Copy and paste the text here.',
        widget=forms.Textarea
    )

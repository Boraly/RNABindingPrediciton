from django import forms


class PredictionForm(forms.Form):
    text_input = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label='Text eingeben:'
    )
    file_input = forms.FileField(label='Datei hochladen:')
    predictor_select = forms.ChoiceField(
        choices=[('species1', 'Species 1 Predictor'), ('species2', 'Species 2 Predictor')],
        label='Predictor auswählen:'
    )

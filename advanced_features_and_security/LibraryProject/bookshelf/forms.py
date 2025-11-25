# bookshelf/forms.py

from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'forbidden' in title.lower():
            raise forms.ValidationError("The title contains forbidden words.")
        return title
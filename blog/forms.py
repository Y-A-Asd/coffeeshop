from django import forms


class GenerateBlogForm(forms.Form):
    title = forms.CharField(max_length=255)
    thumbnail = forms.ImageField(required=False)
    content = forms.CharField(widget=forms.Textarea())

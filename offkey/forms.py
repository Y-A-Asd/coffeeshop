from django import forms


class GetOff(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

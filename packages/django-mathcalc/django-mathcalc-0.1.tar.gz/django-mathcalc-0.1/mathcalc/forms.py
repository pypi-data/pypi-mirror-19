from django import forms


CHOICES = (
    ('circle', 'Area of Circle',),
    ('rect', 'Perimeter of Circle',)
)

class OptForm(forms.Form):
    shape_choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,)

class CircleAreaForm(forms.Form):
    radius_value = forms.CharField(max_length=5)

class RectanglePerimeterForm(forms.Form):
    length_value = forms.CharField(max_length=5)
    breadth_value = forms.CharField(max_length=5)


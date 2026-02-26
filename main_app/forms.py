from django import forms
from .models import Feeding


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']

        widgets = {
            'date': forms.DateInput(
                attrs = {
                    # 'type': 'date'
                    # To hide the non-JS datepicker, replace above with:
                    type: "text",
                    "placeholder": "YYYY-MM-DD",
                    "class": "datepicker"
                }
            )
        }

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class ReportcheckForm(forms.Form):
    CHOICES = [('0', '駁回'), ('1', '核可')]
    check = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="", label_suffix="", initial="0")
                                #widget=forms.Textarea(attrs={'class':'form-control transparent','rows':12, 'cols':14}))

    def clean_check(self):
        data = self.cleaned_data['check']
        # Check if there is no data.
        if len(data) < 1 :
            raise ValidationError(_("can't be empty!"))

        # Remember to always return the cleaned data.
        return data

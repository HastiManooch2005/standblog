from django import forms
from .models import Message


# tamrin
class ConcatForm(forms.Form):
    year_choises = ["1991", "2000", "2011", "2012", "2013", "2014", "2015", "2016"]
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(
            years=year_choises, attrs={"class": "form-control"}
        )
    )
    text = forms.CharField(label="text)")

    def clean_text(
        self,
    ):  # brary field khas shart bezarim bade clean esm field migozarim

        text = self.cleaned_data.get("text")  # method get
        if text == "":
            raise ValidationError("text is empty", code="empty")  # in code mesl klid
        return text  # bayad bashe baray marbot be field khas


# class MessageForm(forms.Form):
# title = forms.CharField(label='message')
# text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
# email = forms.EmailField(label='email')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message  # yani az kodam model
        fields = "__all__"  # che field haie
        # exclude =('date')  #hame field ha be joz kodam vaghti in bashe nabayad field bashe
        # baray style dadan ya mitavanim az ketabkhane  django-widget-tweaks
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your message"}
            )
        }

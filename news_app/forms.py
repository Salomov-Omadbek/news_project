from django import forms
from .models import Contacts,Comment

class ContactsForm(forms.ModelForm):

    class Meta:
        model = Contacts
        fields = '__all__'
class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

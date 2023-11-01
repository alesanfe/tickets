from django import forms
from .models import Tickets

class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ['title', 'description', 'ticket_date', 'status', 'finish_date', 'last_used', 'type_ticket']

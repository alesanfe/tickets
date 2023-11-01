from django.contrib import admin
from .models import Tickets
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Tickets


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'user', 'title', 'status', 'ticket_date', 'finish_date')
    list_filter = ('status', 'ticket_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'ticket_date'




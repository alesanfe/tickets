from django.urls import path

from tickets_app.views import home, all_tickets, tickets_details, use_ticket, create_tickets, assign_ticket, \
    unassigned_tickets

urlpatterns = [
    path('', home, name='home'),
    path('tickets/', all_tickets, name='all'),
    path('details/<str:ticket_id>/', tickets_details, name='details'),
    path('use/<str:ticket_id>', use_ticket, name='use'),
    path('create/', create_tickets, name='create'),
    path('assign/<str:ticket_id>/<int:user_id>', assign_ticket, name='assign'),
    path('unassigned/', unassigned_tickets, name='unassigned')

]
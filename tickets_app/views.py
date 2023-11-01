from datetime import datetime, timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from user_management.models import User
from .forms import TicketsForm
from .models import Tickets
from .utils import generate_qr_code


def home(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = Tickets.objects.get(uuid=ticket_id)
        print(ticket.user)
        if ticket.user is None:
            ticket.user = request.user
            ticket.save()
            return render(request, 'tickets/details.html',
                            {'ticket': ticket, 'message': 'Ticket was successfully assigned', 'status': 'Success'})
        else:
            return render(request, 'tickets/details.html',
                            {'ticket': ticket, 'message': 'Ticket is already assigned', 'status': 'Error'})
    return render(request, 'tickets/home.html')


@user_passes_test(lambda u: u.email_verified)
def all_tickets(request):
    user = request.user
    if user.is_superuser:
        tickets = Tickets.objects.all().order_by('-ticket_date')
    else:
        tickets = Tickets.objects.filter(user=user).order_by('-ticket_date')
    return render(request, 'tickets/all.html', {'tickets': tickets})


@user_passes_test(lambda u: u.email_verified)
def tickets_details(request, ticket_id):
    print(ticket_id)
    ticket = get_object_or_404(Tickets, uuid=ticket_id)
    qrcode = generate_qr_code(request, 'use', ticket_id)
    users = []
    if request.user.is_superuser:
        users = User.objects.all()
    return render(request, 'tickets/details.html', {'ticket': ticket, 'qrcode': qrcode, 'users': users})


@user_passes_test(lambda u: u.email_verified)
def use_ticket(request, ticket_id):
    ticket = get_object_or_404(Tickets, uuid=ticket_id)

    if ticket.status == 'Used':
        return render(request, 'tickets/details.html',
                      {'ticket': ticket, 'message': 'Ticket is already used!!!', 'status': 'Error'})

    if ticket.type_ticket == 'Day':
        ticket.status = 'Used'
        ticket.save()
        return render(request, 'tickets/details.html',
                      {'ticket': ticket, 'message': 'Ticket was successfully used.', 'status': 'Success'})

    fecha_actual = datetime.now().date()
    fecha_anterior = ticket.last_used - timedelta(days=1)

    if fecha_anterior < fecha_actual <= ticket.finish_date:
        return redirect('tickets/details.html',
                        {'ticket': ticket, 'message': 'Ticket was successfully used', 'status': 'Success'})
    elif fecha_actual > ticket.finish_date:
        ticket.status = 'Used'
        ticket.save()
        return render(request, 'tickets/details.html',
                      {'ticket': ticket, 'message': 'Ticket has expired', 'status': 'Error'})
    else:
        return render(request, 'tickets/details.html',
                      {'ticket': ticket, 'message': 'Ticket is already used!!!', 'status': 'Error'})


# Admin
@user_passes_test(lambda u: u.is_superuser and u.email_verified)
def create_tickets(request):
    if request.method == 'POST':
        now = datetime.now()
        one_year = now + timedelta(days=365)
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        ticket_date = request.POST.get('ticket_date')
        if ticket_date:
            ticket_date = datetime.strptime(ticket_date, '%m/%d/%Y').date()
        else:
            ticket_date = now
        status = request.POST.get('status', 'Not Used')
        finish_date = request.POST.get('finish_date')
        if finish_date:
            finish_date = datetime.strptime(finish_date, '%m/%d/%Y').date()
        else:
            finish_date = one_year
        type_ticket = request.POST.get('type_ticket', 'Day')
        num_tickets = int(request.POST.get('num_tickets', 0))  # Obtener el número de tickets del request


        for _ in range(num_tickets):
            Tickets.objects.create(
                user=None,
                title=title,
                description=description,
                ticket_date=ticket_date,
                status=status,
                finish_date=finish_date,
                last_used=None,
                type_ticket=type_ticket
            )

        tickets = Tickets.objects.all().order_by('-ticket_date')
        return render(request, 'tickets/all.html', {'tickets': tickets})
    else:
        form = TicketsForm()
        return render(request, 'tickets/create.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser and u.email_verified)
def assign_ticket(request, ticket_id, user_id):
    user = get_object_or_404(User, id=user_id)
    ticket = get_object_or_404(Tickets, uuid=ticket_id)
    ticket.user = user
    ticket.save()
    tickets = Tickets.objects.all().order_by('-ticket_date')
    return render(request, 'tickets/all.html', {'tickets': tickets})

@user_passes_test(lambda u: u.is_superuser and u.email_verified)
def unassigned_tickets(request):
    tickets = Tickets.objects.filter(user=None).order_by('-ticket_date')
    return render(request, 'tickets/all.html', {'tickets': tickets})

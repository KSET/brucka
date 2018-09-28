# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from tickets import printer
from tickets.models import Student, Ticket
from tickets.forms import StudentForm


# !view
def search_students(query, status):
    students = Student.objects.all()
    if status == '0':
        students = students.filter(ticket__isnull=True)
    elif status == '1':
        students = students.filter(ticket__isnull=False)
    for (i, q) in enumerate(query.split(' ')):
        if not q:
            continue
        students = students.filter(Q(first_name__istartswith=q) | Q(last_name__istartswith=q) |
                                   Q(code__contains=q) | Q(email__istartswith=q) |
                                   Q(ticket__number__istartswith=q))
    return students


@login_required
def student_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    students = search_students(query, status)
    return render(request, 'tickets/student/list.html', {
        'students': students,
        'query': query,
        'status': status,
    })


@login_required
def student_export(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    students = search_students(query, status)
    response = HttpResponse(printer.students_pdf(students), content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % 'Brucosi_Karte.pdf'
    return response


@login_required
def dates_export(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    students = search_students(query, status)
    response = HttpResponse(printer.dates_pdf(students), content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % 'Prodane_Karte.pdf'
    return response


@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('tickets:student_edit', student_id=student.id)
    return render(request, 'tickets/student/edit.html', {
        'student': student,
        'form': form,
    })


@login_required
def student_buy_ticket(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if student.ticket_or_none:
        raise PermissionDenied
    ticket = Ticket.objects.create(student=student)
    msg = u'Karta %s za brucoša %s je uspješno kupljena' % (ticket.number, unicode(student))
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('tickets:student_send_mail', student_id=student.id)


@login_required
def student_send_mail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not student.ticket_or_none:
        raise PermissionDenied
    if send_confirmation_mail(student):
        msg = u'Poslan je e-mail s potvrdom o kupljenoj karti na adresu %s' % student.email
        messages.add_message(request, messages.INFO, msg)
    else:
        msg = u'Trenutačno se ne može poslati e-mail s potvrdom o kupljenoj karti na adresu %s' % student.email
        messages.add_message(request, messages.ERROR, msg)
    return redirect('tickets:student_list')


# !view
def send_confirmation_mail(student):
    subject = u'[Brucosijada FER-a] Potvrda o kupljenoj karti'
    message = render_to_string('tickets/student/mail.html', {'student': student})
    recipients = [student.email]
    try:
        send_mail(subject, message, None, recipients)
        return True
    except Exception:
        return False

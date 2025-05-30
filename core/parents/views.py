from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Parent, Student

def parent_login(request):
    """
    Handle parent login via student's admission number and parent's password.
    """
    if request.method == 'POST':
        adm_number = request.POST.get('adm_number')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(registration_number=adm_number)
        except Student.DoesNotExist:
            messages.error(request, "Student with this admission number does not exist.")
            return render(request, 'parent_login.html')

        # Find a parent of this student matching the password
        parent = next((p for p in student.parents.all() if p.check_password(password)), None)

        if parent:
            request.session['parent_id'] = parent.id
            return redirect('parent_dashboard')
        else:
            messages.error(request, "Invalid password for this student.")
    return render(request, 'parent_login.html')

def parent_dashboard(request):
    """
    Display dashboard for logged-in parent.
    """
    parent_id = request.session.get('parent_id')
    if not parent_id:
        return redirect('parent_login')

    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.students.all()
    fees = [getattr(student, 'feebalance', 0) for student in students]
    messages_list = parent.messages.all().order_by('-created_at')
    events = parent.events.all().order_by('event_date')

    context = {
        'parent': parent,
        'students': students,
        'fees': fees,
        'messages': messages_list,
        'events': events,
    }
    return render(request, 'parent_dashboard.html', context)

def parent_logout(request):
    """
    Log out the parent by clearing the session.
    """
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('parent_login')
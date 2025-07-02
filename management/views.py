from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subject, StudentSubject
from .forms import StudentForm, SubjectForm, StudentSubjectForm
from django.contrib import messages

def home(request):
    return render(request, 'management/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'management/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'management/add_student.html', {'form': form})

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'management/subject_list.html', {'subjects': subjects})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'management/add_subject.html', {'form': form})

def student_subjects(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_subjects = StudentSubject.objects.filter(student=student)
    
    # Check if student has exactly 6 subjects
    subject_count = student_subjects.count()
    can_add = subject_count < 6
    requirement_met = subject_count == 6
    
    if request.method == 'POST':
        # Handle subject removal
        if 'remove_subject' in request.POST:
            subject_id = request.POST.get('remove_subject')
            StudentSubject.objects.filter(id=subject_id).delete()
            messages.success(request, 'Subject removed successfully!')
            return redirect('student_subjects', student_id=student_id)
        
        # Handle subject addition
        elif 'add_subject' in request.POST and can_add:
            form = StudentSubjectForm(request.POST)
            if form.is_valid():
                student_subject = form.save(commit=False)
                student_subject.student = student
                
                # Check if student already has this subject
                if StudentSubject.objects.filter(student=student, subject=student_subject.subject).exists():
                    messages.error(request, 'Student already has this subject!')
                else:
                    student_subject.save()
                    messages.success(request, 'Subject added successfully!')
                    return redirect('student_subjects', student_id=student_id)
            else:
                messages.error(request, 'Error adding subject!')
        else:
            messages.error(request, 'Student already has 6 subjects!')
    
    form = StudentSubjectForm(initial={'student': student})
    return render(request, 'management/student_subjects.html', {
        'student': student,
        'student_subjects': student_subjects,
        'form': form,
        'can_add': can_add,
        'requirement_met': requirement_met,
        'subject_count': subject_count,
    })
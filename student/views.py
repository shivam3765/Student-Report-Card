from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.db.models import Q, Sum

from student.models import *


@login_required(login_url="/signin")
def home(request):
    queryset = Student.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(student_name__icontains = search) |
            Q(department__department__icontains = search) |
            Q(student_id__student_id__icontains = search) |
            Q(student_email__icontains = search) |
            Q(student_age__icontains = search) 
            )

    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {"queryset": page_obj})

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "Username already exist.")
            return redirect('/signup/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account Successfully created.")
        return redirect('/signup/')
    
    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid username.")
            return redirect('/signin/')
        
        user = authenticate(request, username = username, password = password)

        if user is None:
            messages.info(request, "Invalid Password.")
            return redirect("/signin/")
        
        else:
            login(request, user)
            return redirect("/")
        
    return render(request, "signin.html")


def logout_page(request):
    logout(request=request)

    return redirect("/signin/")


def see_marks(request, student_id):
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)

    total = queryset.aggregate(total_marks = Sum("marks"))

    return render(request, "see_marks.html", {"queryset": queryset, "total_marks": total})
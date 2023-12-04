from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from itertools import chain
import random
from django.contrib.auth.models import Group, User

student_group, created = Group.objects.get_or_create(name="Student")


def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("login")

    else:
        return render(request, "login.html")


def student_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        course = request.POST["course"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("student_signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("student_signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.is_staff = True
                user.groups.add(student_group)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Students.objects.create(
                    user=user_model,
                    student_id=Students.objects.latest("student_id").student_id + 1,
                    dob=dob,
                    course=Courses.objects.filter(course_name=course).first(),
                )
                course_subjects = Subjects.objects.filter(
                    course_id=Courses.objects.filter(course_name=course).first()
                )
                for subject in course_subjects:
                    new_attendance = Attendance.objects.create(
                        subject_id=subject, student_id=new_profile, percentage=0
                    )
                    new_attendance.save()
                new_profile.save()
                return redirect("student_settings")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("student_signup")

    else:
        courses = Courses.objects.values_list("course_name", flat=True)
        return render(request, "student_signup.html", {"courses": courses})


@login_required(login_url="login")
def dashboard(request):
    student = Students.objects.filter(user=request.user).first()
    subjects = Subjects.objects.filter(course_id=student.course)
    attendance = Attendance.objects.filter(student_id=student)
    current_day = datetime.now().strftime("%A")
    print(student.course.course_name)
    today_time_table = TimeTables.objects.filter(
        course_id=student.course, day=current_day
    )
    att_list_angle = []
    att_list = []
    for subject in subjects:
        for att in attendance:
            if subject == att.subject_id:
                att_list_angle.append((att.percentage * 360) / 100)
                att_list.append(att.percentage)
    return render(
        request,
        "dashboard.html",
        {
            "user_profile": student,
            "subject_attendance": zip(subjects, att_list_angle, att_list),
            "time_table": today_time_table,
            "subjects": subject,
        },
    )


def teacher_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        course = request.POST["course"]
        current_course = Courses.objects.filter(course_name=course).first()

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("student_signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("student_signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.is_staff = True
                user.groups.add(student_group)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Teachers.objects.create(
                    teacher_user=user_model,
                    teacher_id=Teachers.objects.latest("teacher_id").teacher_id + 1,
                    course_id=current_course,
                )
                new_profile.save()
                return redirect("teacher_settings")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("teacher_signup")

    else:
        courses = Courses.objects.values_list("course_name", flat=True)
        return render(request, "teacher_signup.html", {"courses": courses})


@login_required(login_url="login")
def teacher_settings(request):
    user_profile = Teachers.objects.get(teacher_user=request.user)
    subjects = Subjects.objects.filter(course_id=user_profile.course_id)

    if request.method == "POST":
        if request.FILES.get("image") is None:
            image = user_profile.profile_img
        if request.FILES.get("image") is not None:
            image = request.FILES.get("image")

        address = request.POST["address"]
        phone = request.POST["phone"]
        subject = request.POST["subject"]
        current_subject = Subjects.objects.filter(subject_name=subject).first()
        print(current_subject)

        user_profile.profile_img = image
        user_profile.address = address
        user_profile.phone = phone
        user_profile.subject_id = current_subject
        user_profile.save()

        return redirect("teacher_settings")
    return render(
        request,
        "teacher_settings.html",
        {"user_profile": user_profile, "subjects": subjects},
    )


@login_required(login_url="login")
def student_settings(request):
    user_profile = Students.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image") is None:
            image = user_profile.profile_img
        if request.FILES.get("image") is not None:
            image = request.FILES.get("image")

        address = request.POST["address"]
        father_phone = request.POST["father_phone"]
        father_name = request.POST["father_name"]
        mother_name = request.POST["mother_name"]
        mother_phone = request.POST["mother_phone"]
        phone = request.POST["phone"]

        user_profile.profile_img = image
        user_profile.address = address
        user_profile.father_phone = father_phone
        user_profile.father_name = father_name
        user_profile.mother_name = mother_name
        user_profile.mother_phone = mother_phone
        user_profile.phone = phone
        user_profile.save()

        return redirect("student_settings")
    return render(request, "student_settings.html", {"user_profile": user_profile})


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")


def insert(request):
    course_list = Courses.objects.values_list()
    if request.method == "POST":
        subject1 = request.POST["subject1"]
        subject2 = request.POST["subject2"]
        subject3 = request.POST["subject3"]
        subject4 = request.POST["subject4"]
        subject5 = request.POST["subject5"]
        course = request.POST["course"]

        subject_list = [subject1, subject2, subject3, subject4, subject5]
        print("COurse", course)
        current_course = Courses.objects.filter(course_name=course).first()
        for subject in subject_list:
            new_subject = Subjects.objects.create(
                course_id=current_course,
                subject_name=subject,
                subject_credits=random.randint(2, 5),
                subject_id=Subjects.objects.latest("subject_id").subject_id + 1,
            )
            new_subject.save()

    return render(
        request,
        "insert.html",
        {"courses": Courses.objects.values_list("course_name", flat=True)},
    )


def timetable_inserter(request):
    subjects = Subjects.objects.values_list("subject_name", flat=True)
    if request.method == "POST":
        course = request.POST["course"]
        day = request.POST["day"]
        time_table_list = []
        current_course = Courses.objects.filter(course_name=course).first()
        _10t11 = request.POST["10t11"]
        _11t12 = request.POST["11t12"]
        _12t1 = request.POST["12t1"]
        _1t2 = request.POST["1t2"]
        _3t4 = request.POST["3t4"]
        _4t5 = request.POST["4t5"]
        _5t6 = request.POST["5t6"]
        time_table_list = [_10t11, _11t12, _12t1, _1t2, _3t4, _4t5, _5t6]
        time_shift = [[10, 11], [11, 12], [12, 1], [1, 2], [3, 4], [4, 5], [5, 6]]
        if time_table_list[0] is not None:
            for i, time in enumerate(time_table_list):
                tt = TimeTables.objects.create(
                    day=day,
                    course_id=current_course,
                    subject_id=Subjects.objects.filter(subject_name=time).first(),
                    time_start=f"{time_shift[i][0]}:00:00",
                    time_end=f"{time_shift[i][1]}:00:00",
                    type_of_class="Lecture",
                    room_no=random.randint(100, 400),
                )
                tt.save()
    courses = Courses.objects.values_list("course_name", flat=True)
    return render(
        request, "timetable_inserter.html", {"courses": courses, "subjects": subjects}
    )

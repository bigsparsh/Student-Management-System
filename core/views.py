from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from itertools import chain
from datetime import time, timedelta, datetime
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
                    course_id=Courses.objects.filter(course_name=course).first(),
                )
                course_subjects = Subjects.objects.filter(
                    course_id=Courses.objects.filter(course_name=course).first()
                )
                for subject in course_subjects:
                    new_attendance = Attendance.objects.create(
                        subject_id=subject,
                        student_id=new_profile,
                        date=datetime.today().date(),
                        time=datetime.now().time(),
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
    subjects = Subjects.objects.filter(course_id=student.course_id)
    attendance = Attendance.objects.filter(student_id=student)
    current_day = datetime.now().strftime("%A")
    today_time_table = TimeTables.objects.filter(
        course_id=student.course_id, day=current_day
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
            "subject_attendance": zip(subjects, att_list_angle, att_list, attendance),
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
                    user=user_model,
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
    user_profile = Teachers.objects.get(user=request.user)
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

        return redirect("dashboard")
    return render(request, "student_settings.html", {"user_profile": user_profile})


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url="login")
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


@login_required(login_url="login")
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
        time_shift = [
            [10, 11],
            [11, 12],
            [12, 13],
            [13, 14],
            [15, 16],
            [16, 17],
            [17, 18],
        ]
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


@login_required(login_url="login")
def dash_personal_info(request):
    student = Students.objects.filter(user=request.user).first()
    subjects = Subjects.objects.filter(course_id=student.course_id)
    # attendance = Attendance.objects.filter(student_id=student)
    # current_day = datetime.now().strftime("%A")
    return render(
        request,
        "dash_personal_info.html",
        {"user_profile": student, "subjects": subjects},
    )


@login_required(login_url="login")
def dash_time_table(request):
    student = Students.objects.filter(user=request.user).first()
    subjects = Subjects.objects.filter(course_id=student.course_id)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    current_day = datetime.now().strftime("%A")

    day_wize_timetable = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }
    for day in days:
        for time in TimeTables.objects.filter(course_id=student.course_id, day=day):
            day_wize_timetable[day].append(time)
    return render(
        request,
        "dash_time_table.html",
        {
            "user_profile": student,
            "subjects": subjects,
            "day_wize_timetable": day_wize_timetable,
            "current_day": current_day,
        },
    )


@login_required(login_url="login")
def dash_faculty(request):
    student = Students.objects.filter(user=request.user).first()
    teachers = Teachers.objects.filter(course_id=student.course_id)
    return render(
        request,
        "dash_faculty.html",
        {
            "user_profile": student,
            "teachers": teachers,
        },
    )


@login_required(login_url="login")
def dash_notification(request):
    student = Students.objects.filter(user=request.user).first()
    notifications = Notifications.objects.filter(course_id=student.course_id)
    return render(
        request,
        "dash_notification.html",
        {
            "user_profile": student,
            "notifications": notifications,
        },
    )


@login_required(login_url="login")
def dash_change_pass(request):
    student = Students.objects.filter(user=request.user).first()
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        user = student.user
        if not user.check_password(old_password):
            print("Old password is incorrect")
            return redirect("dash_change_pass")
        user.set_password(new_password)
        user.save()
        return redirect("logout")
    return render(request, "dash_change_pass.html", {"user_profile": student})


def teacher_dashboard(request):
    teacher = Teachers.objects.filter(user=request.user).first()
    subjects = Subjects.objects.filter(course_id=teacher.course_id)

    current_day = datetime.now().strftime("%A")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_wize_timetable = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }
    for day in days:
        for time in TimeTables.objects.filter(course_id=teacher.course_id, day=day):
            day_wize_timetable[day].append(time)
    return render(
        request,
        "teacher_time_table.html",
        {
            "user_profile": teacher,
            "subjects": subjects,
            "day_wize_timetable": day_wize_timetable,
            "current_day": current_day,
        },
    )


def td_course_students(request):
    teacher = Teachers.objects.filter(user=request.user).first()
    students = Students.objects.filter(course_id=teacher.course_id)
    return render(
        request,
        "td_course_students.html",
        {"user_profile": teacher, "students": students},
    )


def td_notification(request):
    teacher = Teachers.objects.filter(user=request.user).first()
    return render(
        request,
        "td_notification.html",
        {
            "user_profile": teacher,
        },
    )


def td_upload_attendance(request):
    teacher = Teachers.objects.filter(user=request.user).first()
    return render(
        request,
        "td_upload_attendance.html",
        {
            "user_profile": teacher,
        },
    )


def td_mark_attendance(request):
    teacher = Teachers.objects.filter(user=request.user).first()
    students = Students.objects.filter(course_id=teacher.course_id)
    current_time = datetime.now().time()
    today_date = datetime.today().date()
    current_day = datetime.now().strftime("%A")
    subjects = TimeTables.objects.filter(day=current_day, course_id=teacher.course_id)
    current_subject = None
    for subject in subjects:
        if subject.time_start <= current_time <= subject.time_end:
            current_subject = subject
    if Attendance.objects.filter(
        subject_id=current_subject.subject_id, date=today_date, teacher_id=teacher
    ).first():
        print("SDf")
        current_subject = None
    return render(
        request,
        "td_mark_attendance.html",
        {
            "user_profile": teacher,
            "current_subject": current_subject,
            "students": students,
        },
    )

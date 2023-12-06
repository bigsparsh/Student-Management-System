from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("student_signup/", views.student_signup, name="student_signup"),
    path("teacher_signup/", views.teacher_signup, name="teacher_signup"),
    path("teacher_settings/", views.teacher_settings, name="teacher_settings"),
    path("student_settings/", views.student_settings, name="student_settings"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "dashboard/dash_personal_info",
        views.dash_personal_info,
        name="dash_personal_info",
    ),
    path(
        "dashboard/dash_time_table",
        views.dash_time_table,
        name="dash_time_table",
    ),
    path(
        "dashboard/dash_faculty",
        views.dash_faculty,
        name="dash_faculty",
    ),
    path(
        "dashboard/dash_notification",
        views.dash_notification,
        name="dash_notification",
    ),
    path(
        "dashboard/dash_change_pass",
        views.dash_change_pass,
        name="dash_change_pass",
    ),
    path(
        "teacher_dashboard/",
        views.teacher_dashboard,
        name="teacher_dashboard",
    ),
    path(
        "teacher_dashboard/td_course_students",
        views.td_course_students,
        name="td_course_students",
    ),
    path(
        "teacher_dashboard/td_mark_attendance",
        views.td_mark_attendance,
        name="td_mark_attendance",
    ),
    path(
        "teacher_dashboard/td_notification",
        views.td_notification,
        name="td_notification",
    ),
    path(
        "teacher_dashboard/td_change_pass",
        views.td_change_pass,
        name="td_change_pass",
    ),
    path("logout/", views.logout, name="logout"),
    path("insert/", views.insert, name="insert"),
    path("timetable_inserter/", views.timetable_inserter, name="timetable_inserter"),
]

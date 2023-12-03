from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class Courses(models.Model):
    course_name = models.CharField(max_length=100)
    course_id = models.IntegerField()

    def __str__(self):
        return self.course_name


class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.IntegerField()
    profile_img = models.ImageField(
        upload_to="profile_images", default="blank_profile_picture.jpg", null=True
    )
    address = models.CharField(max_length=100, default="")
    phone = models.IntegerField(default=0)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    father_name = models.CharField(max_length=30, default="")
    mother_name = models.CharField(max_length=30, default="")
    father_phone = models.IntegerField(default=0)
    mother_phone = models.IntegerField(default=0)
    dob = models.DateField(default=datetime.now)

    def __str__(self):
        return "{}".format(self.user.username)


class Subjects(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_id = models.IntegerField()
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject_credits = models.IntegerField()

    def __str__(self):
        return "{} | of course {}".format(self.subject_name, self.course_id.course_name)


class TimeTables(models.Model):
    day_choices = (
        ("SUN", "Sunday"),
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    )

    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    day = models.CharField(max_length=30, choices=day_choices, default="Sunday")
    room_no = models.IntegerField(default=0)
    type_of_class = models.CharField(
        max_length=10, choices=(("LEC", "Lecture"), ("LAB", "Lab")), default="Lecture"
    )

    def __str__(self):
        return "{} | of course {}, from {} to {} on {}".format(
            self.subject_id.subject_name,
            self.course_id.course_name,
            self.time_start,
            self.time_end,
            self.day,
        )


class Teachers(models.Model):
    teacher_user = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField()
    profile_img = models.ImageField(
        upload_to="profile_images", default="blank_profile_picture.jpg", null=True
    )
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, default="")
    phone = models.IntegerField(default=0)

    def __str__(self):
        return "{} | of course {} teaches {}".format(
            self.teacher_user.username,
            self.course_id.course_name,
            self.subject_id.subject_name,
        )


class Notifications(models.Model):
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "Message: {}, sent by {} on {} for course {}".format(
            self.message,
            self.teacher_id.teacher_name,
            self.date,
            self.course_id.course_name,
        )


class Attendance(models.Model):
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    percentage = models.IntegerField()

    def __str__(self):
        return "{} has {}% attendance in {}".format(
            self.student_id.student_name, self.percentage, self.subject_id.subject_name
        )
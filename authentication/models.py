from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TEACHING_CHOICES = (("private", "personally, privately"),
                        ("professional", "personally, professionally"),
                        ("online", "online"),
                        ("other", "other"))
    AUDITION_CHOICES = (("no", "Currently no"),
                        ("small", "I have small audition"),
                        ("sufficient", "I have sufficient audition"))

    email = models.EmailField("Email", unique=True, blank=False)
    full_name = models.CharField("Full Name", max_length=255, blank=False)
    is_mentor = models.BooleanField("Are you mentor?", default=False)
    is_superuser = models.BooleanField(default=False)
    type_of_teaching = models.CharField(help_text="What kind of teaching have you done before?", max_length=25,
                                        choices=TEACHING_CHOICES, default="other")
    audition = models.CharField(help_text="Do you have an audience that you want to share your course with?",
                                max_length=25,
                                choices=AUDITION_CHOICES, default="no")
    finished_registration = models.BooleanField(default=False)
    reset_uuid = models.CharField(max_length=64, null=True, blank=True, default=None)
    reset_datetime = models.DateTimeField(default=None, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "password"]



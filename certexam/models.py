import secrets
from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


class Battalion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bn")
    group = models.CharField(max_length=150)
    battalion = models.CharField(max_length=150)
    wing = models.CharField(max_length=150, default='Army')

    def __str__(self):
        return f'{self.battalion} of {self.group} group'


class School(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_schools")
    school = models.CharField(verbose_name='Institute', max_length=150)
    wing = models.CharField(max_length=150, default='Army')

    def save(self, *args, **kwargs):
        self.wing = self.user.user_bn.first().wing
        return super(School, self).save(*args, **kwargs)

    def __str__(self):
        return f'school {self.school} in  {self.user.username} '


class Cadet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cadet")
    first_name = models.CharField(max_length=150)
    sec_name = models.CharField(verbose_name='Last Name', max_length=150)
    dob = models.DateField(verbose_name='Date of Birth')
    age = models.CharField(max_length=150)
    gender = models.CharField(max_length=150, default='Male')
    number = models.IntegerField(verbose_name='NCC Number')
    school = models.CharField(max_length=150)
    standard = models.CharField(max_length=150, default=12)
    unit = models.CharField(max_length=150, null=True)
    wing = models.CharField(max_length=150, default='Army')
    appeared = models.BooleanField(default=False)
    appeared_date = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(verbose_name='Email Id', help_text='Enter Correct Email id of the student')
    mobile = models.CharField(verbose_name='Mobile Number', max_length=12, help_text='Enter 10 digit mobile number')

    def save(self, *args, **kwargs):
        current_date = datetime.today()
        birth_date = self.dob
        years = current_date.year - birth_date.year if current_date.month > birth_date.month \
            else current_date.year - birth_date.year - 1

        months = current_date.month - birth_date.month if current_date.month > birth_date.month \
            else current_date.month - birth_date.month + 12
        age = f'{years} Years, {months} Months'
        self.age = age
        self.unit = self.user.user_bn.first().battalion
        self.wing = self.user.user_bn.first().wing
        return super(Cadet, self).save(*args, **kwargs)

    def __str__(self):
        return f'Cadet {self.first_name} of {self.user.user_bn.first().battalion}'


class ExamSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_exam_schedule")
    school = models.CharField(max_length=150)
    strength = models.CharField(max_length=150)
    batch = models.CharField(max_length=150)
    date = models.DateField()
    from_time = models.TimeField()
    to = models.TimeField()
    mail_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Schedule {self.school} of {self.user.user_bn.first().battalion}'


class EmailRecord(models.Model):
    cadet = models.ForeignKey(Cadet, on_delete=models.CASCADE, related_name="cadet_email")
    batch = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name="batch_email", blank=True, null=True)
    date_sent = models.DateField(auto_now_add=True)
    initial = models.BooleanField(default=False)
    exam = models.BooleanField(default=False)
    content = models.TextField()
    meet = models.CharField(max_length=150, blank=True, null=True)
    from_time = models.DateTimeField(blank=True, null=True)
    time_to = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Email to {self.cadet.first_name} '


class CompliedScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_compiled_result", blank=True, null=True)
    cadet = models.OneToOneField(Cadet, on_delete=models.CASCADE, related_name="cadet_compiled_result", blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_compiled_result", blank=True, null=True)
    total_marks = models.CharField(max_length=150, blank=True, null=True)
    marks_obtained = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    result = models.CharField(max_length=150, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-percentage', ]

    def __str__(self):
        return f'Compiled result of {self.user.user_bn.first().battalion}'




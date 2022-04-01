from django.contrib import admin

from .models import Battalion, School, Cadet, EmailRecord, ExamSchedule

# Register your models here.

admin.site.register(Battalion)
admin.site.register(School)
admin.site.register(Cadet)
admin.site.register(ExamSchedule)
admin.site.register(EmailRecord)

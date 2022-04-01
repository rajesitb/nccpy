from django.contrib import admin

from .models import Question, SampleQuestion, StudentScore, ExamSchemaSample, ExamSchema

# Register your models here.

admin.site.register(Question)
admin.site.register(SampleQuestion)
admin.site.register(StudentScore)
admin.site.register(ExamSchemaSample)
admin.site.register(ExamSchema)



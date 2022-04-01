from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('view-exam-paper/<str:branch>/<int:pk>/<int:record>/<str:safe>/', views.view_exam_paper,
         name='view-exam-paper'),
    path('paper-schema/', views.paper_schema, name='paper-schema'),
    path('sample-paper/', views.set_questions, name='sample-paper'),
    path('view-exam-paper-popup/', views.view_exam_paper_popup, name='view-exam-paper-popup'),
    path('generate-paper/<wing>/<int:number>/<int:option>/', views.generate_paper, name='generate-paper'),
    path('record-schema/', views.record_schema, name='record-schema'),
    path('show-schema/', views.show_schema, name='show-schema'),
    path('submit-student-answer/', views.submit_student_answer, name='submit-student-answer'),
    path('student-exam-started/', views.student_exam_started, name='student-exam-started'),
    path('student-exam-finished/', views.student_exam_finished, name='thanks'),
    path('amend-schema-field/', views.amend_schema_field, name='amend-schema-field'),
    # sample paper
    path('submit-student-answer-sample/', views.submit_student_answer_sample, name='submit-student-answer-sample'),
    path('test-sample-paper/', views.view_sample_exam_paper, name='test-sample-paper'),

    ]
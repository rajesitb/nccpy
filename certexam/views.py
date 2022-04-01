import datetime
import io
import json
import logging

import pytz
import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView

from online_exam.models import StudentScore, Question, ExamSchema
from .forms import UserRegisterForm, LoginForm, BattalionForm, AddSchoolForm, AddCadetForm
from django.contrib.auth import login, logout
from online_exam.models import army, navy, wing, af
from .models import Battalion, School, Cadet, ExamSchedule, EmailRecord, CompliedScore
from .utils import group_dict
import secrets

# Create your views here.
army_subjects = [x[0] for x in army]
navy_subjects = [x[0] for x in navy]
af_subjects = [x[0] for x in af]
wings = [x[0] for x in wing]
ncc_subjects = {
    'army_wing': army_subjects,
    'navy_wing': navy_subjects,
    'af_wing': af_subjects,
}
ncc_wings = {
    'army_wing': wings[0],
    'navy_wing': wings[1],
    'af_wing': wings[2],
}
wings_reversed = {
    wings[0]: 'army_wing',
    wings[1]: 'navy_wing',
    wings[2]: 'af_wing',
}


def home(request):
    return render(request, 'certexam/home.html')


def banner(request):
    return render(request, 'certexam/banner.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    form = UserRegisterForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        recd_form = UserRegisterForm(request.POST)
        if recd_form.is_valid():
            new_user = recd_form.save(commit=False)
            new_user.save()
            return redirect('login')
        else:
            print(recd_form.errors)

    return render(request, 'certexam/register.html', context)


def login_user(request):
    form = LoginForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('record-unit-data')
    return render(request, 'certexam/login.html', context)


@login_required
def record_data(request):
    try:
        battalion = Battalion.objects.get(user=request.user)
        form = BattalionForm(instance=battalion)
    except Battalion.DoesNotExist:
        battalion = Battalion.objects.none()
        form = BattalionForm()
    context = {
        'form': form,
        'title': 'Unit Data',
    }
    if request.method == 'POST':
        if battalion:
            recd_form = BattalionForm(request.POST, instance=battalion)
        else:
            recd_form = BattalionForm(request.POST)
        data = request.POST
        bn = data.get('battalion')
        recd_form.fields['battalion'].choices = [(bn, bn)]
        if recd_form.is_valid():
            new_unit = recd_form.save(commit=False)
            new_unit.user = request.user
            new_unit.save()
            return redirect('add-school')

    return render(request, 'certexam/select_unit.html', context)


def get_units(request):
    if request.method == 'POST':
        data = request.POST
        group = data.get('group')
        bns = group_dict.get(group)
        return JsonResponse({'response': bns})


@login_required
def add_school(request):
    form = AddSchoolForm
    context = {
        'form': form,
        'title': 'Institute Data',
    }
    if request.method == 'POST':
        school = request.POST.get('input')
        School.objects.create(user=request.user, school=school)
        return JsonResponse({'response': school})

    return render(request, 'certexam/add_school.html', context)


@login_required
def cadet_list(request):
    schools = [x.school for x in School.objects.filter(user=request.user)]
    schools.insert(0, 'Select')
    query_set = Cadet.objects.filter(user=request.user)
    if request.method == 'POST':
        school = request.POST.get('school')
        query_set = Cadet.objects.filter(user=request.user, school=school)
    context = {
        'object_list': query_set,
        'schools': schools,
        'title': 'Cadets',
    }
    return render(request, 'certexam/cadet_list.html', context)


@login_required
def add_cadet(request):
    form = AddCadetForm()
    schools = School.objects.filter(user=request.user)
    form.fields['school'].choices = [(x.school, x.school) for x in schools]
    context = {
        'form': form,
        'title': 'Add cadet',
    }
    if request.method == 'POST':
        form = AddCadetForm(request.POST)
        schools = School.objects.filter(user=request.user)
        form.fields['school'].choices = [(x.school, x.school) for x in schools]
        if form.is_valid():
            logging.warning(f'form is correct')
            new_cadet = form.save(commit=False)
            new_cadet.user = request.user
            new_cadet.save()
            return redirect('cadet-list')
        else:
            logging.warning(f'{form.errors}')
            print(form.errors)
    return render(request, 'certexam/add_cadets.html', context)


def submit_and_add_more(request):
    if request.method == 'POST':
        form = AddCadetForm(request.POST)
        schools = School.objects.filter(user=request.user)
        form.fields['school'].choices = [(x.school, x.school) for x in schools]
        if form.is_valid():
            logging.warning(f'form is correct')
            new_cadet = form.save(commit=False)
            new_cadet.user = request.user
            new_cadet.save()
            return redirect('add-cadet')
        else:
            logging.warning(f'{form.errors}')
            print(form.errors)
    return redirect('add-cadet')


def send_mail_cadets(request):
    data = request.POST
    data_id = data.get('id')
    schedule = ExamSchedule.objects.get(id=int(data_id))
    mail_number = int(schedule.batch)
    cadets = [x for x in Cadet.objects.filter(user=request.user, school=schedule.school)]
    mail_to_cadets = [x for x in cadets if EmailRecord.objects.filter(cadet=x).count() == 0]

    mail_to_be_sent = mail_to_cadets[:mail_number] if len(cadets) > mail_number else cadets
    amended_date = schedule.date
    amended_from = schedule.from_time
    amended_to = schedule.to
    msg = data.get('msg')

    for cadet in mail_to_be_sent:
        send_mail(subject='NCC C Cert Exam', message=f'''
        Dear Cadet {cadet.first_name.capitalize()}.
        Your C Cert Exam Date is {amended_date}, Starting from {amended_from} to {amended_to}.
        We are sending a site familiarization link for you to check out and get used to it.
        Click on         
        https://nccexam.herokuapp.com/test-sample-paper/
        {msg}

        ''', from_email='NCC Ner', recipient_list=[cadet.email], fail_silently=False)
        EmailRecord.objects.create(cadet=cadet, initial=True, content=msg, batch=schedule)

    schedule.mail_sent = True
    schedule.save()
    return JsonResponse({'response': len(mail_to_be_sent)})


@login_required
def schedule_exam(request):
    cadets = Cadet.objects.filter(user=request.user)
    schools = School.objects.filter(user=request.user)
    school_cadets = [(y.school, y.wing, cadets.filter(school=y.school)) for y in schools]
    school_cadet_str = [(x[0], x[1], x[2].count()) for x in school_cadets]

    context = {
        'str': school_cadet_str,
        'title': 'Schedule',
    }
    return render(request, 'certexam/schedule_exam.html', context)


def add_exam_schedule(request):
    data = request.POST
    ExamSchedule.objects.create(school=data.get('school'),
                                strength=data.get('strength'),
                                batch=data.get('batch'),
                                date=data.get('date'),
                                from_time=data.get('from_time'),
                                to=data.get('to_time'),
                                user=request.user)
    return JsonResponse({'response': 'success'})


@login_required
def review_schedule(request):
    schedule = ExamSchedule.objects.filter(user=request.user).order_by('date')
    dates = list(set([x.date for x in schedule]))

    schools = School.objects.filter(user=request.user)
    sch_wise = {}
    for school in schools:
        sch_wise[school.school] = schedule.filter(school=school.school)

    sch = [(date, v.filter(date=date)) for k, v in sch_wise.items() for date in dates]
    vid = [(school.school, v.filter(school=school.school)) for k, v in sch_wise.items() for school in schools]
    school_date = [(date, x[0], x[1].filter(date=date).count(), x[1].filter(date=date)) for x in vid for date in dates
                   if x[1].filter(date=date).count() > 0]

    context = {
        'schedule': schedule,
        'school_date': school_date,
        'title': 'Review',
    }
    return render(request, 'certexam/review_schedule.html', context)


def edit_exam_schedule(request):
    data = request.POST
    data_type = data.get('type')
    data_id = data.get('id')
    data_value = data.get('value')
    exam = ExamSchedule.objects.get(id=int(data_id))
    setattr(exam, data_type, data_value)
    exam.save()

    return JsonResponse({'response': 'success'})


@login_required
def exam_batch(request):
    batches = ExamSchedule.objects.filter(user=request.user).order_by('date')
    context = {
        'batches': batches,
        'title': 'Batches',
    }
    return render(request, 'certexam/exam_batch.html', context)


def add_batch_data(request):
    data = request.POST
    print(data)
    batch = data.get('batch')
    meet_data = data.get('data')
    from_time = data.get('from_time')
    to_time = data.get('to_time')

    if meet_data is not None:
        EmailRecord.objects.filter(batch_id=batch).update(meet=meet_data)
        return JsonResponse({'response': 'success'})
    elif from_time is not None:
        from_time = datetime.datetime.fromisoformat(data.get('from_time'))
        EmailRecord.objects.filter(batch_id=batch).update(from_time=from_time)
        return JsonResponse({'response': 'success'})
    elif to_time is not None:
        to_time = datetime.datetime.fromisoformat(data.get('to_time'))
        EmailRecord.objects.filter(batch_id=batch).update(time_to=to_time)

        return JsonResponse({'response': 'success'})
    return JsonResponse({'response': 'failure'})


def send_exam_mail_cadets(request):
    data = request.POST
    records = EmailRecord.objects.filter(batch=int(data.get('id')))
    emails = [(x.cadet, x.meet,
               x.from_time.astimezone(tz=pytz.timezone('Asia/Kolkata')).strftime("%A, %d. %B %Y %I:%M%p %Z"),
               x.time_to.astimezone(tz=pytz.timezone('Asia/Kolkata')).strftime("%A, %d. %B %Y %I:%M%p %Z"),
               x) for x in records]

    for email in emails:
        send_mail(subject="NCC C Cert Exam Email", message=f'''Dear {email[0].first_name.capitalize()}
        Your Google Meet id is {email[1]}. You have to join the meet before starting the exam.
        The time window of your exam is from {email[2]} upto {email[3]}. The paper can be attempted between this time window only.
        
        We are sending to you your email link for the exam. You have to click on the link to open your test site.
        https://nccexam.herokuapp.com/view-exam-paper/{email[0].wing}/{email[0].id}/{email[4].id}/{secrets.token_urlsafe(16)}/
        ''', from_email='NCC Ner Dte', recipient_list=[email[0].email])
    return JsonResponse({'response': len(emails)})


@login_required
def batch_student_list(request, batch):
    mailed_list = EmailRecord.objects.filter(batch=batch)
    context = {
        'mailed_list': mailed_list,
    }
    return render(request, 'certexam/email_batch_list.html', context)


def result_helper(request, ncc_wing):
    get_wing = ncc_wings.get(ncc_wing)
    print('get_wing', get_wing)
    result = StudentScore.objects.filter(user=request.user, wing=get_wing)
    cadets = Cadet.objects.filter(user=request.user, appeared=True, wing=get_wing)
    subjects = ncc_subjects.get(ncc_wing)
    print(result, cadets, subjects)
    cadet_score = {}
    for cadet in cadets:
        new_result = result.filter(cadet=cadet)
        all_subjects = []
        indl_subjects = []
        total_marks = ExamSchema.objects.none()
        all_subject_total_mks = []
        subject_pass_marks = []
        for subject in subjects:
            sum_subject = [sum(x.score for x in new_result.filter(subject=subject))]
            schema = ExamSchema.objects.filter(wing=cadet.wing, subject=subject).first()
            print(schema)
            marks_per_question = int(schema.marks)
            marks_obtained = sum(x * marks_per_question for x in sum_subject)
            print('printing', sum_subject, schema, marks_obtained)
            pass_percentage = int(schema.pass_percentage) / 100
            subject_total_marks = schema.get_total()
            pass_marks = subject_total_marks * pass_percentage
            subject_result = 'Pass' if marks_obtained > pass_marks else 'Fail'
            percentage_score_cadet = round((marks_obtained / subject_total_marks) / 100)
            indl_subjects.append((subject, subject_total_marks,
                                  round(pass_marks),
                                  marks_obtained, subject_result, percentage_score_cadet))
            all_subjects.append(marks_obtained)
            subject_pass_marks.append(pass_marks)
            all_subject_total_mks.append(schema.get_total())

        final_result = 'passed' if sum(all_subjects) >= sum(subject_pass_marks) else 'failed'

        percentage_score = round((sum(all_subjects) / sum(all_subject_total_mks))*100)
        print('percentage_score', percentage_score)
        cadet_score[cadet] = [sum(all_subjects), sum(all_subject_total_mks),
                              round(sum(subject_pass_marks)),
                              final_result, indl_subjects,
                              'Fail' if 'Fail' in [x[4] for x in indl_subjects] else 'Pass']
        compiled_score = CompliedScore.objects.filter(cadet=cadet)
        if compiled_score.count() == 0:
            CompliedScore.objects.create(cadet=cadet, user=cadet.user,
                                         school=School.objects.get(school=cadet.school),
                                         total_marks=sum(all_subject_total_mks),
                                         marks_obtained=sum(all_subjects),
                                         percentage=percentage_score,
                                         result=cadet_score.get(cadet)[-1])
        elif compiled_score.count() == 1:
            compiled_score.update(marks_obtained=sum(all_subjects),
                                  percentage=percentage_score,
                                  result=cadet_score.get(cadet)[-1]
                                  )
    all_compiled = CompliedScore.objects.all()
    all_percentage = [(x.id, x.percentage) for x in all_compiled if x.result != 'Fail']
    sort_all_percentage = sorted(all_percentage, key=lambda x: x[1], reverse=True)
    print('sort_all_percentage', sort_all_percentage)
    if len(sort_all_percentage) > 0:
        for item in sort_all_percentage:
            position = sort_all_percentage.index(item) + 1
            CompliedScore.objects.filter(id=item[0]).update(position=position)
    context = {
        ncc_wing: {
            'final_result': cadet_score,
        }

    }
    return context


def schema_helper():
    ncc_schema = {}
    for item in wings:
        ncc_schema[item] = []
        for subject in ncc_subjects.get(wings_reversed[item]):
            schema = ExamSchema.objects.filter(wing=item, subject=subject).first()
            if schema:
                total_marks = schema.get_total()
                ncc_schema[item].append([schema.subject, total_marks, total_marks * schema.pass_percentage / 100])
    return ncc_schema


@login_required
def view_exam_result(request):
    army_wing = result_helper(request, 'army_wing')
    navy_wing = result_helper(request, 'navy_wing')
    af_wing = result_helper(request, 'af_wing')
    ncc_schema = schema_helper()

    context = {
        'army': [army_wing, ncc_schema.get('Army'), 'Army Wing'],
        'navy': [navy_wing, ncc_schema.get('Navy'), 'Navy Wing'],
        'af': [af_wing, ncc_schema.get('AF'), 'AF Wing'],
        'title': 'Result',

    }
    return render(request, 'certexam/student_result.html', context)


@login_required
def wing_exam_result(request, branch):
    branch_str = f'{branch.lower()}_wing'
    result_wing = result_helper(request, branch_str)
    ncc_schema = schema_helper()

    context = {
        'branch': [result_wing, ncc_schema.get(branch), f'{branch} Wing', branch],
        'title': 'Result',

    }
    return render(request, 'certexam/student_wing_result.html', context)


def composite_result(request):
    return render(request, 'certexam/composite_result.html', {'title': 'Result'})


def exam_result(request):
    result = StudentScore.objects.filter(user=request.user)
    cadets = Cadet.objects.filter(user=request.user, appeared=True)
    cadet_results = [[y for y in result.filter(cadet=x)]
                     for x in cadets]

    fields = [x.name for x in StudentScore._meta.get_fields()]
    cadet_results_subjects = [list(set(y.subject for y in x)) for x in cadet_results]
    # print(cadet_results_subjects)

    # subject_wise = [result.filter(cadet=x, subject=y) for x in cadets for y in cadet_results_subjects]
    first_cadet = cadet_results[0]
    table = dict.fromkeys(fields, [])

    for x in table.keys():
        for y in first_cadet:
            table[x].append(getattr(first_cadet, y))
    print(table)
    return JsonResponse({'result': 'success'})


def pdf_helper(request, branch):
    branch_str = f'{branch.lower()}_wing'
    result_context = result_helper(request, branch_str)
    ncc_schema = schema_helper()
    context = {
        'branch': [result_context, ncc_schema.get(branch), f'{branch} Wing', branch],

    }
    html = render_to_string('certexam/result_pdf.html', context)
    response = HttpResponse(content_type='Application/pdf')
    return html, response


def print_exam_pdf(request, branch):
    unit = request.user.user_bn.first().battalion
    html, response = pdf_helper(request, branch)

    response['Content-Disposition'] = 'filename = exam_result_%s.pdf'.format(unit)
    # to get images base_url=request.build_absolute_uri()
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()) \
        .write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/bootstrap.css')])
    return response


def send_result_email(request, branch, email_id):
    html, response = pdf_helper(request, branch)

    unit = request.user.user_bn.first().battalion
    subject = f'NCC C Cert Exam Result'
    message = f'Please find attached result of NCC C Cert Exam'
    email = EmailMessage(subject, message, from_email=f'{unit}', to=[email_id])

    out = io.BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/bootstrap.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'result_{unit}', out.getvalue(), 'application/pdf')
    email.send()


@login_required
def result_summary(request):
    summary = CompliedScore.objects.all()
    context = {
        'summary': summary,
        'title': 'Result',
    }
    return render(request, 'certexam/result_summary.html', context)


@login_required
def detailed_result(request, pk):
    cadet = Cadet.objects.get(id=pk)
    schema = ExamSchema.objects.filter(wing=cadet.wing)
    subjects = [x.subject for x in schema]
    result = StudentScore.objects.filter(cadet=cadet)
    subject_result = [(schema.filter(subject=subject).first().marks, result.filter(subject=subject)) for subject in
                      subjects]
    subject_score = [(schema.filter(subject=subject).first().marks, result.filter(subject=subject, score=1).count()) for
                     subject in subjects]
    total_score = sum([(int(x[0]) * x[1]) for x in subject_score])

    context = {
        'results': subject_result,
        'total_score': total_score,
        'cadet': cadet,
        'title': 'Detail result',
    }
    return render(request, 'certexam/detail_result.html', context)


def remove_batch(request):
    data = request.POST
    record = ExamSchedule.objects.get(id=int(data.get('data')))
    record.delete()

    return JsonResponse({'response': 'success'})


@login_required
def show_institutes(request):
    schools = School.objects.filter(user=request.user)
    context = {
        'schools': schools,
        'title': 'Institutes',
    }
    return render(request, 'certexam/show_schools.html', context)


def remove_school(request):
    data = request.POST
    school = School.objects.get(id=int(data.get('data')))
    cadets = Cadet.objects.filter(school=school)
    schedule = ExamSchedule.objects.filter(school=school).delete()
    school.delete()
    cadets.delete()

    return JsonResponse({'response': 'success'})


def remove_cadet(request):
    data = request.POST
    cadets = Cadet.objects.get(id=int(data.get('data')))
    cadets.delete()
    return JsonResponse({'response': 'success'})


class SchoolEdit(LoginRequiredMixin, UpdateView):
    model = School
    form_class = AddSchoolForm
    template_name = 'certexam/school_update_form.html'
    success_url = '/show-institutes/'


@login_required
def cadet_edit(request, pk):
    cadet = Cadet.objects.get(id=pk)
    form = AddCadetForm(instance=cadet)
    schools = School.objects.filter(user=request.user)
    form.fields['school'].choices = [(x.school, x.school) for x in schools]
    context = {
        'form': form,
        'title': 'Edit',
    }
    if request.method == 'POST':

        recd_form = AddCadetForm(request.POST, instance=cadet)
        recd_form.fields['school'].choices = [(x.school, x.school) for x in schools]
        if recd_form.is_valid():
            updated_cadet = recd_form.save(commit=False)
            updated_cadet.save()
            return redirect('cadet-list')
        else:
            print(recd_form.errors)
    return render(request, 'certexam/cadet_update_form.html', context)


def get_question(request):
    data = request.POST
    q_id = data.get('question')
    q = Question.objects.get(id=int(q_id)).question
    return JsonResponse({'response': f'{q}'})


def get_correct_ans(request):
    data = request.POST
    q_id = data.get('question')
    q = Question.objects.get(id=int(q_id))
    answer = f'option_{q.answer}'
    ans = getattr(q, answer)
    return JsonResponse({'response': f'{ans}'})


def get_student_ans(request):
    data = request.POST
    q_id = data.get('question')
    st_answer = data.get('st_answer')
    q = Question.objects.get(id=int(q_id))
    answer = getattr(q, st_answer)
    return JsonResponse({'response': f'{answer}'})


def add_cadet_list(request):
    form = AddCadetForm()
    schools = School.objects.filter(user=request.user)
    form.fields['school'].choices = [(x.school, x.school) for x in schools]
    context = {
        'form': form,
        'title': 'Cadet',
    }
    if request.method == 'POST':
        form = AddCadetForm(request.POST)
        schools = School.objects.filter(user=request.user)
        form.fields['school'].choices = [(x.school, x.school) for x in schools]
        if form.is_valid():
            logging.warning(f'form is correct')
            new_cadet = form.save(commit=False)
            new_cadet.user = request.user
            new_cadet.save()

        else:
            logging.warning(f'{form.errors}')
            print(form.errors)
    return render(request, 'certexam/add_cadet_rowlist.html', context)


error_message = 'Something is not right. We are looking at it. You can also mail your feedback to ' \
                'nerccert@gmail.com'


def handler500(request, exception=None):
    messages.warning(request, error_message)
    if request.user.is_authenticated:

        return redirect('record-unit-data')
    else:
        return redirect('home')


def handler404(request, exception=None):
    return render(request, 'certexam/404.html', status=404)


def handler400(request, exception=None):
    messages.warning(request, f"Oops ...that was a bad request!")

    return redirect('home')


def handler403(request, exception=None):
    messages.warning(request, f"Sorry you dont have permission to view that page")

    return redirect('home')


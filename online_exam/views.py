import datetime
import json
import random

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect

from django.http import JsonResponse
import datetime
from datetime import timedelta

from certexam.models import Cadet, EmailRecord
from .models import army, navy, af, wing, ExamSchema, SampleQuestion, ExamSchemaSample

from django.shortcuts import render

# Create your views here.
from online_exam.models import Question, StudentScore


def view_exam_paper(request, branch, pk, record, safe):
    # if request.session.get('verified'):
    cadet = get_object_or_404(Cadet, id=pk)
    # exam_wing = ExamSchema.objects.filter(wing=branch)
    # create_sample_set(4, exam_wing)
    context = {
        'army_questions': cadet,
    }
    if not cadet.appeared:
        record = get_object_or_404(EmailRecord, id=record)
        batch = record.batch
        exam_from = batch.from_time
        exam_to = batch.to
        gap = datetime.datetime.combine(datetime.datetime.today().date(), exam_to) - \
              datetime.datetime.combine(datetime.datetime.today().date(), exam_from)

        from_time = record.from_time
        time_to = record.time_to
        time_to.astimezone(tz=pytz.utc)
        timezone = pytz.timezone('Asia/Kolkata')
        just_now = datetime.datetime.now(tz=pytz.utc)

        if from_time < just_now < time_to:

            exam_wing = ExamSchema.objects.filter(wing=branch)
            subjects = [x.subject for x in exam_wing]
            exam_sample = create_sample_set(4, exam_wing)
            context = {
                'army_questions': [exam_sample, exam_wing.first().wing, subjects, cadet, gap.seconds],
            }

            return render(request, 'online_exam/exam_paper.html', context)
        else:
            return render(request, 'online_exam/exam_paper.html', context)
    else:
        messages.warning(request, f'Seems you have already attempted !!')

        return render(request, 'online_exam/exam_paper.html', context)
    # else:
    #     return redirect('thanks')


def view_sample_exam_paper(request):
    # if request.session.get('verified'):
    # cadet = get_object_or_404(Cadet, id=pk)
    # exam_wing = ExamSchema.objects.filter(wing='Army')
    # create_sample_set(4, exam_wing)
    # context = {
    #     'army_questions': cadet,
    # }
    exam_wing = ExamSchemaSample.objects.filter(wing='Army')
    subjects = [x.subject for x in exam_wing]
    exam_sample = create_test_sample_set(4, exam_wing)
    time_plot = timedelta(hours=1)
    context = {
        'army_questions': [exam_sample, 'Army', subjects, time_plot.seconds],
    }

    return render(request, 'online_exam/exam_paper_sample.html', context)


def student_exam_started(request):
    data = request.POST
    cadet = Cadet.objects.get(id=data.get('cadet'))
    if cadet.appeared is True:
        return JsonResponse({'response': 'failed'})
    else:

        cadet.appeared = True
        cadet.appeared_date = datetime.datetime.now(tz=pytz.utc)
        request.session['verified'] = True
        request.session['cadet'] = cadet.id
        cadet.save()

        return JsonResponse({'response': 'success'})


def student_exam_finished(request):
    try:
        del request.session['verified']
    except KeyError:
        pass
    return render(request, 'online_exam/exam_finished.html', )


def view_exam_paper_popup(request):
    return render(request, 'online_exam/exam_paper_pop.html')


def generate_paper(request, wing, number, option):
    # number = random.
    questions = Question.objects.filter(wing__contains=wing)
    # [4:10] is to catch the options field. [:option] is for selecting options per question eg 4
    field_option = list(Question.objects.values()[0].keys())[4:10][:option]
    random.shuffle(field_option)
    normal = [x for x in questions]
    random.shuffle(normal)
    selected_questions = normal[:number]
    random_question = {}
    selected_q_options = {}
    for item in selected_questions:
        for i in range(option):
            selected_q_options[i] = getattr(item, field_option[i])
        random_question[item] = selected_q_options

    if request.method == "POST":
        data = request.POST
        ques_id = list(data.keys())[1]
        q = Question.objects.get(id=int(ques_id))
        ans = (list(data.values())[1]).split()[-1]
        if int(ans) == int(q.answer):
            # StudentScore.objects.create(cadet=)
            print('correct')
        else:
            print('incorrect')
        print(ans, q.answer)

    context = {
        'wing': wing,
        'question': random_question
    }
    return render(request, 'online_exam/questions.html', context)


@login_required
def paper_schema(request):
    questions = Question.objects.all()
    army_qp = questions.filter(wing__iexact='army')
    army_sub = [x[1] for x in army]
    army_sub_qp = [(y, army_qp.filter(subject=y)) for y in army_sub]
    navy_qp = questions.filter(wing__iexact='navy')
    navy_sub = [x[1] for x in navy]
    af_qp = questions.filter(wing__iexact='air')
    af_sub = [x[1] for x in af]
    wings = [x[1] for x in wing]
    navy_sub_qp = [(y, navy_qp.filter(subject=y)) for y in navy_sub]
    af_sub_qp = [(y, af_qp.filter(subject=y)) for y in af_sub]
    context = {
        'army_qp': army_qp,
        'army_sub': army_sub,
        'army_sub_qp': army_sub_qp,
        'navy_sub_qp': navy_sub_qp,
        'af_sub_qp': af_sub_qp,
        'navy_qp': navy_qp,
        'navy_sub': navy_sub,
        'af_qp': af_qp,
        'af_sub': af_sub,
        'wings': wings,
    }
    return render(request, 'online_exam/paper_schema.html', context)


def record_schema(request):
    data = request.POST
    subject = data.get('subject')
    ncc_wing = data.get('wing')
    allotted = data.get('allotted')
    marks = data.get('marks')
    pass_percentage = data.get('pass_percentage')
    existing = ExamSchema.objects.filter(subject=subject, wing=ncc_wing)

    if existing.count() > 0:
        existing.update(questions=allotted, marks=marks, pass_percentage=pass_percentage)

    else:
        ExamSchema.objects.create(
            wing=ncc_wing,
            subject=subject,
            questions=allotted,
            marks=marks,
            pass_percentage=pass_percentage,
        )
    return JsonResponse({'response': 'success'})


@login_required
def show_schema(request):
    army_schema = ExamSchema.objects.filter(wing='Army')
    navy_schema = ExamSchema.objects.filter(wing='Navy')
    af_schema = ExamSchema.objects.filter(wing='AF')
    army_total = sum(x.get_total() for x in army_schema)
    navy_total = sum(x.get_total() for x in navy_schema)
    af_total = sum(x.get_total() for x in af_schema)
    context = {
        'army_schema': army_schema,
        'army_total': army_total,
        'navy_total': navy_total,
        'af_total': af_total,
        'navy_schema': navy_schema,
        'af_schema': af_schema
    }
    return render(request, 'online_exam/show_schema.html', context)


@login_required
def set_questions(request):
    # setting std 4 options per question by[:4]
    army_wing = ExamSchema.objects.filter(wing='Army')
    navy_wing = ExamSchema.objects.filter(wing='Navy')
    af_wing = ExamSchema.objects.filter(wing='AF')
    if army_wing.count() > 0:
        army_sample = create_sample_set(4, army_wing)
    else:
        army_sample = None
    if navy_wing.count() > 0:
        navy_sample = create_sample_set(4, navy_wing)
    else:
        navy_sample = None
    if af_wing.count() > 0:
        af_sample = create_sample_set(4, af_wing)
    else:
        af_sample = None

    context = {
        'army_wing': army_wing,
        'navy_wing': navy_wing,
        'af_wing': af_wing,
        'army_questions': [army_sample, army_wing.first().wing],
        'navy_questions': [navy_sample, navy_wing.first().wing],
        'af_questions': [af_sample, af_wing.first().wing],
    }
    return render(request, 'online_exam/sample_paper.html', context)


def create_sample_set(option, service):
    subject = {}
    subject_questions = {}
    for item in service:
        ncc_wing = item.wing
        q_subject = item.subject
        army_questions_qty = int(item.questions)
        questions = Question.objects.filter(wing__contains=ncc_wing, subject=q_subject)

        normal = [x for x in questions]
        random.shuffle(normal)
        selected_questions = normal[:army_questions_qty]
        random_question = {}
        for ques in selected_questions:
            random_question[ques] = []
            field_option_1 = [x.name for x in ques._meta.fields][4:10]
            field_option_2 = field_option_1[:4]
            random.shuffle(field_option_2)
            answer = ques.answer
            ans_option = f'option_{answer}'
            if ans_option not in field_option_2:
                field_option_2.pop(0)
                field_option_2.insert(0, ans_option)
                random.shuffle(field_option_2)
            field_option_value = [(getattr(ques, x), x) for x in field_option_2]
            random_question[ques].append(field_option_value)
            # remove before actual launch
            random_question[ques].append(getattr(ques, ans_option))
        subject_questions[q_subject] = random_question

    return subject_questions


def create_test_sample_set(option, service):
    subject = {}
    for item in service:
        ncc_wing = item.wing
        q_subject = item.subject
        army_questions_qty = int(item.questions)
        questions = SampleQuestion.objects.filter(wing__contains=ncc_wing, subject__contains=q_subject)
        if questions.count() == 0:
            questions = SampleQuestion.objects.filter(wing__contains='air', subject__contains=q_subject)
        field_option = list(SampleQuestion.objects.values()[0].keys())[4:10]
        random.shuffle(field_option)
        field_option = field_option[:option]
        random.shuffle(field_option)
        normal = [x for x in questions]
        random.shuffle(normal)
        selected_questions = normal[:army_questions_qty]
        random_question = {}
        selected_q_options = {}
        for ques in selected_questions:
            random.shuffle(field_option)
            answer = ques.answer
            ans_option = f'option_{answer}'
            if ans_option not in field_option:
                field_option.pop(0)
                field_option.insert(0, ans_option)
                random.shuffle(field_option)
            option_range = list(range(option))
            for i in option_range:
                selected_q_options[i] = [getattr(ques, field_option[i]), field_option[i]]
            random_question[ques] = [selected_q_options, getattr(ques, ans_option), ]
        subject[q_subject] = random_question
    return subject


def submit_student_answer(request):
    data = request.POST

    if request.session.get('verified'):
        ques = Question.objects.get(id=int(data.get('ques')))
        value = int(data.get('val').split('_')[1])
        ans = ques.answer
        score = value == ans
        cadet = Cadet.objects.get(id=int(data.get('cadet')))
        answered = StudentScore.objects.filter(cadet=cadet, question=data.get('ques'))
        StudentScore.objects.create(cadet=cadet, question=data.get('ques'), score=score,
                                    student_answer=data.get('val'),
                                    correct_answer=f'option_{ques.answer}', subject=ques.subject, user=cadet.user)

        return JsonResponse({'response': 'recorded'})
    else:
        return JsonResponse({'response': 'failure'})


def submit_student_answer_sample(request):
    return JsonResponse({'response': 'recorded'})


def amend_schema_field(request):
    data = request.POST
    value = data.get('val')

    new_element = data.get('new_el')
    schema_data = json.loads(new_element)
    schema_id = schema_data['id']
    field = schema_data['fd']
    schema = ExamSchema.objects.get(id=int(schema_id))
    schema.__setattr__(field, value)
    schema.save()

    return JsonResponse({'response': 'success'})


# def compile_score(request):
#     session = request.session.get('verified')
#     if session:
#         cadet_id = request.session.get('cadet')
#         cadet = Cadet.objects.get(id=int(cadet_id))
#         compiled, created = CompliedScore.objects.get_or_create(cadet=cadet,
#                                                                 user=cadet.user,
#                                                                 school=cadet.school)
#         schema = ExamSchema.objects.filter(wing=cadet.wing)
#         max_marks = sum((int(x.marks) * int(x.questions)) for x in schema)
#         compiled.total_marks = max_marks
#         score = StudentScore.objects.filter(cadet=cadet)
#         marks_scored = sum(int(schema.get(subject=y.subject).marks) for y in score if y.score)
#         compiled.marks_obtained = marks_scored




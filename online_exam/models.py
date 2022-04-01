import random
import string

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from certexam.models import Cadet


wing = [
    ('Army', 'Army'),
    ('Navy', 'Navy'),
    ('AF', 'AF')
]
army = [
    ('Armed Forces', 'Armed Forces'),
    ('MR', 'MR'),
    ('Fd Craft/Battle Craft', 'Fd Craft/Battle Craft'),
    ('Mil History', 'Mil History'),
    ('Communication', 'Communication'),
    ('WE', 'WE'),

]
navy = [
    ('NO & GS', 'NO & GS'),
    ('Communication', 'Communication'),
    ('Navigation', 'Navigation'),
    ('Seamanship', 'Seamanship'),
    ('FF, DC & SS', 'FF, DC & SS'),
    ('Ship & BM', 'Ship & BM'),
    ('Swimming', 'Swimming'),

]

af = [
    ('General Service', 'General Service'),
    ('Air Campaign', 'Air Campaign'),
    ('Pr of Flight', 'Pr of Flight'),
    ('Airmanship', 'Airmanship'),
    ('Navigation', 'Navigation'),
    ('Aero Eng', 'Aero Eng'),
    ('BF Inst', 'BF Inst'),
    ('AeroModelling', 'AeroModelling'),

]
combined = [('Army', army), ('Navy', navy), ('AF', af)]
army_subject = [x[0] for x in army]


class Question(models.Model):
    wing = models.CharField(max_length=150, choices=wing, default='Army')
    subject = models.CharField(max_length=150, choices=combined, blank=True, null=True)
    question = models.CharField(max_length=300, blank=True, null=True)
    option_1 = models.CharField(max_length=300, default='Option number 1')
    option_2 = models.CharField(max_length=300, default='Option number 2')
    option_3 = models.CharField(max_length=300, default='Option number 3')
    option_4 = models.CharField(max_length=300, default='Option number 4')
    option_5 = models.CharField(max_length=300, default='Option number 5')
    option_6 = models.CharField(max_length=300, default='Option number 6')
    answer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Question {self.id} '

    def save(self, *args, **kwargs):
        number = Question.objects.all().count()
        if not self.question:
            self.question = f'Question number {number+1}'
        if not self.answer:
            self.answer = random.randrange(1, 5)
        if not self.subject:
            self.subject = combined[0][1][1][1]
        return super(Question, self).save(*args, **kwargs)


class SampleQuestion(models.Model):
    wing = models.CharField(max_length=150, choices=wing, default='Army')
    subject = models.CharField(max_length=150, choices=combined, blank=True, null=True)
    question = models.CharField(max_length=300, blank=True, null=True)
    option_1 = models.CharField(max_length=300, default='Option number 1')
    option_2 = models.CharField(max_length=300, default='Option number 2')
    option_3 = models.CharField(max_length=300, default='Option number 3')
    option_4 = models.CharField(max_length=300, default='Option number 4')
    option_5 = models.CharField(max_length=300, default='Option number 5')
    option_6 = models.CharField(max_length=300, default='Option number 6')
    answer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Question {self.id} '

    def create_question(self):
        o = combined.index(random.choice(combined))
        o1_len = len(combined[o][1])
        o1_r = random.randint(0, o1_len-1)
        subject = combined[o][1][o1_r][1]
        q = SampleQuestion(wing=combined[o][0], subject=subject)
        q.save()

    def save(self, *args, **kwargs):
        number = Question.objects.all().count()
        if not self.question:
            self.question = f'Question number {number+1}'
        if not self.answer:
            self.answer = random.randrange(1, 5)
        if not self.subject:
            self.subject = combined[0][1][1][1]
        return super(SampleQuestion, self).save(*args, **kwargs)


class StudentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_score", blank=True, null=True)
    cadet = models.ForeignKey(Cadet, on_delete=models.CASCADE, related_name="cadet_score")
    wing = models.CharField(max_length=150, blank=True, null=True)
    question = models.CharField(max_length=150)
    subject = models.CharField(max_length=150, blank=True, null=True)
    student_answer = models.CharField(max_length=150, default='option_1')
    correct_answer = models.CharField(max_length=150, default='option_2')
    score = models.IntegerField()

    def get_score(self):
        score = StudentScore.objects.values_list(self.score, flat=True)
        return sum(score)

    def save(self, *args, **kwargs):
        cadet_wing = self.cadet.wing
        self.wing = cadet_wing
        return super(StudentScore, self).save(*args, **kwargs)

    def __str__(self):
        return f'score of {self.cadet.first_name}'


class ExamSchema(models.Model):
    wing = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    questions = models.CharField(verbose_name="Allotted Questions", max_length=150)
    marks = models.CharField(verbose_name="Marks per question", max_length=150)
    pass_percentage = models.IntegerField(default=40)

    def get_total(self):
        return int(self.questions) * int(self.marks)

    def __str__(self):
        return f'schema of {self.wing}, {self.subject}'


class ExamSchemaSample(models.Model):
    wing = models.CharField(max_length=150, default='Army')
    subject = models.CharField(max_length=150)
    questions = models.CharField(verbose_name="Allotted Questions", max_length=150, default=4)
    marks = models.CharField(verbose_name="Marks per question", max_length=150, default=5)
    pass_percentage = models.IntegerField(default=40)

    def get_total(self):
        return int(self.questions) * int(self.marks)

    def create_schema(self):
        for i in range(len(army_subject)):
            ExamSchemaSample.objects.create(subject=army_subject[i])

    def __str__(self):
        return f'schema of {self.wing}, {self.subject}'




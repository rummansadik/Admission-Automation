import json
from datetime import datetime

from django.db import models
from multiselectfield import MultiSelectField
from student.models import Student

subject_choices = (
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('EEE', 'EEE'),
    ('BBA', 'BBA'),
    ('English', 'English'),
    ('Math', 'Math'),
    ('Bangla', 'Bangla'),
)


class University(models.Model):
    university_name = models.CharField(max_length=100)
    subjects = MultiSelectField(
        max_length=100,
        max_choices=7,
        choices=subject_choices
    )


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()

    start_date = models.DateField()
    start_time = models.TimeField()

    end_date = models.DateField()
    end_time = models.TimeField()

    def start_at(self):
        return datetime.combine(
            self.start_date, self.start_time)

    def end_at(self):
        return datetime.combine(
            self.end_date, self.end_time)

    def __str__(self):
        return self.course_name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (
        ('Option1', 'Option1'),
        ('Option2', 'Option2'),
        ('Option3', 'Option3'),
        ('Option4', 'Option4')
    )
    answer = models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


class ShortQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=2000)


class AnswerSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mcqAnswer = models.CharField(max_length=200, blank=True)
    mcqMarks = models.CharField(max_length=200, blank=True)
    shortsAnswer = models.CharField(max_length=2000, blank=True)

    def set_mcq_answer(self, answer):
        self.mcqAnswer = json.dumps(answer)

    def get_mcq_answer(self):
        return json.loads(self.mcqAnswer)

    def set_mcq_marks(self, answer):
        self.mcqMarks = json.dumps(answer)

    def get_mcq_marks(self):
        return json.loads(self.mcqMarks)

    def set_shorts_answer(self, answer):
        self.shortsAnswer = json.dumps(answer)

    def get_shorts_answer(self):
        return json.loads(self.shortsAnswer)

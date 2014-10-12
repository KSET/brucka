# -*- coding: utf-8 -*-
from django import forms
from tickets.models import Student


class StudentForm(forms.ModelForm):

    class Meta():
        model = Student
        exclude = ('code',)

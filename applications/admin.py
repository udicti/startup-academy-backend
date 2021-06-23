
from django.contrib import admin
from .models import *
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.sites.models import Site

class QuestionInline(admin.StackedInline):

    model = ApplicationQuestion
    extra = 0


@admin.register(ApplicationWindow)
class ApplicationWindowAdmin(admin.ModelAdmin):
    list_display = ('open', 'starts', 'ends', 'date_created')
    fields = ('description', 'starts', 'ends', 'open')
    inlines = [
        QuestionInline
    ]

# @admin.register(ApplicationQuestion)
# class ApplicationQuestionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'statement')

class AnswerInline(admin.StackedInline):

    model = Answer
    extra = 0
    insert_after = 'application_window'
    fields = ('to_question', 'statement')

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('to_question',)
        return self.readonly_fields

@admin.register(Applicant)
class ApplicantWindowAdmin(admin.ModelAdmin):
    list_display = ('email', 'university')
    fields=('first_name','last_name','email','mobile','gender','university','degree_program','application_window','is_selected','is_unselected')
    readonly_fields = ('first_name','last_name','email','mobile','gender','university','degree_program','application_window')
    inlines = [
        AnswerInline,
    ]
    
    change_form_template = 'admin/custom/change_form.html'

    class Media:
        css = {
            'all': (
                'css/admin.css',
            )
        }

# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('from_applicant', 'to_question')




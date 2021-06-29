
from django.contrib import admin
from .models import *
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.sites.models import Site


class SelectedListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'selection'

    def lookups(self, request, model_admin):
        return (
            ('selected', ('selected')),
            ('unselected', ('not selected')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'selected':
            return queryset.filter(is_selected = True)
        if self.value() == 'unselected':
            return queryset.filter(is_unselected = True )



class QuestionInline(admin.StackedInline):

    model = ApplicationQuestion
    classes = ['collapse',]
    extra = 0

class ApplicantsInline(admin.StackedInline):

    model = Applicant
    fields = ('degree_program', 'university')
    readonly_fields =('degree_program', 'university')
    classes = ['collapse',]
    can_delete = False
    show_change_link = True
    extra = 0

@admin.register(ApplicationWindow)
class ApplicationWindowAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('description', 'open', 'date_created')
    fields = ('description', 'starts', 'ends', 'open')
    inlines = [
        QuestionInline,
        ApplicantsInline
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
    list_filter = [SelectedListFilter]
    fields=('first_name','last_name','email','mobile','gender','university','degree_program','reg_no','year_of_study','application_window','is_selected','is_unselected')
    readonly_fields = ('first_name','last_name','email','mobile','gender','university','degree_program','reg_no','year_of_study','application_window')
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




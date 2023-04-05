from django.contrib import admin
from .models import Questions, Submission


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("problem_id", "problem_title", "problem_description", "sample_input", "sample_output",)


admin.site.register(Questions, QuestionsAdmin)


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('get_question_id', 'code', 'language',)

    def get_question_id(self, obj):
        return obj.question.problem_id

    get_question_id.short_description = 'Problem ID'


admin.site.register(Submission, SolutionAdmin)

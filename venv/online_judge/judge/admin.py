from django.contrib import admin
from .models import Questions


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("problem_id", "problem_title", "problem_description", "sample_input", "sample_output",)


admin.site.register(Questions, QuestionsAdmin)




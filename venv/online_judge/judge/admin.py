from django.contrib import admin
from .models import Questions, CodeSnippet, Testcase


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("problem_id", "problem_title", "problem_description", "sample_input", "sample_output",)


admin.site.register(Questions, QuestionsAdmin)


class CodeSnippetInline(admin.TabularInline):
    model = CodeSnippet

    admin.site.register(CodeSnippet)


class test_casesAdmin(admin.ModelAdmin):
    admin.site.register(Testcase)
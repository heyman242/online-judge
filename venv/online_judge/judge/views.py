from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Questions, CodeSnippet, Testcase
from django.http import JsonResponse
from .forms import CodeSnippetForm
import requests
from django.conf import settings
import subprocess
from django.shortcuts import render
import json
import subprocess


def questions(request):
    myquestions = Questions.objects.all()
    context = {
        'myquestions': myquestions,
    }
    return render(request, 'all_questions.html', context)


def details(request, id, ):
    myquestion = get_object_or_404(Questions, id=id)
    context = {
        'myquestions': myquestion,
    }
    return render(request, 'details.html', context)


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))


# def create_code_snippet(request, id):
#     if request.method == 'POST':
#         question = Questions.objects.get(id=id)
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             # AJAX request
#             code = request.POST.get('code')
#             program_input = request.POST.get('input')
#
#             if code is not None:
#                 result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
#                                         capture_output=True)
#                 if result.returncode == 0:
#                     if program_input is not None:
#                         result = subprocess.run(['./program'], input=program_input.encode('utf-8'), capture_output=True)
#                         output = result.stdout.decode('utf-8')
#                     else:
#                         output = "No input provided"
#                 else:
#                     output = result.stderr.decode('utf-8')
#             else:
#                 output = "No code provided"
#
#             return HttpResponse(output)
#         else:
#             # Regular form submission
#             code = request.POST.get('code')
#             program_input = request.POST.get('input')
#
#             if code is not None:
#                 result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
#                                         capture_output=True)
#                 if result.returncode == 0:
#                     if program_input is not None:
#                         result = subprocess.run(['./program'], input=program_input.encode('utf-8'), capture_output=True)
#                         output = result.stdout.decode('utf-8')
#                     else:
#                         output = "No input provided"
#                 else:
#                     output = result.stderr.decode('utf-8')
#             else:
#                 output = "No code provided"
#
#             return render(request, 'create_code_snippet.html', {'output': output}, {'question': question})
#     else:
#         return render(request, 'create_code_snippet.html', )


def create_code_snippet(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            code = request.POST.get('code')
            program_input = request.POST.get('input')

            if code is not None:
                result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
                                        capture_output=True)
                if result.returncode == 0:
                    if program_input is not None:
                        result = subprocess.run(['./program'], input=program_input.encode('utf-8'), capture_output=True)
                        output = result.stdout.decode('utf-8')
                    else:
                        output = "No input provided"
                else:
                    output = result.stderr.decode('utf-8')
            else:
                output = "No code provided"

            return HttpResponse(output)
        else:
            # Regular form submission
            code = request.POST.get('code')
            results = []

            if code is not None:
                result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
                                        capture_output=True)
                if result.returncode == 0:
                    testcases = TestCases.objects.filter(question=question)
                    for testcase in testcases:
                        input_lines = testcase.input.split("\n")
                        expected_output_lines = testcase.output.split("\n")
                        result = subprocess.run(['./program'], input=testcase.input.encode('utf-8'), capture_output=True)
                        actual_output_lines = result.stdout.decode('utf-8').split("\n")

                        if expected_output_lines == actual_output_lines:
                            results.append({'input': input_lines, 'expected_output': expected_output_lines, 'actual_output': actual_output_lines, 'verdict': 'Accepted'})
                        else:
                            results.append({'input': input_lines, 'expected_output': expected_output_lines, 'actual_output': actual_output_lines, 'verdict': 'Wrong Answer'})
                else:
                    output = result.stderr.decode('utf-8')
                    return render(request, 'create_code_snippet.html', {'output': output, 'question': question})

                return render(request, 'create_code_snippet.html', {'results': results, 'question': question})

            else:
                output = "No code provided"
                return render(request, 'create_code_snippet.html', {'output': output, 'question': question})
    else:
        return render(request, 'create_code_snippet.html')


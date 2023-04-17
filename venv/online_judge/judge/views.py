from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Questions, CodeSnippet, Testcase
from django.http import JsonResponse
from .forms import CodeSnippetForm
from django.conf import settings
import subprocess
import json


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


def execute_code(code: str, program_input: str) -> str:
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

    return output

def create_code_snippet(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            code = request.POST.get('code')
            program_input = request.POST.get('input')

            if code is not None:
                output = execute_code(code, program_input)
            else:
                output = "No code provided"

            return HttpResponse(output)
        
        else:
            output = "No code provided"
            return render(request, 'create_code_snippet.html', {'output': output, 'question': question})

    else:
        question = Questions.objects.get(id=id)
        return render(request, 'create_code_snippet.html', {'question': question, 'id': id})


def result(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        # Regular form submission
        code = request.POST.get('code')
        results = []

        if code is not None:
            result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'), capture_output=True)
            if result.returncode == 0:
                testcases = Testcase.objects.filter(question=question)
                for testcase in testcases:
                    input_lines = testcase.input.split("\n")
                    expected_output_lines = testcase.output.split("\n")
                    actual_output_lines = execute_code(code, testcase.input).split("\n")

                    verdict = 'Accepted'
                    for expected, actual in zip(expected_output_lines, actual_output_lines):
                        if expected.strip() != actual.strip():
                            verdict = 'Wrong Answer'
                            break

                    results.append({'input': input_lines, 'expected_output': expected_output_lines,
                                    'actual_output': actual_output_lines, 'verdict': verdict})

                form_submitted = True
                
                return render(request, 'result.html', {'results': results, 'question': question, 'form_submitted': form_submitted})

    else:
        return render(request, 'create_code_snippet.html', {'question': Questions.objects.get(id=id)})

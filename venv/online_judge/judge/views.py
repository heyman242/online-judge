from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Questions, CodeSnippet
from django.http import JsonResponse
from .forms import CodeSnippetForm
import requests
from django.conf import settings
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
#     question = Questions.objects.get(id=id)
#     if request.method == 'POST':
#         form = CodeSnippetForm(request.POST)
#         source_code = request.POST['code']
#         language = request.POST['language']
#         test_cases = request.POST.getlist('test_cases[]')
#
#         # Make API call to JDoodle
#         url = 'https://api.jdoodle.com/v1/execute'
#         data = {
#             'clientId': settings.JD_API_CLIENT_ID,
#             'clientSecret': settings.JD_API_CLIENT_SECRET,
#             'script': source_code,
#             'language': language,
#             'versionIndex': '0',
#             'stdin': '\n'.join(test_cases)
#         }
#         response = requests.post(url, json=data)
#
#         # Parse the response and render the template
#         result = response.json()
#         output = result.get('output')
#         if output:
#             output = output.strip().split('\n')
#         else:
#             output = []
#
#         return render(request, 'compile_result.html', {
#             'output': output,
#             'statusCode': result.get('statusCode'),
#             'memory': result.get('memory'),
#             'cpuTime': result.get('cpuTime'),
#             'error': result.get('error')
#         })
#
#     return render(request, 'create_code_snippet.html', {'question': question})

def create_code_snippet(request,id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            code = request.POST.get('code')
            program_input = request.POST.get('input')

            if code is not None:
                result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'), capture_output=True)
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
            program_input = request.POST.get('input')

            if code is not None:
                result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'), capture_output=True)
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

            return render(request, 'create_code_snippet.html', {'output': output},{'question': question})
    else:
        return render(request, 'create_code_snippet.html',)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Questions, CodeSnippet, Testcase, NewUser
import subprocess
from typing import List
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login


def questions(request):
    myquestions = Questions.objects.all()
    context = {
        'myquestions': myquestions,
    }
    return render(request, 'all_questions.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'newuser'):
            login(request, user)
            return redirect('judge:questions')  # Redirect to the questions view
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email_id = request.POST.get('email_id')
        name = request.POST.get('name')

        # Check if passwords match
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        # Create user instance
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Create newuser instance
        newuser = NewUser(user=user, id=username[:5], email_id=email_id, name=name)
        newuser.save()

        return redirect('judge:login')
    else:
        return render(request, 'signup.html')


def details(request, id):
    question_detail = get_object_or_404(Questions, id=id)
    context = {
        'question_detail': question_detail,
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


def execute_code1(code: str, program_input: List[str]) -> List[str]:
    result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
                            capture_output=True)

    if result.returncode == 0:
        outputs = []
        for input_str in program_input:
            result = subprocess.run(['./program'], input=input_str.encode('utf-8'), capture_output=True)
            output = result.stdout.decode('utf-8').strip()
            outputs.append(output)

        return outputs

    else:
        return []


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


@login_required
def result(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        # Regular form submission
        code = request.POST.get('code')
        results = []

        if code is not None:
            result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
                                    capture_output=True)
            if result.returncode == 0:
                testcases = Testcase.objects.filter(question=question)
                inputs_outputs = []
                for testcase in testcases:
                    inputs_outputs.append({
                        'input': [str(x) for x in testcase.input['input']],
                        'output': [str(x) for x in testcase.output['output']]
                    })

                for i, io in enumerate(inputs_outputs):
                    input_lines = io['input']
                    expected_output_lines = io['output']
                    actual_output_lines = execute_code1(code, input_lines)

                    verdict = 'Accepted'
                    for expected, actual in zip(expected_output_lines, actual_output_lines):
                        if expected.strip() != actual.strip():
                            verdict = 'Wrong Answer'
                            break

                    results.append({
                        'id': i + 1,
                        'input': input_lines,
                        'expected_output': expected_output_lines,
                        'actual_output': actual_output_lines,
                        'verdict': verdict
                    })

                form_submitted = True
                return render(request, 'result.html',
                              {'results': results, 'question': question, 'form_submitted': form_submitted})
            else:
                # Compilation error occurred
                results.append({'verdict': 'Compilation Error'})
                return render(request, 'result.html', {'results': results, 'question': question})
        else:
            # No code submitted
            results.append({'verdict': 'No Code Submitted'})
            return render(request, 'result.html', {'results': results, 'question': question})

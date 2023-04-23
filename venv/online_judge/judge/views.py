import subprocess

from django.shortcuts import render, get_object_or_404
from django.template import loader
import docker
from django.http import HttpResponse
from .models import Questions, Testcase
# from .apps import execute_code
from .docker_init import execute_code_in_docker_container 


def questions(request):
    # Method to fetch all the questions from the DB.
    myquestions = Questions.objects.all()
    context = {
        'myquestions': myquestions,
    }
    return render(request, 'all_questions.html', context)


def details(request, id, ):
    # Method to fetch the details of the question.
    question_detail = get_object_or_404(Questions, id=id)
    context = {
        'question_detail': question_detail,
    }
    return render(request, 'details.html', context)


def main(request):
    #Method to render the main project.
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))



def create_code_snippet(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            code = request.POST.get('code')
            program_input = request.POST.get('input')

            # print(code)
            # print(program_input)

            if code is not None:
                image = 'second'
                print(image)
                output = execute_code_in_docker_container(image, code, program_input)
                print(output)

            else:
                output = "Please provide a valid code."

            return HttpResponse(output)

        else:
            output = "No code provided"
            return render(request, 'create_code_snippet.html', {'output': output, 'question': question})

    else:
        question = Questions.objects.get(id=id)
        return render(request, 'create_code_snippet.html', {'question': question, 'id': id})





def execute_code1(code, input_lines):
    # create a Docker client
    client = docker.from_env()

    # build the Docker image for the compiler
    image, _ = client.images.build(path='/path/to/dockerfile', tag='cpp_compiler')

    # mount the code directory as a volume
    code_dir = '/path/to/code'
    volumes = {code_dir: {'bind': '/code', 'mode': 'rw'}}

    # compile the code using Docker
    cmd = f"g++ -o /code/program -"
    container = client.containers.run(image, command=cmd, volumes=volumes, stdin_open=True, tty=True, detach=True)

    # write the input to stdin of the container
    container.exec_run('echo "{}" | ./program'.format('\\n'.join(input_lines)), stdin=True)

    # get the output of the execution
    output = container.logs().decode('utf-8')

    # stop and remove the container
    container.stop()
    container.remove()

    # return the output as a list of lines
    return output.strip().split('\n')


def result(request, id):
    if request.method == 'POST':
        question = Questions.objects.get(id=id)
        # Regular form submission
        code = request.POST.get('code')
        results = []

        if code is not None:
            # create a Docker client
            client = docker.from_env()

            # build the Docker image for the compiler
            image, _ = client.images.build(path='/path/to/dockerfile', tag='cpp_compiler')

            # mount the code directory as a volume
            code_dir = '/path/to/code'
            volumes = {code_dir: {'bind': '/code', 'mode': 'rw'}}

            # compile the code using Docker
            cmd = f"g++ -o /code/program -"
            container = client.containers.run(image, command=cmd, volumes=volumes, stdin_open=True, tty=True, detach=True)

            # write the input to stdin of the container
            testcases = Testcase.objects.filter(question=question)
            inputs_outputs = []
            for testcase in testcases:
                inputs_outputs.append({
                    'input': [str(x) for x in testcase.input['input']],
                    'output': [str(x) for x in testcase.output['output']]
                })
            for io in inputs_outputs:
                input_lines = io['input']
                container.exec_run('echo "{}" | ./program'.format('\\n'.join(input_lines)), stdin=True)

                # get the output of the execution
                output = container.logs().decode('utf-8')

                expected_output_lines = io['output']
                actual_output_lines = output.strip().split('\n')

                verdict = 'Accepted'
                for expected, actual in zip(expected_output_lines, actual_output_lines):
                    if expected.strip() != actual.strip():
                        verdict = 'Wrong Answer'
                        break

                results.append({
                    'input': input_lines,
                    'expected_output': expected_output_lines,
                    'actual_output': actual_output_lines,
                    'verdict': verdict
                })

            # stop and remove the container
            container.stop()
            container.remove()

            form_submitted = True
            return render(request, 'result.html', {'results': results, 'question': question, 'form_submitted': form_submitted})
        else:
            # No code submitted
            results.append({'verdict': 'No Code Submitted'})
        return render(request, 'result.html', {'results': results, 'question': question})
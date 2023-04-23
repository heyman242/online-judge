import subprocess
from typing import List

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Questions, Testcase
import os


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


# def execute_code1(code: str, program_input: List[str]) -> List[str]:
#     result = subprocess.run(['g++', '-x', 'c++', '-o', 'program', '-'], input=code.encode('utf-8'),
#                             capture_output=True)
#
#     if result.returncode == 0:
#         outputs = []
#         for input_str in program_input:
#             result = subprocess.run(['./program'], input=input_str.encode('utf-8'), capture_output=True)
#             output = result.stdout.decode('utf-8').strip()
#             outputs.append(output)
#
#         return outputs
#
#     else:
#         return []


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


import os
import docker

# def result(request, id):
#     if request.method == 'POST':
#         question = Questions.objects.get(id=id)
#         # Regular form submission
#         code = request.POST.get('code')
#         results = []

#         if code is not None:
#             # Create a Docker client and connect to the Docker daemon
#             client = docker.from_env()
#             # Set up the container
#             volumes = {os.getcwd(): {'bind': '/app', 'mode': 'rw'}}
#             environment = {'CODE': code}
#             container = client.containers.run('gcc',
#                                               command='bash -c "echo \"$CODE\" > program.cpp && g++ -o program program.cpp && ./program"',
#                                               environment=environment,
#                                               volumes=volumes,
#                                               detach=True)
#             # Get the container output
#             output = container.logs().decode('utf-8')
#             # Stop and remove the container
#             container.stop()
#             container.remove()

#             if "error" in output.lower():
#                 # Compilation error occurred
#                 results.append({'verdict': 'Compilation Error'})
#                 print(output)
#                 return render(request, 'result.html', {'results': results, 'question': question})
#             else:
#                 # Compilation successful, run the tests
#                 testcases = Testcase.objects.filter(question=question)
#                 inputs_outputs = []
#                 for testcase in testcases:
#                     inputs_outputs.append({
#                         'input': [str(x) for x in testcase.input['input']],
#                         'output': [str(x) for x in testcase.output['output']]
#                     })

#                 for i, io in enumerate(inputs_outputs):
#                     input_lines = io['input']
#                     expected_output_lines = io['output']
#                     # Execute the compiled program with the test case input
#                     container = client.containers.run('gcc',
#                                                       command='bash -c "echo \'{}\' | ./program"'.format('\n'.join(input_lines)),
#                                                       volumes=volumes,
#                                                       detach=True)
#                     # Get the container output
#                     output = container.logs().decode('utf-8')
#                     # Stop and remove the container
#                     container.stop()
#                     container.remove()

#                     if "error" in output.lower():
#                         # Runtime error occurred
#                         results.append({
#                             'id': i+1,
#                             'input': input_lines,
#                             'expected_output': expected_output_lines,
#                             'actual_output': [],
#                             'verdict': 'Runtime Error'
#                         })
#                     else:
#                         actual_output_lines = output.strip().split('\n')
#                         # Check if the actual output matches the expected output
#                         verdict = 'Accepted'
#                         for expected, actual in zip(expected_output_lines, actual_output_lines):
#                             if expected.strip() != actual.strip():
#                                 verdict = 'Wrong Answer'
#                                 break

#                         results.append({
#                             'id': i+1,
#                             'input': input_lines,
#                             'expected_output': expected_output_lines,
#                             'actual_output': actual_output_lines,
#                             'verdict': verdict
#                         })

#                 form_submitted = True
#                 print(results)
#                 return render(request, 'result.html', {'results': results, 'question': question, 'form_submitted': form_submitted})
#         else:
#             # No code submitted
#             results.append({'verdict': 'No Code Submitted'})
#             return render(request, 'result.html', {'results': results, 'question': question})


# import docker
# import tempfile
# from typing import List

# # def execute_code1(code: str, program_input: List[str]) -> List[str]:
# #     client = docker.from_env()
# #     image = 'gcc:latest'
# #     with tempfile.TemporaryDirectory() as tempdir:
# #         # Create a temporary directory to store the program files
# #         program_path = f"{tempdir}/program.cpp"
# #         input_path = f"{tempdir}/input.txt"
# #
# #         # Write the program code and input to files
# #         with open(program_path, 'w') as f:
# #             f.write(code)
# #         with open(input_path, 'w') as f:
# #             f.write("\n".join(program_input))
# #
# #         # Compile the code inside a Docker container
# #         volumes = {tempdir: {'bind': '/mnt', 'mode': 'rw'}}
# #         cmd = f"g++ /mnt/program.cpp -o /mnt/program && cd /mnt && ./program < /mnt/input.txt"
# #         container = client.containers.run(image, command=cmd, volumes=volumes, remove=True)
# #
# #         # Get the container output and return the result
# #         output = container.decode('utf-8').strip()
# #         return output.split("\n")


# import docker


import docker
from django.http import HttpResponse

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
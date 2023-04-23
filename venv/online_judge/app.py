import subprocess

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


def execute_code_in_container(code: str, program_input: str) -> str:
    # Define the Docker image and container name
    image_name = "my-docker-image"
    container_name = "my-container"
    print('0')
    # Create the Docker container
    subprocess.run(["docker", "create", "--name", container_name, image_name])
    print('1')

    # Start the Docker container and execute the code
    command = f"docker start -a {container_name} /bin/bash -c 'python app.py'"
    print(command)
    if program_input is not None:
        command += f" '{program_input}'"
        print(command)
    result = subprocess.run(command, input=code.encode("utf-8"), capture_output=True, shell=True)
    print(result)

    # Remove the Docker container
    subprocess.run(["docker", "rm", container_name])

    # Return the output
    return result.stdout.decode("utf-8")

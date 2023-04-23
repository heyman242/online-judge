import docker
import subprocess

def execute_code_in_docker_container(image_name, code, program_input):
    client = docker.from_env()
    # print(client) 

    # Build the Docker container
    client.images.build(path='.', tag=image_name)

    # Run the execute_code function in the Docker container
    docker_command = ['docker', 'run', '-i', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr', image_name]
    # print(docker_command)
    execute_code_command = ['python3', 'app.py', code, program_input]
    command = docker_command + execute_code_command
    result = subprocess.run(command, capture_output=True)
    print(result)
    print('---------------------------')
    print(result.stdout)
    print(result.returncode)

    output = result.stdout.decode('utf-8')
    print('---------------------------')
    print('done', output)


    return "done" + output
import subprocess

def main(code: str, program_input: str) -> str:
    print("code", code)
    print("input", input)

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



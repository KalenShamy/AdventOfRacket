import random
import os
import subprocess, tempfile
from pathlib import Path
import platform

# Construct the absolute path to the racket executable
BASE_DIR = Path(__file__).resolve().parent.parent
RACKET_ROOT = BASE_DIR / "RacketInstalls" / "racket"

def add_sandbox(code):
    safe_code = code.replace("\\", "\\\\").replace('"', '\\"')
    return f"""
    #lang racket
        (require racket/sandbox)

        (define run (make-evaluator 'racket "{safe_code}"))
    """

def add_tests(code, tests, delimiter):
    public_tests = tests["public"]
    hidden_tests = tests["hidden"]
    func_name = tests.get("function_name")

    for test in public_tests + hidden_tests:
        code += f'\n(print "{delimiter}") (run "({func_name} {test[0]})")'

    return code

def get_results(code, delimiter):
    with tempfile.NamedTemporaryFile(suffix=".rkt", mode="w+", delete=True) as temp_file:
        temp_file.write(code)
        temp_file.flush()

        try:
            run_env = os.environ.copy()
            run_env["PLTCOLLECTS"] = str(RACKET_ROOT / "collects")

            result = subprocess.run(
                [str(RACKET_ROOT / "bin" / "racket"), temp_file.name],
                capture_output=True,
                text=True,
                timeout=15,
                env=run_env
            )
        except subprocess.TimeoutExpired:
            return False, "Code execution timed out."

    output = result.stdout.split(f'"{delimiter}"')[1:]
    output = [out.strip() for out in output]

    if result.stderr == "":
        return True, output
    else:
        return False, "Your code crashed during execution\n" + result.stderr.encode("utf-8").splitlines()[0].decode("utf-8")

def verify_tests(tests, output):
    results = []
    passed_public = 0
    passed_hidden = 0
    public_total = len(tests["public"])
    hidden_total = len(tests["hidden"])

    if len(output) < public_total + hidden_total:
        print(output)
        return False, {"message": "Your code crashed during execution\nUnknown Error"}

    for i, test in enumerate(tests["public"]):
        expected = test[1]
        actual = output[i]
        if expected == actual:
            passed_public += 1
        results.append(output[i].strip() if i < len(output) else "No output")

    for i, test in enumerate(tests["hidden"]):
        expected = test[1]
        actual = output[public_total + i]
        if expected == actual:
            passed_hidden += 1
    
    if passed_public == public_total and passed_hidden == hidden_total:
        return True, {"message": "All tests passed!", "results": results}
    
    if passed_public != public_total:
        return False, {"message": f"{passed_public}/{public_total} passed", "results": results}
    
    return False, {"message": f"All public tests pass\n{passed_hidden}/{hidden_total} hidden tests passed", "results": results}

def validate_code(code, tests):
    delimiter = f"*{random.random()}*"

    code = add_sandbox(code)
    code = add_tests(code, tests, delimiter)

    success, output = get_results(code, delimiter)
    if not success:
        return False, {"message": output, "results": []}
    
    return verify_tests(tests, output)
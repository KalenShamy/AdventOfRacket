import random
import subprocess, tempfile

def add_sandbox(code):
    return f"""
    #lang racket
        (require racket/sandbox)

        (define run (make-evaluator 'racket "{code}"))
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
            result = subprocess.run(
                ["racket", temp_file.name],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            return False, "Code execution timed out."

    output = result.stdout.split(delimiter)[1:]
    output = [out[1:-1].strip() for out in output]

    return True, output

def verify_tests(tests, output):
    results = []
    passed_public = 0
    passed_hidden = 0
    public_total = len(tests["public"])
    hidden_total = len(tests["hidden"])

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
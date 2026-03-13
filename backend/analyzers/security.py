import ast
import re

DANGEROUS_CALLS = {"eval", "exec", "compile", "os.system", "pickle.loads",
                   "subprocess.call", "subprocess.Popen"}

def analyze(code: str) -> list:
    findings = []
    lines = code.splitlines()

    sql_pattern = re.compile(
        r'(execute|cursor\.execute|db\.execute)\s*\(\s*["\'].*["\'].*\+',
        re.IGNORECASE
    )
    for i, line in enumerate(lines, 1):
        if sql_pattern.search(line):
            findings.append({
                "line": i,
                "type": "SQL injection",
                "severity": "critical",
                "description": "String concatenation inside a SQL execute() is vulnerable to injection.",
                "fix": 'cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))'
            })

    secret_pattern = re.compile(
        r'(password|api_key|secret|token|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']',
        re.IGNORECASE
    )
    for i, line in enumerate(lines, 1):
        if secret_pattern.search(line) and "os.environ" not in line:
            findings.append({
                "line": i,
                "type": "Hardcoded secret",
                "severity": "critical",
                "description": "A credential appears to be hardcoded in the source code.",
                "fix": "import os\nvalue = os.environ.get('MY_SECRET')"
            })

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = f"{getattr(node.func.value, 'id', '')}.{node.func.attr}"
                if name in DANGEROUS_CALLS:
                    findings.append({
                        "line": node.lineno,
                        "type": f"Dangerous call: {name}()",
                        "severity": "critical",
                        "description": f"'{name}' is a security risk — can execute arbitrary code.",
                        "fix": "Use a safer alternative or validate/sanitize all inputs first."
                    })
    except SyntaxError:
        pass

    user_input_pattern = re.compile(r'\b(request|user_input|raw_input|input\()\b')
    validation_pattern = re.compile(r'\b(if|validate|sanitize|escape|strip|isinstance)\b')
    for i, line in enumerate(lines, 1):
        if user_input_pattern.search(line):
            window = "\n".join(lines[max(0, i-3):i+3])
            if not validation_pattern.search(window):
                findings.append({
                    "line": i,
                    "type": "Unvalidated user input",
                    "severity": "warning",
                    "description": "User input is used without nearby validation or sanitization.",
                    "fix": "value = request.get('field', '').strip()\nif not value: raise ValueError('Required')"
                })

    return findings
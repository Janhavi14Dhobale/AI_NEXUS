import ast

def analyze(code: str) -> list:
    findings = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "line": e.lineno or 1,
            "type": "Syntax error",
            "severity": "critical",
            "description": str(e),
            "fix": "Fix the syntax error before analysis."
        }]

    assigned_vars = set()
    used_vars = set()

    for node in ast.walk(tree):

        # Track variables
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                assigned_vars.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)

        # Self assignment
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if isinstance(node.value, ast.Name) and node.value.id == target.id:
                        findings.append({
                            "line": node.lineno,
                            "type": "Self-assignment",
                            "severity": "warning",
                            "description": f"Variable '{target.id}' assigned to itself.",
                            "fix": "Check assignment logic."
                        })

        # Hardcoded password
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if "password" in target.id.lower():
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            findings.append({
                                "line": node.lineno,
                                "type": "Hardcoded password",
                                "severity": "critical",
                                "description": "Hardcoded passwords are a security risk.",
                                "fix": "Store secrets in environment variables or secure vaults."
                            })

        # Mutable default argument
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    findings.append({
                        "line": node.lineno,
                        "type": "Mutable default argument",
                        "severity": "warning",
                        "description": f"Function '{node.name}' uses mutable default argument.",
                        "fix": f"def {node.name}(arg=None):\n    if arg is None: arg = []"
                    })

        # Bare except
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append({
                "line": node.lineno,
                "type": "Bare except",
                "severity": "warning",
                "description": "Catching all exceptions hides real errors.",
                "fix": "except Exception as e:"
            })

        # Nested loops detection
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if child is not node and isinstance(child, ast.For):
                    findings.append({
                        "line": node.lineno,
                        "type": "Nested loop",
                        "severity": "warning",
                        "description": "Nested loops may lead to O(n²) complexity.",
                        "fix": "Consider using set or dictionary lookups."
                    })
                    break

        # Division by zero
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                findings.append({
                    "line": node.lineno,
                    "type": "Division by zero",
                    "severity": "critical",
                    "description": "Division by zero will crash program.",
                    "fix": "Check denominator before dividing."
                })

        # Infinite loop detection
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value == True:
                findings.append({
                    "line": node.lineno,
                    "type": "Infinite loop risk",
                    "severity": "critical",
                    "description": "while True loop may run forever.",
                    "fix": "Ensure break condition exists."
                })

        # Dangerous eval()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({
                    "line": node.lineno,
                    "type": "Dangerous eval()",
                    "severity": "critical",
                    "description": "Using eval() can execute arbitrary code.",
                    "fix": "Avoid eval(); use safer parsing methods."
                })

    # Unused variables
    unused = assigned_vars - used_vars
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in unused:
                    findings.append({
                        "line": node.lineno,
                        "type": "Unused variable",
                        "severity": "info",
                        "description": f"Variable '{target.id}' is assigned but never used.",
                        "fix": "Remove the variable or use it."
                    })

    return findings
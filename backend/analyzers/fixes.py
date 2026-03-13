FIX_TEMPLATES = {
    "SQL injection": {
        "explanation": "Use parameterised queries. Never build SQL strings by concatenation.",
        "before": "cursor.execute('SELECT * FROM users WHERE name=' + name)",
        "after":  "cursor.execute('SELECT * FROM users WHERE name=%s', (name,))"
    },
    "Hardcoded secret": {
        "explanation": "Store secrets in environment variables, not source code.",
        "before": "API_KEY = 'abc123secret'",
        "after":  "import os\nAPI_KEY = os.environ.get('API_KEY')"
    },
    "Mutable default argument": {
        "explanation": "Default values are created once at function definition time.",
        "before": "def add_item(item, lst=[]):\n    lst.append(item)\n    return lst",
        "after":  "def add_item(item, lst=None):\n    if lst is None: lst = []\n    lst.append(item)\n    return lst"
    },
    "Nested loop": {
        "explanation": "Two nested loops over the same collection = quadratic time.",
        "before": "for i in items:\n    for j in items:\n        if i == j: ...",
        "after":  "seen = set()\nfor i in items:\n    if i in seen: ...\n    seen.add(i)"
    },
    "Bare except": {
        "explanation": "Bare except catches everything including system signals.",
        "before": "try:\n    ...\nexcept:\n    pass",
        "after":  "try:\n    ...\nexcept Exception as e:\n    logger.error(e)"
    },
}

def get_fix(issue_type: str) -> dict:
    for key, template in FIX_TEMPLATES.items():
        if key.lower() in issue_type.lower():
            return template
    return {}
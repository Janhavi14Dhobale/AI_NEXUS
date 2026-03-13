# AI_NEXUS

- ---

## What it detects

### Bugs
- Mutable default arguments in functions
- Bare except clauses
- Self-assignments
- Nested loops (O(n²) complexity smell)
- Syntax errors

### Security
- SQL injection via string concatenation
- Hardcoded secrets (passwords, API keys, tokens)
- Dangerous function calls (eval, exec, pickle.loads, os.system)
- Unvalidated user input

### Complexity
- Cyclomatic complexity per function (flagged at >10 and >15)
- Halstead volume, difficulty, and effort metrics

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend setup
```bash

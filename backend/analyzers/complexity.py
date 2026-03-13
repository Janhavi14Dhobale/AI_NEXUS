import radon.complexity as rc
import radon.metrics as rm

def analyze(code: str) -> dict:
    functions = []
    try:
        results = rc.cc_visit(code)
        for r in results:
            severity = "info"
            if r.complexity > 15:
                severity = "critical"
            elif r.complexity > 10:
                severity = "warning"
            functions.append({
                "name": r.name,
                "line": r.lineno,
                "complexity": r.complexity,
                "severity": severity,
                "description": (
                    "Very hard to test — refactor urgently." if r.complexity > 15
                    else "Consider simplifying." if r.complexity > 10
                    else "Acceptable complexity."
                ),
            })
    except Exception:
        pass

    halstead = {}
    try:
        h = rm.h_visit(code)
        if h:
            halstead = {
                "volume": round(h[0].volume, 1),
                "difficulty": round(h[0].difficulty, 1),
                "effort": round(h[0].effort, 1),
            }
    except Exception:
        pass

    return {"functions": functions, "halstead": halstead}
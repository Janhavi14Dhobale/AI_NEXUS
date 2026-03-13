from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzers import ast_parser, security, complexity, fixes

app = FastAPI(title="Code Reviewer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@app.get("/health")
def health():
    return {"status": "ok", "engine": "self-contained"}

@app.post("/analyze")
def analyze(req: CodeRequest):
    if req.language == "python":
        bugs            = ast_parser.analyze(req.code)
        security_issues = security.analyze(req.code)
        cx              = complexity.analyze(req.code)
    else:
        bugs            = []
        security_issues = security.analyze(req.code)
        cx              = {"functions": [], "halstead": {}}

    for issue in bugs + security_issues:
        fix_detail = fixes.get_fix(issue["type"])
        if fix_detail:
            issue["fix_detail"] = fix_detail

    critical = sum(1 for i in bugs + security_issues if i.get("severity") == "critical")
    warnings = sum(1 for i in bugs + security_issues if i.get("severity") == "warning")
    total    = len(bugs) + len(security_issues)

    return {
        "bugs":        bugs,
        "security":    security_issues,
        "performance": [],
        "complexity":  cx,
        "summary":     f"{total} issue(s) found — {critical} critical, {warnings} warnings.",
        "engine":      "self-contained"
    }
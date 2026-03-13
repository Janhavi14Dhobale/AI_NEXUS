import { useState } from "react"
import axios from "axios"
import "./App.css"

const DEMOS = [
  {
    label: "SQL injection",
    code: `import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name=" + username)
    return cursor.fetchone()

result = get_user("admin' OR '1'='1")
print(result)`
  },

  {
    label: "Mutable default + bare except",
    code: `def add_item(item, lst=[]):
    lst.append(item)
    return lst

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        pass

print(add_item(1))
print(add_item(2))`
  },

  {
    label: "O(n²) nested loop",
    code: `def find_duplicates(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j and i not in duplicates:
                duplicates.append(i)
    return duplicates

data = list(range(1000))
print(find_duplicates(data))`
  },

  {
    label: "Division by zero",
    code: `def divide(a,b):
    return a/b

print(divide(10,0))`
  },

  {
    label: "Hardcoded password",
    code: `password = "admin123"

def login(user_input):
    if user_input == password:
        print("Access granted")
    else:
        print("Access denied")

login("admin123")`
  },

  {
    label: "Infinite loop risk",
    code: `i = 0

while i >= 0:
    print(i)
    i += 1`
  },

  {
    label: "Unused variable",
    code: `def calculate():
    x = 10
    y = 20
    z = x + y
    unused = 100
    return z

print(calculate())`
  },

  {
    label: "File not closed",
    code: `def read_data():
    f = open("data.txt","r")
    data = f.read()
    return data

print(read_data())`
  },

  {
    label: "Inefficient list search",
    code: `def search(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return True
    return False

nums = list(range(100000))
print(search(nums,99999))`
  },

  {
    label: "Recursive stack overflow",
    code: `def recurse():
    return recurse()

recurse()`
  }
]

const SEVERITY_COLOR = {
  critical: "badge-critical",
  warning: "badge-warning",
  info: "badge-info"
}

function Badge({ severity }) {
  return <span className={`badge ${SEVERITY_COLOR[severity] || "badge-info"}`}>{severity}</span>
}

function IssueCard({ issue }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="issue-card">
      <div className="issue-header" onClick={() => setOpen(!open)}>
        <span className="issue-line">Line {issue.line}</span>
        <Badge severity={issue.severity} />
        <span className="issue-type">{issue.type}</span>
        <span className="chevron">{open ? "▲" : "▼"}</span>
      </div>

      {open && (
        <div className="issue-body">
          <p className="issue-desc">{issue.description}</p>

          {issue.fix_detail ? (
            <div className="fix-block">
              <p className="fix-label">Why: {issue.fix_detail.explanation}</p>

              <div className="code-diff">
                <div className="diff-before">
                  <span className="diff-tag">Before</span>
                  <pre>{issue.fix_detail.before}</pre>
                </div>

                <div className="diff-after">
                  <span className="diff-tag">After</span>
                  <pre>{issue.fix_detail.after}</pre>
                </div>
              </div>
            </div>
          ) : (
            <pre className="fix-simple">{issue.fix}</pre>
          )}
        </div>
      )}
    </div>
  )
}

export default function App() {

  const [code, setCode] = useState(DEMOS[0].code)
  const [language, setLang] = useState("python")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function analyze() {

    setLoading(true)
    setError("")
    setResult(null)

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/analyze",
        { code, language }
      )

      setResult(res.data)

    } catch (e) {

      setError("Could not reach backend. Is uvicorn running?")

    }

    setLoading(false)

  }

  const allIssues = result
    ? [...(result.bugs || []), ...(result.security || [])]
    : []

  const critical = allIssues.filter(i => i.severity === "critical").length
  const warnings = allIssues.filter(i => i.severity === "warning").length

  return (

    <div className="app">

      <header className="header">
        <h1>ErrorVision</h1>
        <p className="subtitle">
          AI-powered static analysis for detecting bugs, security risks and performance issues
        </p>
      </header>

      <div className="toolbar">

        <select
          value={language}
          onChange={e => setLang(e.target.value)}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
        </select>

        <span className="demo-label">Load demo:</span>

        {DEMOS.map(d => (
          <button
            key={d.label}
            className="btn-demo"
            onClick={() => setCode(d.code)}
          >
            {d.label}
          </button>
        ))}

      </div>

      <div className="editor-row">

        <textarea
          className="editor"
          value={code}
          onChange={e => setCode(e.target.value)}
          spellCheck={false}
          placeholder="Paste your code here..."
        />

      </div>

      <button
        className="btn-analyze"
        onClick={analyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>

      {error && <div className="error">{error}</div>}

      {loading && (
        <div className="spinner-wrap">
          <div className="spinner" />
        </div>
      )}

      {result && (

        <div className="results">

          <div className="summary-bar">
            <span className="summary-text">{result.summary}</span>

            <span className="badge badge-critical">
              {critical} critical
            </span>

            <span className="badge badge-warning">
              {warnings} warnings
            </span>
          </div>

          {result.security?.length > 0 && (
            <section>

              <h2>Security issues</h2>

              {result.security.map((i, idx) => (
                <IssueCard key={idx} issue={i} />
              ))}

            </section>
          )}

          {result.bugs?.length > 0 && (
            <section>

              <h2>Bugs</h2>

              {result.bugs.map((i, idx) => (
                <IssueCard key={idx} issue={i} />
              ))}

            </section>
          )}

          {result.complexity?.functions?.length > 0 && (

            <section>

              <h2>Complexity</h2>

              <div className="complexity-grid">

                {result.complexity.functions.map((f, idx) => (

                  <div key={idx} className="complexity-card">

                    <span className="fn-name">{f.name}</span>

                    <span className="fn-line">
                      line {f.line}
                    </span>

                    <span className={`complexity-score score-${f.severity}`}>
                      {f.complexity}
                    </span>

                    <span className="fn-desc">
                      {f.description}
                    </span>

                  </div>

                ))}

              </div>

              {result.complexity.halstead?.volume && (

                <div className="halstead">

                  <span>
                    Volume: {result.complexity.halstead.volume}
                  </span>

                  <span>
                    Difficulty: {result.complexity.halstead.difficulty}
                  </span>

                  <span>
                    Effort: {result.complexity.halstead.effort}
                  </span>

                </div>

              )}

            </section>

          )}

        </div>

      )}

    </div>
  )
}
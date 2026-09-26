from app.models import Evidence

def scan_evidence(paths: list[str]) -> list[Evidence]:
    normalized = [p.lower() for p in paths]
    evidence: list[Evidence] = []

    tests = [p for p in normalized if any(m in p for m in ("tests/", "test/", "__tests__/"))]
    if tests:
        evidence.append(Evidence(source="repository", details={"type": "tests_found", "examples": tests[:5]}))

    ci = [p for p in normalized if ".github/workflows/" in p]
    if ci:
        evidence.append(Evidence(source="repository", details={"type": "ci_found", "examples": ci[:5]}))

    benchmarks = [p for p in normalized if any(m in p for m in ("benchmark", "metrics.json", "results.json"))]
    if benchmarks:
        evidence.append(Evidence(source="repository", details={"type": "benchmark_candidate", "examples": benchmarks[:5]}))

    return evidence

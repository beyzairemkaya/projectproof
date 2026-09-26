def run_test_presence_probe(paths: list[str]) -> dict:
    normalized = [p.lower() for p in paths]
    test_files = [
        p for p in normalized
        if "/tests/" in f"/{p}" or "/test/" in f"/{p}" or "__tests__/" in p
        or p.startswith("tests/") or p.startswith("test/")
    ]
    return {
        "method": "ProjectProof repository test-presence probe",
        "tests_found": bool(test_files),
        "examples": test_files[:5],
        "note": "MVP detects test artifacts; it does not execute untrusted repository code.",
    }

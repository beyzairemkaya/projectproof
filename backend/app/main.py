from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import AnalyzeRequest, ClaimResult, Evidence, EvidenceStatus
from app.probes.latency_probe import run_latency_probe
from app.probes.test_presence_probe import run_test_presence_probe
from app.services.claim_extractor import extract_claims
from app.services.evidence_scanner import scan_evidence
from app.services.github_service import fetch_readme, fetch_repo_tree

app = FastAPI(
    title="ProjectProof",
    description="Evidence layer for early-stage web projects.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health() -> dict:
    return {"service": "ProjectProof", "status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest) -> dict:
    try:
        readme = await fetch_readme(str(request.repo_url))
        repo_paths = await fetch_repo_tree(str(request.repo_url))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not inspect repository: {exc}") from exc

    claims = extract_claims(readme)
    repository_evidence = scan_evidence(repo_paths)
    test_probe = run_test_presence_probe(repo_paths)

    latency_result = None
    if request.deployed_url:
        try:
            latency_result = await run_latency_probe(str(request.deployed_url))
        except Exception as exc:
            latency_result = {"error": str(exc)}

    results: list[ClaimResult] = []

    for claim in claims:
        if claim.claim_type == "LATENCY":
            if not request.deployed_url:
                status = EvidenceStatus.NOT_TESTED
                evidence = repository_evidence
            elif latency_result and "error" not in latency_result:
                status = (
                    EvidenceStatus.SUPPORTED
                    if claim.target is not None and latency_result["p95_ms"] <= claim.target
                    else EvidenceStatus.UNSUPPORTED
                )
                evidence = [
                    *repository_evidence,
                    Evidence(source="projectproof_probe", details=latency_result),
                ]
            else:
                status = EvidenceStatus.NOT_TESTED
                evidence = [
                    *repository_evidence,
                    Evidence(source="projectproof_probe", details=latency_result or {}),
                ]
        elif claim.claim_type == "TEST_PRESENCE":
            status = EvidenceStatus.SUPPORTED if test_probe["tests_found"] else EvidenceStatus.NO_EVIDENCE
            evidence = [
                *repository_evidence,
                Evidence(source="projectproof_probe", details=test_probe),
            ]
        else:
            status = EvidenceStatus.NO_EVIDENCE
            evidence = repository_evidence

        results.append(ClaimResult(claim=claim, status=status, evidence=evidence))

    return {
        "repository": str(request.repo_url),
        "claims_found": len(claims),
        "results": results,
        "methodology": {
            "claim_extraction": "deterministic MVP patterns",
            "evidence_scan": "repository artifact scan",
            "probe_logic": "deterministic and auditable",
            "untrusted_code_execution": False,
        },
    }

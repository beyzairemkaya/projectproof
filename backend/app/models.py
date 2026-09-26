from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import Any


class EvidenceStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    NO_EVIDENCE = "NO_EVIDENCE"
    NOT_TESTED = "NOT_TESTED"


class AnalyzeRequest(BaseModel):
    repo_url: HttpUrl
    deployed_url: HttpUrl | None = None


class Claim(BaseModel):
    text: str
    claim_type: str
    target: float | None = None
    unit: str | None = None


class Evidence(BaseModel):
    source: str
    details: dict[str, Any] = {}


class ClaimResult(BaseModel):
    claim: Claim
    status: EvidenceStatus
    evidence: list[Evidence] = []

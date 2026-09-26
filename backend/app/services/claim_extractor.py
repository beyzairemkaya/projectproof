import re
from app.models import Claim

LATENCY_PATTERN = re.compile(
    r"(?P<full>[^\n.!?]{0,100}?(?:latency|response time|responds?|response)[^\n.!?]{0,80}?"
    r"(?:under|below|less than|<)\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>ms|milliseconds?|s|seconds?))",
    re.IGNORECASE,
)

def extract_claims(readme: str) -> list[Claim]:
    claims: list[Claim] = []
    for match in LATENCY_PATTERN.finditer(readme):
        value = float(match.group("value"))
        unit = match.group("unit").lower()
        if unit in {"s", "second", "seconds"}:
            value *= 1000
        claims.append(Claim(text=match.group("full").strip(), claim_type="LATENCY", target=value, unit="ms"))

    lowered = readme.lower()
    if any(p in lowered for p in ("fully tested", "well tested", "comprehensive tests")):
        claims.append(Claim(text="README claims the project is tested.", claim_type="TEST_PRESENCE"))
    return claims[:5]

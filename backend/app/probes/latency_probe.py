import statistics
import time
import httpx

async def run_latency_probe(url: str, requests: int = 10) -> dict:
    samples_ms: list[float] = []
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        for _ in range(requests):
            started = time.perf_counter()
            response = await client.get(url)
            elapsed_ms = (time.perf_counter() - started) * 1000
            response.raise_for_status()
            samples_ms.append(elapsed_ms)

    ordered = sorted(samples_ms)
    p95_index = max(0, min(len(ordered) - 1, round(0.95 * (len(ordered) - 1))))
    return {
        "method": "ProjectProof HTTP latency probe",
        "requests": requests,
        "p50_ms": round(statistics.median(samples_ms), 2),
        "p95_ms": round(ordered[p95_index], 2),
        "max_ms": round(max(samples_ms), 2),
    }

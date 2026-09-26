# ProjectProof

**Build. Prove. Ship.**

ProjectProof is an evidence layer for early-stage web projects. It checks whether technical claims are backed by inspectable engineering evidence.

## MVP scope

The first version focuses on public web/API repositories and a deliberately small set of claims:

- latency / response-time claims
- test-presence claims
- obvious evidence artifacts such as test folders, benchmark files, metrics outputs, and CI workflows

ProjectProof does **not** decide whether a project is "good" or "bad". It shows which claims are supported, unsupported, untested, or missing evidence.

## Core flow

```
GitHub URL
   ↓
README claim extraction
   ↓
Repository evidence scan
   ↓
Standard probes
   ↓
Evidence report
```

## Run locally

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Example request

```json
{
  "repo_url": "https://github.com/owner/repo",
  "deployed_url": "https://example.com"
}
```

The `deployed_url` field is optional. If supplied, the MVP runs a deterministic HTTP latency probe.

## Evidence statuses

- `SUPPORTED`
- `UNSUPPORTED`
- `NO_EVIDENCE`
- `NOT_TESTED`

## Product principle

> We do not ask you to trust the verdict. We show where the evidence came from.

AI may assist with claim classification later, but probe logic should remain deterministic and auditable.

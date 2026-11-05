from fastapi import FastAPI

app = FastAPI(
    title="SENTINEL-X",
    version="0.1.0",
    description="Defensive network threat detection API scaffold.",
)


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz", tags=["health"])
def readyz() -> dict[str, str]:
    # Replace with model and dependency readiness checks when serving is implemented.
    return {"status": "ready"}

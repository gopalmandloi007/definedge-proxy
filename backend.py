from fastapi import FastAPI, Request
import httpx
from fastapi.responses import Response

app = FastAPI()

# Base URL of Definedge Zone
BASE_URL = "https://zone.definedgesecurities.com"

@app.get("/")
def home():
    return {"message": "Definedge Proxy Running. Visit /zone for access."}

@app.api_route("/zone/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    url = f"{BASE_URL}/{path}"
    method = request.method

    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.request(method, url, headers=headers, content=body)

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.headers.get("content-type")
    )

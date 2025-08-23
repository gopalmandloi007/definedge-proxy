from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Replace with Definedge broker base URL
TARGET_URL = "https://integrate.definedgesecurities.com"

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    url = f"{TARGET_URL}/{path}"
    headers = {key: value for key, value in request.headers if key.lower() != "host"}

    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

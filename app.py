import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Apne broker ka base URL
TARGET_URL = "https://integrate.definedgesecurities.com"

@app.route("/ping")
def ping():
    return {"status": "ok", "message": "Proxy is working!"}

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    # Final URL jahan forward karna hai
    url = f"{TARGET_URL}/{path}"

    # Incoming headers copy karna (host change na kare)
    headers = {k: v for k, v in request.headers if k.lower() != "host"}

    # Forward request
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    # Response back client ko dena
    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    response_headers = [(name, value) for name, value in resp.headers.items() if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, response_headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os
import subprocess

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

# FIX: secret comes from the environment, never from source code.
# Without SECRET_KEY set, a random one is generated at startup.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32).hex()

# FIX: command injection. Only fixed, pre-approved commands can run,
# and no shell is involved.
ALLOWED_COMMANDS = {
    "ls": ["ls", "-l"],
    "date": ["date"],
    "whoami": ["whoami"],
}


@app.route("/")
def index():
    return """
    <h1>Welcome to our (now fixed) Flask App!</h1>
    <p>Explore the different pages:</p>
    <ul>
        <li><a href="/hello?name=World">Hello Page</a></li>
        <li><a href="/execute?cmd=ls">Execute Command Page (allow-listed commands only)</a></li>
        <li><a href="/admin">Admin Area</a></li>
    </ul>
    """


@app.route("/hello")
def hello():
    # FIX: reflected XSS. User input is HTML-escaped before rendering.
    name = escape(request.args.get("name", "Guest"))
    return f"""
    <h1>Hello Page</h1>
    <p>Hello, {name}!</p>
    <p><a href="/">Back to Homepage</a></p>
    """


@app.route("/execute")
def execute():
    key = request.args.get("cmd", "ls")
    command = ALLOWED_COMMANDS.get(key)
    if command is None:
        allowed = ", ".join(sorted(ALLOWED_COMMANDS))
        return f"<h1>Command not allowed</h1><p>Allowed: {escape(allowed)}</p>", 400
    result = subprocess.run(command, capture_output=True, text=True, timeout=5)
    return f"""
    <h1>Execute Command Page</h1>
    <p>Executing command: <code>{escape(key)}</code></p>
    <pre>{escape(result.stdout)}</pre>
    <pre style="color: red;">{escape(result.stderr)}</pre>
    <p><a href="/">Back to Homepage</a></p>
    """


@app.route("/admin")
def admin():
    # FIX: the secret is no longer displayed. (A real app would also
    # require authentication here.)
    return """
    <h1>Admin Area</h1>
    <p>Access restricted. Authentication is required.</p>
    <p><a href="/">Back to Homepage</a></p>
    """, 403


@app.after_request
def add_security_headers(response):
    # FIX: common DAST findings (missing security headers).
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    # FIX: debug mode off. Bind to 0.0.0.0 only because it runs in a container.
    app.run(debug=False, host="0.0.0.0")  # NOSONAR

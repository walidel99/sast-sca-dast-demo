from flask import Flask, request
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecretkey123" # Hardcoded secret!

@app.route('/')
def index():
    return """
    <h1>Welcome to our vulnerable Flask App! 😎</h1>
    <p>Explore the different pages:</p>
    <ul>
        <li><a href="/hello?name=World">Hello Page (try changing the name in the URL!)</a></li>
        <li><a href="/execute?cmd=ls -la">Execute Command Page (try changing the command in the URL!)</a></li>
        <li><a href="/admin">Admin Area (contains a secret!)</a></li>
    </ul>
    
    <a href="https://github.com/pandelig/sast-sca-dast-demo" target="_blank">GitHub Repo↗</a></li>
    """

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"""
    <h1>Hello Page</h1>
    <p>Hello, {name}!</p>
    <p><a href="/">Back to Homepage</a></p>
    """

@app.route('/execute')
def execute():
    command = request.args.get('cmd', 'ls -l')
    # Insecure command execution!
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return f"""
    <h1>Execute Command Page</h1>
    <p>Executing command: <code>{command}</code></p>
    <pre>{result.stdout}</pre>
    <pre style="color: red;">{result.stderr}</pre>
    <p><a href="/">Back to Homepage</a></p>
    """

@app.route('/admin')
def admin():
    return f"""
    <h1>Admin Area</h1>
    <p>Admin area - Secret Key: {app.config['SECRET_KEY']}</p>
    <p><a href="/">Back to Homepage</a></p>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
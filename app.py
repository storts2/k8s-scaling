from flask import Flask, jsonify
import os
import socket
import time
app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()
    return f"""
    <html>
        <head>
            <title>Kubernetes Scaling Lab</title>
        </head>
        <body>
            <h1>Online Shopping Website</h1>
            
            <h2>Kubernetes Scaling Demonstration</h2>
            
            <p>Application: Online Shopping Website</p>
            <p>Container Hostname: {hostname}</p>
            
            <p>Environment: {os.getenv("APP_ENV", "development")}</p>
            
            <hr>

            <p>This application is running on Kubernetes.</p>

            <p>Try the following endpoints:</p>

            <ul>
                <li>/health</li>
                <li>/info</li>
                <li>/work</li>
            </ul>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/info")
def info():
    return jsonify({
        "application": "Online Shopping Website",
        "hostname": socket.gethostname(),
        "environment": os.getenv("APP_ENV", "development")
    })

@app.route("/work")
def work():
    # Simulate CPU-intensive application processing
    result = 0

    for i in range(2000000):
        result += i * i

    return jsonify({
        "message": "Work completed",
        "hostname": socket.gethostname(),
        "result": result
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
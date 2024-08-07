import subprocess
import os
import sys


def run_backend():
    backend_path = os.path.join(os.getcwd(), "backend", "app.py")
    # Set the PYTHONPATH environment variable to the project root
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    return subprocess.Popen(
        ["python", backend_path], cwd=os.path.join(os.getcwd(), "backend"), env=env
    )


def run_frontend():
    frontend_path = os.path.join(os.getcwd(), "frontend", "front.py")
    return subprocess.Popen(
        ["python", frontend_path], cwd=os.path.join(os.getcwd(), "frontend")
    )


def run_db():
    frontend_path = os.path.join(os.getcwd(), "database", "docker-compose.yaml")
    return subprocess.Popen(
        ["docker", "compose", "up"], cwd=os.path.join(os.getcwd(), "database")
    )


if __name__ == "__main__":
    database_process = run_db()
    backend_process = run_backend()
    frontend_process = run_frontend()

    try:
        database_process.wait()
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()

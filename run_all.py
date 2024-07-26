import subprocess
import os

def run_backend():
    backend_path = os.path.join(os.getcwd(), 'backend', 'back.py')
    return subprocess.Popen(['python', backend_path], cwd=os.path.join(os.getcwd(), 'backend'))

def run_frontend():
    frontend_path = os.path.join(os.getcwd(), 'frontend', 'front.py')
    return subprocess.Popen(['python', frontend_path], cwd=os.path.join(os.getcwd(), 'frontend'))

if __name__ == "__main__":
    backend_process = run_backend()
    frontend_process = run_frontend()

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()

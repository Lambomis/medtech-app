import threading
import http.server
import socketserver
import os
import uvicorn
import webbrowser
import importlib.util
import time
import sys
import signal
import json

MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")
BACKEND_DIR = os.path.join(MODULES_DIR, "backend")
FRONTEND_DIR = os.path.join(MODULES_DIR, "frontend")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

default_config = {
    "backend_host": "127.0.0.1",
    "backend_port": 8000,
    "frontend_host": "127.0.0.1",
    "frontend_port": 8001
}

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump(default_config, f, indent=4)
    config = default_config
else:
    with open(CONFIG_PATH) as f:
        config = json.load(f)

BACKEND_HOST = config["backend_host"]
BACKEND_PORT = config["backend_port"]
FRONTEND_HOST = config["frontend_host"]
FRONTEND_PORT = config["frontend_port"]

app_path = os.path.join(BACKEND_DIR, "app.py")
spec = importlib.util.spec_from_file_location("app", app_path)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
stop_flag = threading.Event()

def signal_handler(sig, frame):
    print("\nCTRL+C premuto. Chiusura dei server...")
    stop_flag.set()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

CONFIG_JS_PATH = os.path.join(FRONTEND_DIR, "config.js")
with open(CONFIG_JS_PATH, "w", encoding="utf-8") as f:
    backend_url = f"http://{BACKEND_HOST}:{BACKEND_PORT}/process"
    f.write(f'const API_URL = "{backend_url}";\n')


def run_frontend():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    with socketserver.TCPServer((FRONTEND_HOST, FRONTEND_PORT), Handler) as httpd:
        url = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"
        print(f"Frontend server running at {url}")
        webbrowser.open(url)
        while not stop_flag.is_set():
            httpd.handle_request()

def run_backend():
    print(f"Backend FastAPI running at http://{BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run(app_module.app, host=BACKEND_HOST, port=BACKEND_PORT, reload=False)


if __name__ == "__main__":
    t_backend = threading.Thread(target=run_backend, daemon=True)
    t_frontend = threading.Thread(target=run_frontend, daemon=True)

    t_backend.start()
    t_frontend.start()

    try:
        while not stop_flag.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        signal_handler(None, None)


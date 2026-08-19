
import threading
import time
import requests
from app import app

def run_server():
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

time.sleep(2)

print("Testing request to /")
try:
    response = requests.get('http://127.0.0.1:5001/')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("Press Ctrl+C to exit")
server_thread.join()

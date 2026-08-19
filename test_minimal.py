
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask!"

if __name__ == '__main__':
    print("Starting minimal server...")
    app.run(host='127.0.0.1', port=5002, debug=False, use_reloader=False)

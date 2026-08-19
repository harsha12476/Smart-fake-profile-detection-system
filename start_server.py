
import sys
from app import app
print('Server running at http://127.0.0.1:5001')
print('Press Ctrl+C to stop')
try:
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False, threaded=True)
except KeyboardInterrupt:
    print('Server stopped.')

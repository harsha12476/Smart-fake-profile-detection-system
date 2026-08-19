
import traceback

print("Importing app...")
try:
    from app import app
    print("App imported successfully!")
    
    print("Starting server...")
    app.run(host='127.0.0.1', port=5003, debug=False, use_reloader=False)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

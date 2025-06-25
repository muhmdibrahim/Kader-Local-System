import webview
import threading
from app import app  # Import your Flask app

def run_flask():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    window = webview.create_window(
        'Kader Academy System',
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
        text_select=True
    )
    webview.start()
import webbrowser
from utils import log_error

def open_web_browser(url):
    try:
        webbrowser.open(url)
        print(f"Opening web browser with URL: {url}")
    except Exception as e:
        print(f"Error opening web browser: {e}")
        log_error(e)
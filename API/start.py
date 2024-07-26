import subprocess
import time

def start_fastapi():
    subprocess.Popen(["uvicorn", "api_main:app", "--reload"])

def start_streamlit():
    subprocess.Popen(["streamlit", "run", "home_page.py"])

if __name__ == "__main__":
    start_fastapi()
    time.sleep(4)  # Attendre un peu pour s'assurer que le serveur FastAPI démarre avant Streamlit
    start_streamlit()

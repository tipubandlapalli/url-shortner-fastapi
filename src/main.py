from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
def home():
    return "home page"

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return "ok"
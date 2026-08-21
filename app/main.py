from fastapi import FastAPI

app = FastAPI(title="E-Commerce")

@app.get("/")
def root():
    return {"message": "E-commerce is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

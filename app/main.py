from fastapi import FastAPI
from app.user.router import router as user_router

app = FastAPI(title="Ecommerce API", version="1.0.0")

# Mount your User module router with a shared api prefix
app.include_router(user_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
from fastapi import FastAPI
from app.user.router import router as user_router
from app.auth.router import router as auth_router


app = FastAPI(title="Ecommerce API", version="1.0.0")

# Mount your User module router with a shared api prefix
app.include_router(user_router, prefix="/api/v1")
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
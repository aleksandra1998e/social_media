from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.db.session import get_db
from app.api import router as api_router

app = FastAPI()

app.openapi = get_openapi(
    title="Social Networking API",
    version="1.0.0",
    description="API for a social networking application",
    routes=app.routes,
)

# Add API router
app.include_router(api_router, prefix="/api")


@app.middleware("http")
async def add_db(request, call_next):
    request.state.db = get_db()
    response = await call_next(request)
    request.state.db.close()
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

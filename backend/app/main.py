from fastapi import FastAPI
from app.routes import router as data_router
import uvicorn

app = FastAPI()

# Register API routes
app.include_router(data_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import router as data_router
import uvicorn


# to start app use following command from project directory (challenger_stats dir): uvicorn backend.app.main:app --reload

app = FastAPI()


# Enable CORS for your frontend application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(data_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Player Stats API!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
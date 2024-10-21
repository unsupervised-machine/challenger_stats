from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import router
import uvicorn
from dotenv import load_dotenv
import os

# run backend with: uvicorn backend.app.main:app --port 8000
# exit with control+c to gracefully exit
# if above doesn't work try: uvicorn backend.app.main:app --port 8001

# Load environment variables
load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Create FastAPI app
app = FastAPI()


# Allow CORS for specified origins
origins = [
    "http://localhost:3000",  # Your frontend URL
    "http://localhost:8001",  # Add this if you need to access from another localhost server
    # Add other origins if needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins (for example, ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
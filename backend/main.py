import logging
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import StatusResponse, Feedback
from metro_service import metro_manager
from security import RateLimitMiddleware, SecurityHeaderMiddleware, validate_input_sanitization

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("HydroFlow.API")

app = FastAPI(title="HydroFlow: Metro Crowd Predictor API", version="2.0.0")
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(SecurityHeaderMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

@app.get("/status", response_model=StatusResponse)
async def get_network_status(request: Request):
        try:
                    return metro_manager.get_network_status()
except Exception as e:
        raise HTTPException(status_code=500, detail="Service currently unavailable")

@app.post("/feedback")
async def post_feedback(feedback: Feedback, background_tasks: BackgroundTasks):
        sanitized_desc = validate_input_sanitization(feedback.description)
        background_tasks.add_task(logger.info, "Feedback processed.")
        return {"status": "accepted"}

dist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend/dist")
if os.path.exists(dist_path):
        app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
        @app.exception_handler(404)
        async def not_found_handler(request: Request, exc: HTTPException):
                    return FileResponse(os.path.join(dist_path, "index.html"))

    if __name__ == "__main__":
            import uvicorn
            port = int(os.environ.get("PORT", 8000))
            uvicorn.run(app, host="0.0.0.0", port=port)
        

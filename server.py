# server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
import uvicorn
from main import run_master_pipeline  # Import your Master Glue

app = FastAPI(title="Adobe AI Toolkit Server")

# Create a folder for files coming from your laptop
UPLOAD_DIR = "incoming_jobs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "Online", "message": "Gamer PC is ready to process video audio."}

@app.post("/process-from-adobe")
async def handle_adobe_request(file: UploadFile = File(...)):
    """
    This endpoint receives the audio from Adobe Premiere.
    """
    try:
        # 1. Save the incoming audio file
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📥 Received Job: {file.filename}")

        # 2. Trigger the Master Glue Pipeline
        # We pass the path of the saved audio to your main.py logic
        result_json = run_master_pipeline(file_location)

        # 3. Return the Instructions back to the Laptop
        if os.path.exists(result_json):
            with open(result_json, "r") as f:
                import json
                recipe_data = json.load(f)
            
            return {
                "status": "success",
                "message": "Processing complete",
                "data": recipe_data
            }
        else:
            raise HTTPException(status_code=500, detail="Pipeline failed to generate screenplay.")

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the server on Port 8000
    # host='0.0.0.0' allows your laptop to find the Gamer PC on the network
    uvicorn.run(app, host="0.0.0.0", port=8000)
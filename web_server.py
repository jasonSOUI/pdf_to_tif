
import os
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from core.converter import convert_pdf_to_tif

# --- Initial Setup ---
app = FastAPI()

# Create directories for temporary file storage
UPLOAD_DIR = "uploads"
DOWNLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Mount static files directory to serve downloaded files
app.mount("/downloads", StaticFiles(directory=DOWNLOAD_DIR), name="downloads")

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serves the main HTML page."""
    try:
        with open("web/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found.")

@app.post("/api/convert")
async def api_convert_pdf(
    file: UploadFile = File(...),
    compression: str = Form("LZW")
):
    """Handles PDF file upload, conversion, and returns a download link."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # Generate a unique filename to avoid conflicts
    unique_id = uuid.uuid4().hex
    original_filename = os.path.splitext(file.filename)[0]
    pdf_filename = f"{original_filename}_{unique_id}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    # Save the uploaded PDF temporarily
    try:
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    # Perform the conversion
    success, result = convert_pdf_to_tif(
        pdf_path=pdf_path,
        output_dir=DOWNLOAD_DIR,
        compression=compression
    )

    # Clean up the uploaded PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    if not success:
        # If conversion fails, return an error message
        raise HTTPException(status_code=500, detail=result)

    # If conversion succeeds, return a download link to the TIF file
    tif_filename = os.path.basename(result)
    download_url = f"downloads/{tif_filename}"
    
    return JSONResponse(content={
        "success": True,
        "message": "File converted successfully!",
        "download_url": download_url
    })

# --- Main execution for development ---
if __name__ == "__main__":
    import uvicorn
    print("Starting web server...")
    print("Access the application at http://127.0.0.1:28888")
    uvicorn.run(app, host="127.0.0.1", port=28888)

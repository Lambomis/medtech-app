from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import io
import base64
from pathlib import Path


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = FRONTEND_DIR / "index.html"
    html_content = html_path.read_text(encoding="utf-8")
    html_content = html_content.replace('href="style.css"', 'href="/static/style.css"')
    html_content = html_content.replace('src="scripts.js"', 'src="/static/scripts.js"')
    return html_content

@app.post('/process')
async def process_image(file: UploadFile = File(...), phase: str = Form(...)):
    contents = await file.read()

    try:
        img = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception as e:
        return JSONResponse({'error': 'Impossibile leggere immagine: ' + str(e)}, status_code=400)


    if phase == 'arterial':
        enhancer = ImageEnhance.Contrast(img)
        processed = enhancer.enhance(1.8)


    elif phase == 'venous':
        arr = np.array(img)
        blurred = cv2.GaussianBlur(arr, (7, 7), 0)
        processed = Image.fromarray(blurred)

    else:
        return JSONResponse({'error': 'Fase non valida'}, status_code=400)


    buf = io.BytesIO()
    processed.save(buf, format='PNG')
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {'processed_image': encoded}
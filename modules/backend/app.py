from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import io
import base64
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

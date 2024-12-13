from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import onnxruntime as ort
import numpy as np
from PIL import Image
from io import BytesIO
from storage import load_model
import os 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/c/credential/worknonetwork-project-f46884310b6c.json"

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bucket_name = "wnn-bucket"
blob_name = "model-in-prod/WNN_Model.onnx"

try:
    session = load_model(bucket_name, blob_name)
except Exception as e: 
    raise RuntimeError(f"Failed to load model: {e}")

def preprocess_image(image):
    image = image.resize((224, 224)) 
    image = np.array(image).astype(np.float32) / 255.0 
    
    image = np.expand_dims(image, axis=0)  
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    print(f"Received file content type: {file.content_type}")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        input_data = preprocess_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    inputs = {session.get_inputs()[0].name: input_data}
    prediction = session.run(None, inputs)

    return JSONResponse(content={"prediction": prediction[0].tolist()})

import onnx
import onnxruntime as ort
from google.cloud import storage
from io import BytesIO

def download_model(bucket_name, blob_name):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        model_data = blob.download_as_bytes()
        return model_data
    except Exception as e: 
        raise RuntimeError("Failed to download model from GCS: {e}")

def load_model(bucket_name, blob_name):
    try: 
        model_data = download_model(bucket_name, blob_name)
        model = onnx.load(BytesIO(model_data))
        session = ort.InferenceSession(model.SerializeToString())
        return session
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

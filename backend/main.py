from fastapi import FastAPI, UploadFile, File
import pandas as pd
import os
import shutil

app = FastAPI(
    title="AI All-in-One Data Tool",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI All-in-One Tool API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        return {"error": "Unsupported file format"}

    # JSON-safe response
    return {
        "filename": file.filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": [str(col) for col in df.columns],
        "dtypes": {
            str(col): str(dtype)
            for col, dtype in df.dtypes.items()
             },
        "preview": df.head(5).fillna("").to_dict(orient="records")
    }
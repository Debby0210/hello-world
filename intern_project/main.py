from fastapi import FastAPI, Response, HTTPException,UploadFile, Form
import os
from pydantic import BaseModel
import uvicorn
import logging

app = FastAPI()



#設置原本圖像與名稱
IMAGE_DIRECTORY = "."
ORIGINAL_IMAGE_NAME = "image.jpg"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/debby/debby00")
async def cc():
    return {"message": "Hello!!!"}

@app.get("/image")
async def get_image():
    image_path = os.path.join(IMAGE_DIRECTORY, ORIGINAL_IMAGE_NAME)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return Response(content=image_data, media_type="image/jpeg")

@app.post("/uploadfile")
async def create_upload_file(file:UploadFile):
     return {"filename": file.filename}



@app.put("/update-image-name")
async def update_image_name(new_name: str = Form(...)):
    original_image_path = os.path.join(IMAGE_DIRECTORY, ORIGINAL_IMAGE_NAME)
    new_image_path = os.path.join(IMAGE_DIRECTORY, new_name)

    if not os.path.exists(original_image_path):
        raise HTTPException(status_code=404, detail="Original image not found")

    if os.path.exists(new_image_path):
        raise HTTPException(status_code=400, detail="New image name already exists")

    try:
        os.rename(original_image_path, new_image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming image file: {e}")

    return {"message": "Image renamed successfully", "new_name": new_name}

@app.delete("/delete-image")
async def delete_image():
   return {"message": "Image removed successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




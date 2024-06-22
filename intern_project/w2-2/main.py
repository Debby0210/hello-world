from fastapi import FastAPI, Response, HTTPException,UploadFile, Form
import os
from pydantic import BaseModel
from typing import List
import uvicorn
import logging

app = FastAPI()


#設置原本圖像路徑
IMAGE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'original_image')  # 將 'original_image' 替換成你的資料夾名稱
print(IMAGE_DIRECTORY)
TARGET_DIRECTORY= os.path.join(os.path.dirname(__file__), 'target_image')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/debby/debby00")
async def cc():
    return {"message": "Hello!!!"}

@app.get("/images", response_model=List[str])
async def list_images():
    try:
        print(f"Image directory: {IMAGE_DIRECTORY}")  # 調試信息
        # 列出資料夾中的所有圖片文件
        files = os.listdir(IMAGE_DIRECTORY)
        images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        return images
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image directory not found")

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(IMAGE_DIRECTORY, image_name)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    return Response(content=image_data, media_type="image/jpeg")


@app.post("/upload-image/")
async def upload_image(file: UploadFile):
    try:
        file_location = os.path.join(TARGET_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving image file: {e}")

    return {"message": "Image uploaded successfully", "file_name": file.filename}


@app.put("/update-image-name")
async def update_image_name(image_name: str = Form(...), new_name: str = Form(...)):
    original_image_path = os.path.join(IMAGE_DIRECTORY, image_name)
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
async def delete_image(image_name: str = Form(...)):
    original_image_path = os.path.join(IMAGE_DIRECTORY, image_name)

    if not os.path.exists(original_image_path):
       
        raise HTTPException(status_code=404, detail="Original image not found")
    return {"message": "Image removed successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




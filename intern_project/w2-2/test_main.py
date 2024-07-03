from fastapi import FastAPI, Response, HTTPException,UploadFile, Form
import os
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.testclient import TestClient
from main import app


client=TestClient(app)

#定義測試的資料夾以及目標資料夾
IMAGE_DIRECTORY = "test_original_image" 
TARGET_DIRECTORY = "test_target_image" 


# @app.get("/")
# def root():
#     return{"Hello":"World"}



# def test_root ():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json()== {"Hello":"World"}

def setup_directories():
    # 清理测试目录
    if os.path.exists(IMAGE_DIRECTORY):
        for file in os.listdir(IMAGE_DIRECTORY):
            os.remove(os.path.join(IMAGE_DIRECTORY, file))
    if os.path.exists(TARGET_DIRECTORY):
        for file in os.listdir(TARGET_DIRECTORY):
            os.remove(os.path.join(TARGET_DIRECTORY, file))

    # 创建测试目录和文件
    os.makedirs(IMAGE_DIRECTORY, exist_ok=True)
    os.makedirs(TARGET_DIRECTORY, exist_ok=True)
    
    # 创建多个测试文件
    with open(os.path.join(IMAGE_DIRECTORY, "test1.jpg"), 'wb') as f:
        f.write(b"test image content 1")
    with open(os.path.join(IMAGE_DIRECTORY, "test2.jpg"), 'wb') as f:
        f.write(b"test image content 2")
    with open(os.path.join(IMAGE_DIRECTORY, "bicycle.jpg"), 'wb') as f:
        f.write(b"test image content 3")
    with open(os.path.join(IMAGE_DIRECTORY, "airplane.jpg"), 'wb') as f:
        f.write(b"test image content 4")
    
    # 调试信息
    print(f"Created directory: {IMAGE_DIRECTORY}")
    print(f"Created directory: {TARGET_DIRECTORY}")
    print(f"Files in {IMAGE_DIRECTORY}: {os.listdir(IMAGE_DIRECTORY)}")
    print(f"Files in {TARGET_DIRECTORY}: {os.listdir(TARGET_DIRECTORY)}")

    assert os.path.exists(IMAGE_DIRECTORY), "test_original_image directory was not created"
    assert os.path.exists(TARGET_DIRECTORY), "test_target_image directory was not created"
    assert os.path.exists(os.path.join(IMAGE_DIRECTORY, "test1.jpg")), "test1.jpg was not created"


def teardown_directories():
    for file in os.listdir(IMAGE_DIRECTORY):
        os.remove(os.path.join(IMAGE_DIRECTORY, file))
    os.rmdir(IMAGE_DIRECTORY)
    for file in os.listdir(TARGET_DIRECTORY):
        os.remove(os.path.join(TARGET_DIRECTORY, file))
    os.rmdir(TARGET_DIRECTORY)


def test_list_images():
    setup_directories()
    try:
        assert os.path.exists("test_original_image"), "test_original_image directory was not created"
        assert os.path.exists("test_target_image"), "test_target_image directory was not created"
        assert os.path.exists(os.path.join("test_original_image", "test1.jpg")), "test1.jpg was not created"

        response = client.get("/images")
        assert response.status_code == 200
        # 期望的文件列表
        expected_files = ["test1.jpg", "test2.jpg","bicycle.jpg","airplane.jpg"]
        assert sorted(response.json()) == sorted(expected_files), f"Expected {expected_files} but got {response.json()}"
        
    finally:
        teardown_directories()



def test_get_image():
    setup_directories()
    try:
        response = client.get("/image/test2.jpg")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
    finally:
        teardown_directories()


def test_get_image_not_found():
    response = client.get("/image/nonexistent.jpg")
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}


def test_upload_image():
    setup_directories()
    try:
        file_data = {"file": ("test_upload.jpg", b"test image content", "image/jpeg")}
        response = client.post("/upload-image/", files=file_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Image uploaded successfully", "file_name": "test_upload.jpg"}

        print(f"Files in {TARGET_DIRECTORY}: {os.listdir(TARGET_DIRECTORY)}")
        assert os.path.exists(os.path.join(TARGET_DIRECTORY, "test_upload.jpg"))
    finally:
        teardown_directories()



def test_update_image_name():
    setup_directories()
    try:
        data = {"image_name": "test1.jpg", "new_name": "test_renamed.jpg"}
        response = client.put("/update-image-name", data=data)
        assert response.status_code == 200
        assert response.json() == {"message": "Image renamed successfully", "new_name": "test_renamed.jpg"}
        assert os.path.exists(os.path.join(IMAGE_DIRECTORY, "test_renamed.jpg"))
    finally:
        teardown_directories()

def test_update_image_name_not_found():
    data = {"image_name": "nonexistent.jpg", "new_name": "test_renamed.jpg"}
    response = client.put("/update-image-name", data=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Original image not found"}


def test_delete_image():
    setup_directories()
    try:
        data = {"image_name": "test2.jpg"}
        response = client.delete("/delete-image", data=data)
        assert response.status_code == 200
        assert response.json() == {"message": "Image removed successfully"}
        assert not os.path.exists(os.path.join(IMAGE_DIRECTORY, "test2.jpg"))
    finally:
        teardown_directories()


from fastapi import FastAPI
from fastapi.testclient import TestClient
app = FastAPI()

@app.get("/")
def root():
    return{"Hello":"World"}

client=TestClient(app)

def test_root ():
    response=client.get("/")
    assert response.status_code == 200
    assert response.json()== {"Hello":"World"}
from fastapi.testclient import TestClient
from main import app

# This creates a fake browser to test your app without starting a real server
client = TestClient(app)

def test_read_root():
    # 1. Ask the fake browser to visit the home page "/"
    response = client.get("/")
    
    # 2. Check if the server responded with a 200 OK status code
    assert response.status_code == 200
    
    # 3. Check if the message matches exactly what we expect
    assert response.json() == {"message": "Welcome to MyFASTAPI"}

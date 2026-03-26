from fastapi.testclient import TestClient
from app.main import app
from app.data import names

client = TestClient(app)

def test_health_check():
    """Test the root endpoint to ensure the server is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "server is running"}

def test_generate_name_no_params():
    """Test the /generate_name endpoint without any query parameters."""
    response = client.get("/generate_name")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    # Verify the generated name is actually from our data list
    assert data["name"] in names

def test_generate_name_starts_with_lowercase():
    """Test the starts_with query parameter with a lowercase letter."""
    prefix = "a"
    response = client.get(f"/generate_name?starts_with={prefix}")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    assert data["name"].startswith(prefix)
    assert data["name"] in names

def test_generate_name_starts_with_uppercase():
    """Test the starts_with query parameter to ensure it is case-insensitive."""
    prefix = "A" # Uppercase 'A'
    response = client.get(f"/generate_name?starts_with={prefix}")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    # The generated name should start with 'a' or 'A'
    assert data["name"].lower().startswith(prefix.lower())

def test_generate_name_full_prefix():
    """Test the starts_with query parameter with a full name prefix."""
    prefix = "osa"
    response = client.get(f"/generate_name?starts_with={prefix}")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    assert data["name"] == "osama" # "osama" is the only name starting with "osa"
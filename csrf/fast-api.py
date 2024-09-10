from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# CSRF configuration model
class CsrfSettings(BaseModel):
    secret_key: str = "mysecretkey"

# Initialize CSRF protection with settings
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# Route to get the CSRF token
@app.get("/get-csrf-token")
def get_csrf(csrf_protect: CsrfProtect = Depends()):
    token = csrf_protect.create_csrf_token()
    return {"csrf_token": token}

# Sample data model
class Item(BaseModel):
    name: str
    description: str

# POST route with CSRF protection
@app.post("/submit-item")
def submit_item(item: Item, csrf_protect: CsrfProtect = Depends()):
    return {"message": f"Item {item.name} submitted successfully!"}

# CSRF-protected route
@app.post("/protected")
def protected_route(item: Item, csrf_protect: CsrfProtect = Depends(), request: Request = None):
    # Protect against CSRF by verifying the token
    csrf_protect.validate_csrf(request)
    return {"message": "CSRF token is valid, request processed."}

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

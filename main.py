from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_TOKEN = "supersecrettoken123"

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niepoprawny token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/secure-data")
def secure_data(token: str = Depends(verify_token)):
    return {"message": "sukces"}

from fastapi import FastAPI
from port import ser

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Server is running"}


@app.post("/angles")
def set_angles(angles: str):
    if ser:
        ser.write((angles + "\n").encode())
        return {"sent": angles}
    else:
        print("No serial port found, running without hardware")
        return {"sent": None, "note": "no serial port found"}
    

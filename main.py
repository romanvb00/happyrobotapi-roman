from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import pandas as pd
import os
import json


load_dotenv()

API_KEY = os.getenv("ROMANHAPPYROBOT_2025")
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

try:
    df = pd.read_csv("loads_sample.csv", sep=";", dtype={"load_id": str})
    df.replace([float("inf"), float("-inf")], 0, inplace=True)
    df.fillna(0, inplace=True)
except Exception as e:
    print("Failed to load CSV:", str(e))
    df = pd.DataFrame()


app = FastAPI()

@app.get("/loads/{load_id}", dependencies=[Depends(get_api_key)])
def get_load(load_id: str):
    try:
        print(f"🔍 Buscando load_id: {load_id}")
        result = df[df["load_id"] == load_id]
        print(f"🔎 Resultados encontrados: {len(result)}")
        if result.empty:
            raise HTTPException(status_code=404, detail="Load not found")
        return result.iloc[0].to_dict()
    except Exception as e:
        print("Internal error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

import os
from fastapi import Request

@app.post("/calls", dependencies=[Depends(get_api_key)])
async def add_call(request: Request):
    try:
        call = await request.json()
        print("📥 Received call:", call)

        required_keys = {"mc_number", "load_id", "initial_rate", "final_rate", "outcome", "sentiment"}
        if not required_keys.issubset(call.keys()):
            print("Missing keys in call:", call.keys())
            raise HTTPException(status_code=400, detail="Invalid call format")

        try:
            call["initial_rate"] = float(call["initial_rate"])
            call["final_rate"] = float(call["final_rate"])
        except ValueError as ve:
            print("Rate parsing failed:", ve)
            raise HTTPException(status_code=400, detail="Rates must be numeric")

        if os.path.exists("calls_log.json"):
            with open("calls_log.json", "r") as f:
                calls = json.load(f)
        else:
            calls = []

        calls.append(call)

        with open("calls_log.json", "w") as f:
            json.dump(calls, f, indent=2)

        print("✅ call saved. Total calls:", len(calls))
        return {"status": "success", "call_count": len(calls)}

    except Exception as e:
        print("Internal error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
from fastapi.staticfiles import StaticFiles
@app.get("/calls", dependencies=[Depends(get_api_key)])
def get_all_calls():
    try:
        if os.path.exists("calls_log.json"):
            with open("calls_log.json", "r") as f:
                calls = json.load(f)
            return calls
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading call log: {str(e)}")


app.mount("/dashboard", StaticFiles(directory="static", html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)


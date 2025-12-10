from fastapi import FastAPI,UploadFile,Form,File,HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from dotenv import load_dotenv
load_dotenv()

class AIResponse(BaseModel):
    answer:str
    sources: List[str]



app = FastAPI()

@app.get("/")
def start():
    return({"status":"AI running"})

@app.post("/process")
async def process_request(
    files: List[UploadFile] = File(...), 
    userprompt: str = Form(...),
    searchenabled: str = Form(...) 
):# --- CHECK DATA IMPORT ---
    print("\n--- NEW REQUEST RECEIVED ---")
    
    # 1. Check Prompt
    print(f"User Prompt: {userprompt}")
    
    # 2. Check Web Search
    # Convert string "true" to Boolean True
    is_web_search_enabled = searchenabled.lower() == 'true'
    print(f"Web Search Enabled: {is_web_search_enabled}")

    # 3. Check Files
    if not files:
        print("Error: No files received.")
        raise HTTPException(status_code=400, detail="No files provided")
    
    print(f"Number of Files: {len(files)}")
    for file in files:
        print(f" - Filename: {file.filename}")
        print(f" - Content Type: {file.content_type}")
    
    print("----------------------------\n")

    # --- RETURN DUMMY RESPONSE ---
    # We send this back so Node.js doesn't crash while waiting
    return {
        "answer": f"Python received {len(files)} files. Prompt: '{userprompt}'",
        "sources": ["System Log", "Python Backend"]
    }

# --- 3. Run Server (Optional if using terminal command) ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
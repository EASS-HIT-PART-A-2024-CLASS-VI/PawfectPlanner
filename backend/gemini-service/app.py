from fastapi import FastAPI, HTTPException, Request
import httpx
import os

# Initialize the FastAPI app
app = FastAPI()

# Load the Gemini API key from the environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/gemini/query")
async def query_gemini(request: Request):
    """
    Endpoint to query the Gemini API with a user-provided prompt and return the response.
    """
    try:
        # Parse JSON from the request
        body = await request.json()
        prompt = body.get("prompt", "")
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # Define headers and payload for the Gemini API request
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
        payload = {"prompt": prompt}

        # Query the Gemini API using an asynchronous HTTP client
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.google.com/gemini/v1/query", headers=headers, json=payload)
            response.raise_for_status()
        
        # Return the API response to the user
        return {"response": response.json()}
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

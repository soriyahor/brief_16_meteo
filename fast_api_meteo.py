from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
from typing import Optional

from to_speech import get_text_from_forecast, get_speach_from_text

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get('/test') 
async def test():
    print("coucou")


@app.get("/forecast")
async def forecast(city: str, date: str, hour: Optional[int] = None):
    try:
        text = get_text_from_forecast(city, date, hour)  # Pass the hour argument
        audio_file = get_speach_from_text(text, city, date, hour)
        print('audio_file', audio_file)
        return StreamingResponse(io.BytesIO(audio_file), media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=audio.mp3"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8020)
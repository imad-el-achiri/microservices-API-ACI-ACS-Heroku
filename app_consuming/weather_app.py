from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import uvicorn
import json
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

url = 'https://imad-weather-app-11317224e11b.herokuapp.com/predict'
headers = {'Content-Type':'application/json'}

class weather(BaseModel):
    Temperature_C: int
    Humidity: int
    Wind_speed_kmph: int
    Wind_bearing_degrees: int
    Visibility_km: int
    Pressure_millibars: int
    Current_weather_condition: int

@app.get("/")
def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post('/predict', response_class=HTMLResponse)
async def make_predictions(request: Request, Temperature_C: int = Form(...), Humidity: int = Form(...), Wind_speed_kmph: int = Form(...), Wind_bearing_degrees: int = Form(...), Visibility_km: int = Form(...), Pressure_millibars: int = Form(...), Current_weather_condition: int = Form(...)):
    inference_data = [int(Temperature_C), int(Humidity), int(Wind_speed_kmph), int(Wind_bearing_degrees), int(Visibility_km), int(Pressure_millibars), int(Current_weather_condition)]
    inference_data = json.dumps({"data": [inference_data]})
    r = requests.post(url, data=inference_data, headers=headers)
    result = r.content
    res = str(r.content)
    #print(res[-5])

    if (res[-5] == 1):
        result = "No rain"
    else:
        result = "Rain"
   
    return templates.TemplateResponse("index.html", {"request": request, "result":result})




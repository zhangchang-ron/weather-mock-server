from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
import random
from datetime import datetime, timedelta

app = FastAPI(
    title="Weather Mock API",
    description="一个模拟天气数据的 API 服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    date: str
    temperature: float
    weather: str
    humidity: int
    wind_speed: float

class WeatherMock:
    def __init__(self):
        self.weather_conditions = [
            "晴天", "多云", "阴天", "小雨", "中雨", "大雨", 
            "雷阵雨", "小雪", "中雪", "大雪"
        ]
        
    def get_random_temperature(self, season="summer"):
        if season == "summer":
            return round(random.uniform(20, 35), 1)
        elif season == "winter":
            return round(random.uniform(-5, 15), 1)
        else:
            return round(random.uniform(10, 25), 1)
    
    def get_random_humidity(self):
        return random.randint(30, 95)
    
    def get_random_wind_speed(self):
        return round(random.uniform(0, 30), 1)
    
    def get_random_weather(self):
        return random.choice(self.weather_conditions)
    
    def get_weather_data(self, days=1, season="summer"):
        weather_data = []
        current_date = datetime.now()
        
        for i in range(days):
            date = current_date + timedelta(days=i)
            weather = WeatherResponse(
                date=date.strftime("%Y-%m-%d"),
                temperature=self.get_random_temperature(season),
                weather=self.get_random_weather(),
                humidity=self.get_random_humidity(),
                wind_speed=self.get_random_wind_speed()
            )
            weather_data.append(weather)
            
        return weather_data

weather_mock = WeatherMock()

@app.get("/", response_model=List[WeatherResponse])
async def get_weather(
    days: Optional[int] = Query(1, description="需要获取的天数", ge=1, le=15),
    season: Optional[str] = Query("summer", description="季节 (summer/winter/spring/autumn)")
):
    """
    获取天气预报数据
    
    - **days**: 需要获取的天数（1-15天）
    - **season**: 季节（summer/winter/spring/autumn）
    """
    return weather_mock.get_weather_data(days=days, season=season)

@app.get("/today", response_model=WeatherResponse)
async def get_today_weather(
    season: Optional[str] = Query("summer", description="季节 (summer/winter/spring/autumn)")
):
    """
    获取今天的天气数据
    
    - **season**: 季节（summer/winter/spring/autumn）
    """
    return weather_mock.get_weather_data(days=1, season=season)[0]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
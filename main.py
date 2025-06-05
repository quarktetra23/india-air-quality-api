from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load the dataset
df = pd.read_csv("data/city_day.csv")
df['Date'] = pd.to_datetime(df['Date'])

@app.get("/")
def root():
    return {"message": "Welcome to the India Air Quality API"}

@app.get("/cities")
def get_cities():
    """Return a sorted list of unique cities."""
    cities = df['City'].dropna().unique().tolist()
    return {"cities": sorted(cities)}

@app.get("/city/{city_name}")
def get_city_data(city_name: str):
    """Return recent air quality data for a specific city."""
    city_df = df[df['City'].str.lower() == city_name.lower()]
    if city_df.empty:
        return {"error": "City not found"}
    
    latest = city_df.sort_values(by="Date", ascending=False).iloc[0]
    return {
        "city": latest['City'],
        "date": str(latest['Date'].date()),
        "PM2.5": latest['PM2.5'],
        "PM10": latest['PM10'],
        "NO2": latest['NO2'],
        "SO2": latest['SO2'],
        "CO": latest['CO'],
        "O3": latest['O3']
    }

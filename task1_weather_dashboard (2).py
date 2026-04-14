"""
CODTECH Internship - Task 1
API Integration and Data Visualization

Description: Fetches weather data from OpenWeatherMap API and creates
             a multi-panel visualization dashboard using Matplotlib/Seaborn.
"""

import requests
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
 

# ─────────────────────────────────────────────
API_KEY  = "5e239ca30ea79676c352c44042d534aa"   # <-- paste your key here
CITIES   = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
UNITS    = "metric"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    """Fetch current weather data for a given city."""
    params = {"q": city, "appid": API_KEY, "units": UNITS}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city":        data["name"],
            "temp":        data["main"]["temp"],
            "feels_like":  data["main"]["feels_like"],
            "humidity":    data["main"]["humidity"],
            "wind_speed":  data["wind"]["speed"],
            "pressure":    data["main"]["pressure"],
            "weather":     data["weather"][0]["description"].title(),
            "visibility":  data.get("visibility", 0) / 1000,
        }
    except requests.exceptions.HTTPError as e:
        print("HTTP Error for {}: {}".format(city, e))
    except requests.exceptions.ConnectionError:
        print("Connection Error for {}".format(city))
    except Exception as e:
        print("Error for {}: {}".format(city, e))
    return None


def get_all_weather(cities):
    """Fetch weather for all cities."""
    results = []
    for city in cities:
        print("Fetching weather for {}...".format(city))
        data = fetch_weather(city)
        if data:
            results.append(data)
            print("  OK {} : {}C, {}".format(city, data["temp"], data["weather"]))
        else:
            print("  SKIP {}".format(city))
    return results


def create_dashboard(weather_data):
    """Generate a 2x2 dashboard with 4 different charts."""
    if not weather_data:
        print("No data to visualize.")
        return

    cities     = [d["city"]       for d in weather_data]
    temps      = [d["temp"]       for d in weather_data]
    feels      = [d["feels_like"] for d in weather_data]
    humidity   = [d["humidity"]   for d in weather_data]
    wind_speed = [d["wind_speed"] for d in weather_data]
    pressure   = [d["pressure"]   for d in weather_data]
    visibility = [d["visibility"] for d in weather_data]

    sns.set_theme(style="darkgrid", palette="muted")

    fig = plt.figure(figsize=(16, 10), facecolor="#1a1a2e")
    fig.suptitle(
        "Weather Dashboard — {}".format(datetime.now().strftime("%d %b %Y, %H:%M")),
        fontsize=18, fontweight="bold", color="white", y=0.98
    )

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # Chart 1: Temperature vs Feels Like
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.arange(len(cities))
    w = 0.35
    ax1.bar(x - w/2, temps, w, label="Actual Temp", color="#e94560", alpha=0.85)
    ax1.bar(x + w/2, feels, w, label="Feels Like",  color="#0f3460", alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cities, rotation=20, ha="right", color="white", fontsize=9)
    ax1.set_ylabel("Temperature (C)", color="white")
    ax1.set_title("Temperature vs Feels Like", color="white", fontweight="bold")
    ax1.legend(facecolor="#2a2a3e", labelcolor="white", fontsize=8)
    ax1.tick_params(colors="white")
    ax1.set_facecolor("#2a2a3e")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#555")

    # Chart 2: Humidity
    ax2 = fig.add_subplot(gs[0, 1])
    colors = ["#48cae4" if h < 60 else "#0096c7" if h < 80 else "#023e8a" for h in humidity]
    bars = ax2.barh(cities, humidity, color=colors, edgecolor="white", linewidth=0.5)
    ax2.set_xlabel("Humidity (%)", color="white")
    ax2.set_title("Humidity Levels", color="white", fontweight="bold")
    ax2.set_xlim(0, 110)
    ax2.tick_params(colors="white")
    ax2.set_facecolor("#2a2a3e")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#555")
    for bar, val in zip(bars, humidity):
        ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
                 "{}%".format(val), va="center", color="white", fontsize=9)

    # Chart 3: Wind Speed
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(cities, wind_speed, marker="o", color="#f4d03f",
             linewidth=2.5, markersize=8, markerfacecolor="white")
    ax3.fill_between(range(len(cities)), wind_speed, alpha=0.2, color="#f4d03f")
    for i, (c, ws) in enumerate(zip(cities, wind_speed)):
        ax3.annotate("{} m/s".format(ws), (c, ws), textcoords="offset points",
                     xytext=(0, 10), ha="center", color="white", fontsize=8)
    ax3.set_xticks(range(len(cities)))
    ax3.set_xticklabels(cities, rotation=20, ha="right", color="white", fontsize=9)
    ax3.set_ylabel("Wind Speed (m/s)", color="white")
    ax3.set_title("Wind Speed by City", color="white", fontweight="bold")
    ax3.tick_params(colors="white")
    ax3.set_facecolor("#2a2a3e")
    for spine in ax3.spines.values():
        spine.set_edgecolor("#555")

    # Chart 4: Pressure & Visibility
    ax4  = fig.add_subplot(gs[1, 1])
    ax4b = ax4.twinx()
    ax4.bar(cities, pressure, color="#a29bfe", alpha=0.7, label="Pressure (hPa)", width=0.4)
    ax4b.plot(cities, visibility, color="#fd79a8", marker="^", linewidth=2,
              markersize=8, label="Visibility (km)")
    ax4.set_ylabel("Pressure (hPa)", color="#a29bfe")
    ax4b.set_ylabel("Visibility (km)", color="#fd79a8")
    ax4.set_title("Pressure & Visibility", color="white", fontweight="bold")
    ax4.tick_params(axis="x", rotation=20, labelcolor="white", labelsize=9)
    ax4.tick_params(axis="y", colors="#a29bfe")
    ax4b.tick_params(axis="y", colors="#fd79a8")
    ax4.set_facecolor("#2a2a3e")
    for spine in ax4.spines.values():
        spine.set_edgecolor("#555")
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2,
               facecolor="#2a2a3e", labelcolor="white", fontsize=8, loc="lower right")

    output_path = "weather_dashboard.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print("\nDashboard saved as '{}'".format(output_path))
    plt.show()


DEMO_DATA = [
    {"city": "Mumbai",    "temp": 33, "feels_like": 38, "humidity": 80,
     "wind_speed": 4.5,  "pressure": 1008, "weather": "Haze",          "visibility": 3.0},
    {"city": "Delhi",     "temp": 38, "feels_like": 41, "humidity": 35,
     "wind_speed": 3.1,  "pressure": 1002, "weather": "Clear Sky",     "visibility": 8.0},
    {"city": "Bangalore", "temp": 27, "feels_like": 28, "humidity": 65,
     "wind_speed": 2.8,  "pressure": 1015, "weather": "Partly Cloudy", "visibility": 10.0},
    {"city": "Chennai",   "temp": 35, "feels_like": 40, "humidity": 72,
     "wind_speed": 5.2,  "pressure": 1006, "weather": "Thunderstorm",  "visibility": 5.0},
    {"city": "Kolkata",   "temp": 36, "feels_like": 42, "humidity": 78,
     "wind_speed": 3.7,  "pressure": 1004, "weather": "Mostly Cloudy", "visibility": 6.5},
]

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("=" * 55)
        print("  No API key set — running in DEMO MODE")
        print("  Get a free key at https://openweathermap.org/api")
        print("=" * 55)
        weather_data = DEMO_DATA
    else:
        weather_data = get_all_weather(CITIES)

    create_dashboard(weather_data)

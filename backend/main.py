from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime
from typing import List, Dict
import math

app = FastAPI(title="HydroFlow Metro Crowd Detector API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Station definitions with coordinates (27 stations)
STATIONS = [
    # Red Line
    {"id": 1, "name": "LB Nagar", "line": "red", "x": 600, "y": 500, "capacity": 500, "coachTip": "Commercial hub"},
    {"id": 2, "name": "Victoria Memorial", "line": "red", "x": 550, "y": 450, "capacity": 450},
    {"id": 3, "name": "Chaitanyapuri", "line": "red", "x": 500, "y": 400, "capacity": 400},
    {"id": 4, "name": "Dilsukhnagar", "line": "red", "x": 450, "y": 350, "capacity": 600, "coachTip": "Major interchange"},
    {"id": 5, "name": "Moosarambagh", "line": "red", "x": 400, "y": 300, "capacity": 400},
    {"id": 6, "name": "Malakpet", "line": "red", "x": 350, "y": 250, "capacity": 450},
    {"id": 7, "name": "Parade Ground", "line": "red", "x": 300, "y": 200, "capacity": 500, "coachTip": "Central hub"},
    {"id": 8, "name": "Ameerpet", "line": "red", "x": 250, "y": 150, "capacity": 700, "coachTip": "Super busy! Coaching institutes area"},
    {"id": 9, "name": "SR Nagar", "line": "red", "x": 200, "y": 120, "capacity": 400},
    {"id": 10, "name": "ESI Hospital", "line": "red", "x": 150, "y": 90, "capacity": 350},
    {"id": 11, "name": "KPHB Colony", "line": "red", "x": 100, "y": 60, "capacity": 550, "coachTip": "Residential hub"},
    {"id": 12, "name": "Miyapur", "line": "red", "x": 50, "y": 30, "capacity": 600, "coachTip": "Terminal station"},
    
    # Green Line
    {"id": 13, "name": "Nagole", "line": "green", "x": 650, "y": 350, "capacity": 500, "coachTip": "Terminal station"},
    {"id": 14, "name": "Uppal", "line": "green", "x": 600, "y": 330, "capacity": 450},
    {"id": 15, "name": "Stadium", "line": "green", "x": 550, "y": 310, "capacity": 400},
    {"id": 16, "name": "NGRI", "line": "green", "x": 500, "y": 290, "capacity": 350},
    {"id": 17, "name": "Habsiguda", "line": "green", "x": 450, "y": 270, "capacity": 400},
    {"id": 18, "name": "Tarnaka", "line": "green", "x": 400, "y": 250, "capacity": 450},
    {"id": 19, "name": "Mettuguda", "line": "green", "x": 350, "y": 230, "capacity": 350},
    {"id": 20, "name": "Secunderabad East", "line": "green", "x": 300, "y": 210, "capacity": 400},
    {"id": 21, "name": "Begumpet", "line": "green", "x": 250, "y": 180, "capacity": 450},
    {"id": 22, "name": "Moosapet", "line": "green", "x": 200, "y": 150, "capacity": 400},
    {"id": 23, "name": "JNTU", "line": "green", "x": 150, "y": 120, "capacity": 550, "coachTip": "University area"},
    
    # Blue Line
    {"id": 24, "name": "Raidurg", "line": "blue", "x": 100, "y": 200, "capacity": 500, "coachTip": "IT corridor"},
    {"id": 25, "name": "Hitech City", "line": "blue", "x": 150, "y": 230, "capacity": 700, "coachTip": "Super busy! IT hub"},
    {"id": 26, "name": "Nanakramguda", "line": "blue", "x": 200, "y": 260, "capacity": 550, "coachTip": "Financial district"},
    {"id": 27, "name": "Gachibowli", "line": "blue", "x": 120, "y": 180, "capacity": 600, "coachTip": "DLF Cybercity area"},
]

def get_crowd_level(passengers: int) -> str:
    """Classify traffic level based on passenger count"""
    if passengers < 100:
        return "LOW"
    elif passengers < 300:
        return "MEDIUM"
    elif passengers < 400:
        return "HIGH"
    else:
        return "PEAK"

def get_rush_level(occupancy_percent: float) -> str:
    """Classify train rush level based on occupancy percentage"""
    if occupancy_percent < 40:
        return "Low Rush"
    elif occupancy_percent < 70:
        return "Moderate Rush"
    else:
        return "High Rush"

def generate_station_traffic(station: Dict, current_hour: int) -> Dict:
    """Generate realistic traffic for a station based on time and capacity"""
    # Peak hours: 9-11 AM (9-11) and 5-8 PM (17-20)
    is_peak_hour = (9 <= current_hour <= 11) or (17 <= current_hour <= 20)
    
    # Base multiplier based on time
    if is_peak_hour:
        time_multiplier = random.uniform(0.6, 0.9)
    else:
        time_multiplier = random.uniform(0.1, 0.4)
    
    # Calculate passengers
    passengers = int(station["capacity"] * time_multiplier)
    
    # Add some randomness
    passengers += random.randint(-50, 50)
    passengers = max(0, passengers)
    
    return {
        **station,
        "passengers": passengers,
        "status": get_crowd_level(passengers),
        "trend": random.choice(["increasing", "decreasing", "stable"]),
        "waitTime": random.randint(2, 8),
        "lastUpdated": datetime.now().isoformat()
    }

def generate_train_data(current_hour: int) -> List[Dict]:
    """Generate realistic train data with seat availability"""
    is_peak_hour = (9 <= current_hour <= 11) or (17 <= current_hour <= 20)
    
    trains = []
    num_trains = random.randint(8, 12)
    
    for i in range(num_trains):
        # Train capacity
        total_capacity = 350
        seats = 50
        standing_capacity = 300
        
        # Generate occupancy based on peak hours
        if is_peak_hour:
            current_occupancy = random.randint(200, 340)
        else:
            current_occupancy = random.randint(50, 200)
        
        occupancy_percent = (current_occupancy / total_capacity) * 100
        seated_passengers = min(current_occupancy, seats)
        standing_passengers = max(0, current_occupancy - seats)
        available_seats = max(0, seats - seated_passengers)
        
        # Random position on lines
        line = random.choice(["red", "green", "blue"])
        progress = random.random()
        
        trains.append({
            "id": f"T{100 + i}",
            "line": line,
            "position": progress,
            "current_occupancy": current_occupancy,
            "total_capacity": total_capacity,
            "occupancy_percent": round(occupancy_percent, 1),
            "seat_rush_level": get_rush_level(occupancy_percent),
            "available_seats": available_seats,
            "standing_passengers": standing_passengers,
            "direction": random.choice(["northbound", "southbound", "eastbound", "westbound"]),
            "speed": random.randint(40, 60),
            "nextStation": random.choice(STATIONS)["name"]
        })
    
    return trains

@app.get("/")
def root():
    return {
        "message": "HydroFlow 1.0 - Metro Crowd Detection System API",
        "version": "1.0.0",
        "endpoints": [
            "/status",
            "/trains",
            "/analytics/overview",
            "/analytics/peak-predictions"
        ]
    }

@app.get("/status")
def get_status():
    """Get current status of all stations"""
    current_hour = datetime.now().hour
    
    stations_with_traffic = [
        generate_station_traffic(station, current_hour)
        for station in STATIONS
    ]
    
    total_passengers = sum(s["passengers"] for s in stations_with_traffic)
    peak_stations = [s for s in stations_with_traffic if s["status"] in ["HIGH", "PEAK"]]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "stations": stations_with_traffic,
        "summary": {
            "totalStations": len(STATIONS),
            "totalPassengers": total_passengers,
            "peakStations": len(peak_stations),
            "averageWaitTime": round(sum(s["waitTime"] for s in stations_with_traffic) / len(stations_with_traffic), 1)
        }
    }

@app.get("/trains")
def get_trains():
    """Get current train positions and seat availability"""
    current_hour = datetime.now().hour
    trains = generate_train_data(current_hour)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "trains": trains,
        "summary": {
            "totalTrains": len(trains),
            "averageOccupancy": round(sum(t["occupancy_percent"] for t in trains) / len(trains), 1),
            "highRushTrains": len([t for t in trains if t["seat_rush_level"] == "High Rush"])
        }
    }

@app.get("/analytics/overview")
def get_analytics_overview():
    """Get comprehensive system analytics overview"""
    from advanced_analytics import analytics_engine
    current_hour = datetime.now().hour
    
    stations_with_traffic = [
        generate_station_traffic(station, current_hour)
        for station in STATIONS
    ]
    
    trains = generate_train_data(current_hour)
    
    # Run analytics
    patterns = analytics_engine.analyze_crowd_patterns(stations_with_traffic)
    anomalies = analytics_engine.detect_anomalies(stations_with_traffic)
    network_flow = analytics_engine.analyze_network_flow(stations_with_traffic)
    bottlenecks = analytics_engine.identify_bottlenecks(stations_with_traffic, trains)
    peak_info = analytics_engine.detect_peak_hours(current_hour)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "patterns": patterns,
        "anomalies": anomalies,
        "network_flow": network_flow,
        "bottlenecks": bottlenecks,
        "peak_info": peak_info
    }

@app.get("/analytics/peak-predictions")
def get_peak_predictions(hours_ahead: int = 3):
    """Get ML-powered crowd predictions"""
    from ml_prediction_engine import ml_engine
    
    # Generate historical data
    historical = [random.randint(100, 400) for _ in range(24)]
    predictions = ml_engine.predict_crowd(historical, hours_ahead)
    
    return predictions

@app.get("/analytics/network-flow")
def get_network_flow():
    """Get network flow analysis"""
    from flow_analysis_engine import flow_analyzer
    current_hour = datetime.now().hour
    
    stations_with_traffic = [
        generate_station_traffic(station, current_hour)
        for station in STATIONS
    ]
    trains = generate_train_data(current_hour)
    
    return flow_analyzer.analyze_flow_path(stations_with_traffic, trains)

@app.get("/analytics/revenue")
def get_revenue_analytics():
    """Get revenue analytics by corridor"""
    from revenue_engine import revenue_engine as rev_engine
    current_hour = datetime.now().hour
    
    stations_with_traffic = [
        generate_station_traffic(station, current_hour)
        for station in STATIONS
    ]
    
    return rev_engine.calculate_corridor_revenue(stations_with_traffic)

@app.post("/incident/simulate")
def simulate_incident(incident_type: str = "delay", station_id: int = None):
    """Simulate a service disruption"""
    from incident_engine import incident_engine as inc_engine
    return inc_engine.simulate_incident(incident_type, station_id)

@app.get("/incident/active")
def get_active_incidents():
    """Get all active incidents"""
    from incident_engine import incident_engine as inc_engine
    return {
        "active_incidents": inc_engine.get_active_incidents(),
        "total_active": len(inc_engine.get_active_incidents())
    }

@app.post("/ai/chat")
def chat_with_ai(query: str):
    """Chat with AI assistant"""
    from ai_assistant_engine import ai_assistant
    current_hour = datetime.now().hour
    
    context = {
        "current_hour": current_hour,
        "is_peak": (9 <= current_hour <= 11) or (17 <= current_hour <= 20)
    }
    
    return ai_assistant.process_query(query, context)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting HydroFlow Metro Crowd Detector API...")
    print("📍 Server will run on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n✨ Available Endpoints:")
    print("   - GET  /status                    (Station traffic data)")
    print("   - GET  /trains                    (Train positions & seats)")
    print("   - GET  /analytics/overview        (System analytics)")
    print("   - GET  /analytics/peak-predictions (ML predictions)")
    print("   - GET  /analytics/network-flow    (Flow analysis)")
    print("   - GET  /analytics/revenue         (Revenue analytics)")
    print("   - POST /incident/simulate         (Simulate incidents)")
    print("   - GET  /incident/active           (Active incidents)")
    print("   - POST /ai/chat                   (AI assistant)")
    print("\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

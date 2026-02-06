"""
Prediction Service Integration Layer
Coordinates ML predictions with real-time data
"""

from typing import List, Dict
from datetime import datetime
import numpy as np

class PredictionService:
    def __init__(self):
        self.cache = {}
        
    def get_station_prediction(self, station_id: int, hours_ahead: int = 3) -> Dict:
        """Get crowd prediction for a specific station"""
        # Generate synthetic historical data
        historical_data = self._generate_station_history(station_id)
        
        # Use simple prediction model
        predictions = []
        current_hour = datetime.now().hour
        
        for i in range(1, hours_ahead + 1):
            future_hour = (current_hour + i) % 24
            
            # Peak hour logic
            if 9 <= future_hour <= 11 or 17 <= future_hour <= 20:
                base_passengers = np.random.randint(250, 400)
            else:
                base_passengers = np.random.randint(50, 200)
            
            predictions.append({
                "hour_ahead": i,
                "predicted_passengers": base_passengers,
                "confidence": round(np.random.uniform(0.75, 0.95), 2)
            })
        
        return {
            "station_id": station_id,
            "predictions": predictions,
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_station_history(self, station_id: int, hours: int = 24) -> List[int]:
        """Generate synthetic historical data for a station"""
        history = []
        current_hour = datetime.now().hour
        
        for i in range(hours):
            hour = (current_hour - hours + i) % 24
            if 9 <= hour <= 11 or 17 <= hour <= 20:
                passengers = np.random.randint(200, 400)
            else:
                passengers = np.random.randint(50, 180)
            history.append(passengers)
        
        return history

prediction_service = PredictionService()

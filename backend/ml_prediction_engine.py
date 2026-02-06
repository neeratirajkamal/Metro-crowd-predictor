"""
ML Prediction Engine for Metro Crowd Forecasting
Implements multiple prediction models with ensemble methods
"""

import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class MLPredictionEngine:
    def __init__(self):
        self.models = ["sma", "exponential_smoothing", "polynomial", "ensemble"]
        
    def predict_crowd(self, historical_data: List[int], hours_ahead: int = 3, 
                     model: str = "ensemble") -> Dict:
        """Predict crowd levels for future hours"""
        if len(historical_data) < 10:
            # Generate synthetic historical data if insufficient
            historical_data = self._generate_synthetic_history()
        
        predictions = {}
        
        if model == "sma" or model == "ensemble":
            predictions["sma"] = self._simple_moving_average(historical_data, hours_ahead)
        
        if model == "exponential_smoothing" or model == "ensemble":
            predictions["exponential"] = self._exponential_smoothing(historical_data, hours_ahead)
        
        if model == "polynomial" or model == "ensemble":
            predictions["polynomial"] = self._polynomial_regression(historical_data, hours_ahead)
        
        if model == "ensemble":
            predictions["ensemble"] = self._ensemble_prediction(predictions)
            return self._format_prediction(predictions["ensemble"], hours_ahead)
        else:
            return self._format_prediction(predictions[model], hours_ahead)
    
    def _simple_moving_average(self, data: List[int], hours: int, window: int = 5) -> List[float]:
        """Simple Moving Average prediction"""
        predictions = []
        for i in range(hours):
            if len(data) >= window:
                pred = np.mean(data[-window:])
            else:
                pred = np.mean(data)
            predictions.append(pred)
            data.append(pred)  # Use prediction for next iteration
        return predictions
    
    def _exponential_smoothing(self, data: List[int], hours: int, alpha: float = 0.3) -> List[float]:
        """Exponential Smoothing prediction"""
        if len(data) == 0:
            return [0] * hours
        
        predictions = []
        last_value = data[-1]
        
        for _ in range(hours):
            # Simple exponential smoothing
            pred = alpha * last_value + (1 - alpha) * np.mean(data[-10:] if len(data) >= 10 else data)
            predictions.append(pred)
            last_value = pred
        
        return predictions
    
    def _polynomial_regression(self, data: List[int], hours: int, degree: int = 2) -> List[float]:
        """Polynomial Regression prediction"""
        if len(data) < degree + 1:
            return [np.mean(data)] * hours
        
        x = np.arange(len(data))
        y = np.array(data)
        
        # Fit polynomial
        coefficients = np.polyfit(x, y, degree)
        poly = np.poly1d(coefficients)
        
        # Predict future values
        future_x = np.arange(len(data), len(data) + hours)
        predictions = poly(future_x)
        
        # Ensure non-negative predictions
        predictions = np.maximum(predictions, 0)
        
        return predictions.tolist()
    
    def _ensemble_prediction(self, predictions: Dict[str, List[float]]) -> List[float]:
        """Combine predictions using weighted average"""
        # Weights for different models
        weights = {
            "sma": 0.3,
            "exponential": 0.3,
            "polynomial": 0.4
        }
        
        ensemble = []
        num_predictions = len(predictions["sma"])
        
        for i in range(num_predictions):
            weighted_sum = 0
            for model, weight in weights.items():
                if model in predictions:
                    weighted_sum += predictions[model][i] * weight
            ensemble.append(weighted_sum)
        
        return ensemble
    
    def _generate_synthetic_history(self, hours: int = 24) -> List[int]:
        """Generate synthetic historical data for testing"""
        current_hour = datetime.now().hour
        history = []
        
        for i in range(hours):
            hour = (current_hour - hours + i) % 24
            # Simulate peak hours
            if 9 <= hour <= 11 or 17 <= hour <= 20:
                base = np.random.randint(250, 400)
            else:
                base = np.random.randint(50, 200)
            history.append(base)
        
        return history
    
    def _format_prediction(self, predictions: List[float], hours: int) -> Dict:
        """Format prediction output with confidence intervals"""
        current_time = datetime.now()
        
        formatted_predictions = []
        for i, pred in enumerate(predictions):
            hour_ahead = i + 1
            future_time = current_time + timedelta(hours=hour_ahead)
            
            # Calculate confidence interval (±15% for demonstration)
            confidence_margin = pred * 0.15
            
            formatted_predictions.append({
                "hour": hour_ahead,
                "timestamp": future_time.isoformat(),
                "predicted_passengers": int(pred),
                "confidence_interval": {
                    "lower": int(pred - confidence_margin),
                    "upper": int(pred + confidence_margin)
                },
                "confidence_score": round(85 + np.random.uniform(-5, 5), 1)
            })
        
        return {
            "predictions": formatted_predictions,
            "model_used": "ensemble",
            "prediction_horizon_hours": hours,
            "generated_at": current_time.isoformat()
        }
    
    def predict_peak_times(self, station_id: int, date: str = None) -> Dict:
        """Predict peak times for a specific station"""
        # Simulated peak time predictions
        current_hour = datetime.now().hour
        
        peaks = []
        
        # Morning peak
        if current_hour < 11:
            peaks.append({
                "time": "09:00-11:00",
                "type": "morning_peak",
                "expected_passengers": np.random.randint(300, 450),
                "confidence": 0.88
            })
        
        # Evening peak
        if current_hour < 20:
            peaks.append({
                "time": "17:00-20:00",
                "type": "evening_peak",
                "expected_passengers": np.random.randint(350, 500),
                "confidence": 0.85
            })
        
        return {
            "station_id": station_id,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "predicted_peaks": peaks,
            "recommendation": "Increase train frequency during predicted peak times"
        }

# Global instance
ml_engine = MLPredictionEngine()

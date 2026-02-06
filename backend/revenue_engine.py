"""
Revenue Analytics Engine
Financial analytics for metro operations
"""

from typing import Dict, List
import random

class RevenueEngine:
    def __init__(self):
        self.base_fare = 10  # Rupees
        self.per_km_rate = 2
        
    def calculate_corridor_revenue(self, stations: List[Dict]) -> Dict:
        """Calculate revenue by corridor"""
        corridors = {}
        
        for station in stations:
            line = station["line"]
            if line not in corridors:
                corridors[line] = {
                    "line": line,
                    "total_passengers": 0,
                    "estimated_revenue": 0,
                    "stations": 0
                }
            
            passengers = station["passengers"]
            avg_fare = self.base_fare + (random.randint(1, 10) * self.per_km_rate)
            revenue = passengers * avg_fare
            
            corridors[line]["total_passengers"] += passengers
            corridors[line]["estimated_revenue"] += revenue
            corridors[line]["stations"] += 1
        
        return {
            "corridors": list(corridors.values()),
            "total_revenue": sum(c["estimated_revenue"] for c in corridors.values())
        }

revenue_engine = RevenueEngine()

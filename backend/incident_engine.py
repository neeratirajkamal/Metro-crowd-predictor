"""
Incident Management Engine
Simulates and manages service disruptions
"""

from typing import List, Dict
from datetime import datetime
import random

class IncidentEngine:
    def __init__(self):
        self.active_incidents = []
        
    def simulate_incident(self, incident_type: str, station_id: int = None) -> Dict:
        """Simulate a service disruption"""
        incident_types = {
            "delay": "Train delay due to technical issue",
            "overcrowding": "Platform overcrowding detected",
            "signal_failure": "Signal failure on track",
            "medical_emergency": "Medical emergency on platform"
        }
        
        incident = {
            "id": f"INC{random.randint(1000, 9999)}",
            "type": incident_type,
            "description": incident_types.get(incident_type, "Unknown incident"),
            "station_id": station_id or random.randint(1, 27),
            "severity": random.choice(["low", "medium", "high"]),
            "status": "active",
            "reported_at": datetime.now().isoformat(),
            "estimated_resolution_minutes": random.randint(5, 30)
        }
        
        self.active_incidents.append(incident)
        return incident
    
    def get_active_incidents(self) -> List[Dict]:
        """Get all active incidents"""
        return [i for i in self.active_incidents if i["status"] == "active"]

incident_engine = IncidentEngine()

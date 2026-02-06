"""
AI Assistant Engine
Context-aware conversational AI for metro travel assistance
"""

from typing import Dict, List
from datetime import datetime

class AIAssistantEngine:
    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = {
            "routes": "Hyderabad Metro has 3 lines: Red (Miyapur-LB Nagar), Green (Nagole-JNTU), Blue (Raidurg-Hitech City)",
            "fares": "Metro fares start from ₹10 and go up to ₹60 based on distance",
            "timings": "Metro operates from 6:00 AM to 11:00 PM daily",
            "frequency": "Train frequency is 3-7 minutes during peak hours, 10-15 minutes during off-peak"
        }
        
    def process_query(self, query: str, context: Dict = None) -> Dict:
        """Process user query with context awareness"""
        query_lower = query.lower()
        
        # Simple keyword-based responses
        if "route" in query_lower or "how to" in query_lower:
            response = self._get_route_advice(context)
        elif "crowd" in query_lower or "busy" in query_lower:
            response = self._get_crowd_info(context)
        elif "time" in query_lower or "when" in query_lower:
            response = self._get_timing_info()
        elif "fare" in query_lower or "cost" in query_lower:
            response = self._get_fare_info()
        else:
            response = "I can help you with routes, crowd information, timings, and fares. What would you like to know?"
        
        return {
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }
    
    def _get_route_advice(self, context: Dict = None) -> str:
        """Provide route recommendations"""
        return ("The Hyderabad Metro has 3 main lines. Red Line connects Miyapur to LB Nagar, "
                "Green Line runs from Nagole to JNTU, and Blue Line serves the IT corridor from "
                "Raidurg to Hitech City. Where would you like to go?")
    
    def _get_crowd_info(self, context: Dict = None) -> str:
        """Provide crowd-related information"""
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 11:
            return ("Currently in morning peak hours (9-11 AM). Stations like Ameerpet, "
                   "Hitech City, and JNTU are expected to be very busy. Consider traveling "
                   "slightly earlier or later if possible.")
        elif 17 <= current_hour <= 20:
            return ("Currently in evening peak hours (5-8 PM). Heavy crowds expected at IT corridor "
                   "stations (Hitech City, Gachibowli) and major interchanges like Ameerpet.")
        else:
            return "Good time to travel! Off-peak hours mean less crowding and shorter wait times."
    
    def _get_timing_info(self) -> str:
        """Provide timing information"""
        return ("Hyderabad Metro operates from 6:00 AM to 11:00 PM daily. First train starts at 6 AM, "
                "last train departs around 10:30 PM from terminal stations.")
    
    def _get_fare_info(self) -> str:
        """Provide fare information"""
        return ("Metro fares are distance-based, starting from ₹10 for short distances up to ₹60 for "
                "longer journeys. You can use metro cards, QR codes, or mobile payment apps like "
                "PhonePe, Paytm, and GPay.")

ai_assistant = AIAssistantEngine()

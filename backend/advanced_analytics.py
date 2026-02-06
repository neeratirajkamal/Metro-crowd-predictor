"""
Advanced Analytics Engine for Metro Crowd Detection
Provides statistical analysis, anomaly detection, and network flow optimization
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple
import networkx as nx
from datetime import datetime, timedelta

class AdvancedAnalytics:
    def __init__(self):
        self.historical_data = []
        
    def analyze_crowd_patterns(self, stations: List[Dict]) -> Dict:
        """Analyze crowd patterns across all stations"""
        passengers = [s["passengers"] for s in stations]
        
        return {
            "mean": round(np.mean(passengers), 2),
            "median": round(np.median(passengers), 2),
            "std_dev": round(np.std(passengers), 2),
            "min": int(np.min(passengers)),
            "max": int(np.max(passengers)),
            "total": int(np.sum(passengers))
        }
    
    def detect_anomalies(self, stations: List[Dict]) -> List[Dict]:
        """Detect anomalies using Z-score and IQR methods"""
        passengers = np.array([s["passengers"] for s in stations])
        
        # Z-score method
        z_scores = np.abs(stats.zscore(passengers))
        z_anomalies = z_scores > 2.5
        
        # IQR method
        q1, q3 = np.percentile(passengers, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        iqr_anomalies = (passengers < lower_bound) | (passengers > upper_bound)
        
        # Combine results
        anomalies = []
        for i, station in enumerate(stations):
            if z_anomalies[i] or iqr_anomalies[i]:
                anomalies.append({
                    "station_id": station["id"],
                    "station_name": station["name"],
                    "passengers": station["passengers"],
                    "z_score": round(float(z_scores[i]), 2),
                    "severity": "high" if z_scores[i] > 3 else "medium",
                    "reason": "Unusually high crowd" if station["passengers"] > np.mean(passengers) else "Unusually low crowd"
                })
        
        return anomalies
    
    def analyze_network_flow(self, stations: List[Dict]) -> Dict:
        """Analyze network flow using graph algorithms"""
        # Create network graph
        G = nx.Graph()
        
        # Add stations as nodes
        for station in stations:
            G.add_node(station["id"], 
                      name=station["name"],
                      passengers=station["passengers"],
                      line=station["line"])
        
        # Add edges based on metro lines
        red_line = [s["id"] for s in stations if s["line"] == "red"]
        green_line = [s["id"] for s in stations if s["line"] == "green"]
        blue_line = [s["id"] for s in stations if s["line"] == "blue"]
        
        for line in [red_line, green_line, blue_line]:
            for i in range(len(line) - 1):
                G.add_edge(line[i], line[i + 1])
        
        # Calculate network metrics
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        
        # Find critical stations (high centrality)
        critical_stations = []
        for node_id, centrality in sorted(betweenness_centrality.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]:
            station = next(s for s in stations if s["id"] == node_id)
            critical_stations.append({
                "station_id": node_id,
                "station_name": station["name"],
                "betweenness_centrality": round(centrality, 4),
                "passengers": station["passengers"]
            })
        
        return {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "network_density": round(nx.density(G), 4),
            "critical_stations": critical_stations,
            "average_degree": round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2)
        }
    
    def identify_bottlenecks(self, stations: List[Dict], trains: List[Dict]) -> List[Dict]:
        """Identify bottlenecks in the metro network"""
        bottlenecks = []
        
        # Identify stations with high passengers and multiple trains
        for station in stations:
            if station["status"] in ["HIGH", "PEAK"]:
                # Count trains near this station
                nearby_trains = [t for t in trains 
                               if t["line"] == station["line"] 
                               and t["seat_rush_level"] in ["Moderate Rush", "High Rush"]]
                
                if len(nearby_trains) >= 2:
                    bottlenecks.append({
                        "station_id": station["id"],
                        "station_name": station["name"],
                        "passengers": station["passengers"],
                        "status": station["status"],
                        "nearby_trains": len(nearby_trains),
                        "severity": "critical" if station["status"] == "PEAK" else "warning",
                        "recommendation": f"Increase train frequency on {station['line']} line"
                    })
        
        return bottlenecks
    
    def detect_peak_hours(self, current_hour: int) -> Dict:
        """Detect and classify peak hours"""
        morning_peak = 9 <= current_hour <= 11
        evening_peak = 17 <= current_hour <= 20
        
        return {
            "current_hour": current_hour,
            "is_peak_hour": morning_peak or evening_peak,
            "peak_type": "morning" if morning_peak else ("evening" if evening_peak else "off-peak"),
            "next_peak_in_hours": self._calculate_next_peak(current_hour),
            "peak_intensity": self._calculate_peak_intensity(current_hour)
        }
    
    def _calculate_next_peak(self, current_hour: int) -> int:
        """Calculate hours until next peak"""
        if current_hour < 9:
            return 9 - current_hour
        elif current_hour < 17:
            return 17 - current_hour
        elif current_hour < 20:
            return 0  # Currently in evening peak
        else:
            return (24 - current_hour) + 9  # Next morning
    
    def _calculate_peak_intensity(self, current_hour: int) -> str:
        """Calculate peak intensity level"""
        if 9 <= current_hour <= 10 or 18 <= current_hour <= 19:
            return "high"
        elif current_hour == 11 or 17 <= current_hour <= 20:
            return "medium"
        else:
            return "low"

# Global instance
analytics_engine = AdvancedAnalytics()

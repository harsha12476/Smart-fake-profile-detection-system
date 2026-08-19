
import random
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt

class GeolocationRiskEngine:
    def __init__(self):
        self.high_risk_regions = [
            "Nigeria", "Russia", "China", "Brazil", "India", "Indonesia"
        ]
        
        self.cities = {
            "Bangalore": {"lat": 12.9716, "lng": 77.5946, "country": "India"},
            "New Delhi": {"lat": 28.6139, "lng": 77.2090, "country": "India"},
            "Mumbai": {"lat": 19.0760, "lng": 72.8777, "country": "India"},
            "New York": {"lat": 40.7128, "lng": -74.0060, "country": "USA"},
            "Los Angeles": {"lat": 34.0522, "lng": -118.2437, "country": "USA"},
            "London": {"lat": 51.5074, "lng": -0.1278, "country": "UK"},
            "Sao Paulo": {"lat": -23.5505, "lng": -46.6333, "country": "Brazil"},
            "Lagos": {"lat": 6.5244, "lng": 3.3792, "country": "Nigeria"},
            "Moscow": {"lat": 55.7558, "lng": 37.6173, "country": "Russia"},
            "Beijing": {"lat": 39.9042, "lng": 116.4074, "country": "China"},
            "Tokyo": {"lat": 35.6762, "lng": 139.6503, "country": "Japan"},
            "Sydney": {"lat": -33.8688, "lng": 151.2093, "country": "Australia"}
        }

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on earth (in km)"""
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r

    def generate_login_history(self, num_logins=10):
        """Generate sample login history for testing"""
        history = []
        cities_list = list(self.cities.keys())
        
        base_time = datetime.now()
        for i in range(num_logins):
            city = random.choice(cities_list)
            city_data = self.cities[city]
            time_diff = timedelta(hours=random.randint(1, 72))
            
            login_time = base_time - time_diff * i
            history.append({
                "city": city,
                "country": city_data["country"],
                "lat": city_data["lat"],
                "lng": city_data["lng"],
                "timestamp": login_time,
                "ip": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            })
        
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)

    def analyze_logins(self, login_history):
        """Analyze login history for risks"""
        if len(login_history) < 2:
            return {
                "multiple_locations": False,
                "impossible_travel": False,
                "high_risk_region": False,
                "location_anomalies": False,
                "risk_score": 0,
                "risk_level": "Safe",
                "details": []
            }
        
        details = []
        risk_score = 0
        
        # Check multiple locations
        unique_countries = set(l["country"] for l in login_history)
        if len(unique_countries) > 1:
            details.append(f"Multiple country logins: {', '.join(unique_countries)}")
            risk_score += 20
        
        unique_cities = set(l["city"] for l in login_history)
        if len(unique_cities) > 3:
            details.append(f"Multiple city logins: {len(unique_cities)} cities detected")
            risk_score += 15
        
        # Check impossible travel
        impossible_travel = False
        for i in range(1, len(login_history)):
            prev = login_history[i-1]
            curr = login_history[i]
            
            distance = self.haversine(prev["lat"], prev["lng"], curr["lat"], curr["lng"])
            time_diff = abs((prev["timestamp"] - curr["timestamp"]).total_seconds() / 3600)  # in hours
            
            # Assume average travel speed is 800 km/h (commercial plane)
            required_time = distance / 800
            
            if time_diff < required_time and distance > 500:
                impossible_travel = True
                details.append(f"Impossible travel detected: {prev['city']} → {curr['city']} ({round(distance, 0)} km in {round(time_diff, 1)} hours)")
                risk_score += 35
                break
        
        # Check high risk region
        high_risk = False
        for login in login_history:
            if login["country"] in self.high_risk_regions:
                high_risk = True
                details.append(f"Login from high-risk region: {login['city']}, {login['country']}")
                risk_score += 25
                break
        
        # Check location anomalies
        anomalies = False
        if len(unique_countries) > 2:
            anomalies = True
            details.append("Unusual number of country changes")
            risk_score += 10
        
        # Determine risk level
        if risk_score <= 20:
            risk_level = "Safe"
        elif risk_score <= 40:
            risk_level = "Low Risk"
        elif risk_score <= 60:
            risk_level = "Medium Risk"
        elif risk_score <= 80:
            risk_level = "High Risk"
        else:
            risk_level = "Critical Risk"
        
        return {
            "multiple_locations": len(unique_cities) > 1,
            "impossible_travel": impossible_travel,
            "high_risk_region": high_risk,
            "location_anomalies": anomalies,
            "risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "details": details,
            "login_history": login_history
        }

    def create_report(self, analysis_result):
        """Create a geolocation risk analysis report"""
        if not analysis_result or not analysis_result.get("login_history"):
            return None
            
        latest_login = analysis_result["login_history"][0]
        previous_login = analysis_result["login_history"][1] if len(analysis_result["login_history"]) > 1 else None
        
        report = {
            "current_location": f"{latest_login['city']}, {latest_login['country']}",
            "current_ip": latest_login["ip"],
            "previous_location": f"{previous_login['city']}, {previous_login['country']}" if previous_login else "N/A",
            "distance": self.haversine(latest_login["lat"], latest_login["lng"], 
                                       previous_login["lat"], previous_login["lng"]) if previous_login else 0,
            "travel_time": abs((latest_login["timestamp"] - previous_login["timestamp"]).total_seconds() / 60) if previous_login else 0,
            "risk_analysis": analysis_result["details"],
            "regional_threat_level": "Medium Risk" if latest_login["country"] in self.high_risk_regions else "Low Risk",
            "location_anomaly_score": analysis_result["risk_score"],
            "final_result": "Suspicious Login Activity Detected" if analysis_result["risk_score"] > 60 else "Normal Login Activity"
        }
        
        return report
        
    def analyze_locations(self, current_location, previous_locations):
        risk_score = 10
        login_region_analysis = "Normal"
        impossible_travel = False
        
        if not current_location:
            current_location = "Unknown"
            
        for region in previous_locations:
            if region.lower() in [r.lower() for r in self.high_risk_regions]:
                risk_score += 25
                
        if len(previous_locations) > 3:
            impossible_travel = True
            risk_score += 30
            
        if risk_score <= 20:
            risk_level = "Safe"
        elif risk_score <= 40:
            risk_level = "Medium Risk"
        elif risk_score <= 60:
            risk_level = "High Risk"
        else:
            risk_level = "Critical Risk"
            
        return {
            "current_location": current_location,
            "previous_locations": previous_locations,
            "impossible_travel": impossible_travel,
            "login_region_analysis": login_region_analysis,
            "location_risk_score": risk_score,
            "risk_level": risk_level
        }

engine = GeolocationRiskEngine()

# HydroFlow 1.0 - Metro Crowd Detector

An enterprise-grade intelligent transportation monitoring system for Hyderabad Metro with real-time crowd detection, ML predictions, and advanced analytics.

## 🚀 Features

- **Real-time Station Monitoring**: Track passenger traffic at 27 metro stations
- **4-Level Traffic Classification**: LOW, MEDIUM, HIGH, PEAK
- **Train Seat Availability**: Monitor occupancy and rush levels
- **Advanced Analytics**: ML-powered predictions, anomaly detection, network flow analysis
- **Interactive Network Map**: Visualize metro network with animated trains
- **Revenue Analytics**: Track corridor profitability
- **AI Assistant**: Context-aware travel recommendations
- **Incident Management**: Service disruption simulation

## 📋 Technology Stack

**Backend:**
- Python 3.13
- FastAPI
- Uvicorn
- NumPy, SciPy, NetworkX

**Frontend:**
- React 18
- Vite 6
- Tailwind CSS
- Lucide React Icons

## 🛠️ Installation & Setup

### Backend Setup

```powershell
# Navigate to backend directory
cd "C:\Users\LENOVO\Documents\Metro crowd detector\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

Backend will run on: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Frontend Setup

```powershell
# Navigate to frontend directory
cd "C:\Users\LENOVO\Documents\Metro crowd detector\frontend"

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /status` - Station traffic data
- `GET /trains` - Train positions & seat availability

### Analytics Endpoints
- `GET /analytics/overview` - System analytics overview
- `GET /analytics/peak-predictions` - ML crowd predictions
- `GET /analytics/network-flow` - Flow analysis
- `GET /analytics/revenue` - Revenue analytics

### Management Endpoints
- `POST /incident/simulate` - Simulate service disruption
- `GET /incident/active` - Active incidents
- `POST /ai/chat` - AI assistant chat

## 🎯 Usage

1. **Start Backend**: Run `python main.py` in the backend directory
2. **Start Frontend**: Run `npm run dev` in the frontend directory
3. **Open Browser**: Navigate to http://localhost:5173
4. **Explore**: Switch between Map, Dashboard, and Activity views

## 📊 Features Overview

### Network Map View
- Interactive SVG-based metro network visualization
- Color-coded stations (green → amber → orange → red)
- Animated trains with rush indicators
- Real-time station tooltips

### Dashboard View
- Live passenger statistics
- Train seat availability monitoring
- Peak station alerts
- Rush level indicators

### Activity Table View
- Complete station listing
- Traffic trends
- Wait times
- Sortable columns

## 🏗️ Project Structure

```
Metro crowd detector/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── advanced_analytics.py      # Analytics engine
│   ├── ml_prediction_engine.py    # ML predictions
│   ├── prediction_service.py      # Prediction service
│   ├── flow_analysis_engine.py    # Flow analysis
│   ├── revenue_engine.py          # Revenue analytics
│   ├── incident_engine.py         # Incident management
│   ├── ai_assistant_engine.py     # AI assistant
│   └── requirements.txt           # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.jsx               # Main React component
    │   ├── main.jsx              # React entry point
    │   └── index.css             # Global styles
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## 🎨 Station Lines

- **Red Line**: Miyapur ↔ LB Nagar (12 stations)
- **Green Line**: Nagole ↔ JNTU (11 stations)
- **Blue Line**: Raidurg ↔ Hitech City corridor (4 stations)

## 📈 Traffic Classification

**Station Traffic Levels:**
- LOW: < 100 passengers
- MEDIUM: 100-299 passengers
- HIGH: 300-399 passengers
- PEAK: ≥ 400 passengers

**Train Rush Levels:**
- Low Rush: < 40% occupied
- Moderate Rush: 40-70% occupied
- High Rush: > 70% occupied

## 🔧 Development

**Backend Development:**
```bash
# Auto-reload on code changes
uvicorn main:app --reload
```

**Frontend Development:**
```bash
# Vite hot module replacement
npm run dev
```

## 🌟 Key Highlights

- **27 Metro Stations** with real-time monitoring
- **Live Train Tracking** with seat availability
- **ML-Powered Predictions** using ensemble methods
- **Network Flow Analysis** with graph algorithms
- **Anomaly Detection** using statistical methods
- **Premium UI/UX** with Tailwind CSS

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Built with ❤️ for Hyderabad Metro commuters.

---

**HydroFlow 1.0** - Making metro travel smarter, one prediction at a time.

import { useState, useEffect } from 'react'
import { Train, Users, Activity, TrendingUp, AlertCircle, MapPin, Radio } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
    const [stationsData, setStationsData] = useState([])
    const [trainsData, setTrainsData] = useState([])
    const [summary, setSummary] = useState({})
    const [loading, setLoading] = useState(true)
    const [currentView, setCurrentView] = useState('map')

    useEffect(() => {
        fetchData()
        const interval = setInterval(fetchData, 5000)
        return () => clearInterval(interval)
    }, [])

    const fetchData = async () => {
        try {
            const [statusRes, trainsRes] = await Promise.all([
                fetch(`${API_URL}/status`),
                fetch(`${API_URL}/trains`)
            ])

            const statusData = await statusRes.json()
            const trainsDataRes = await trainsRes.json()

            setStationsData(statusData.stations || [])
            setSummary(statusData.summary || {})
            setTrainsData(trainsDataRes.trains || [])
            setLoading(false)
        } catch (error) {
            console.error('Error fetching data:', error)
            setLoading(false)
        }
    }

    const getStatusColor = (status) => {
        switch (status) {
            case 'LOW': return 'bg-green-500'
            case 'MEDIUM': return 'bg-amber-500'
            case 'HIGH': return 'bg-orange-500'
            case 'PEAK': return 'bg-red-600'
            default: return 'bg-gray-500'
        }
    }

    const getRushColor = (rushLevel) => {
        if (rushLevel === 'Low Rush') return 'text-green-400'
        if (rushLevel === 'Moderate Rush') return 'text-amber-400'
        return 'text-red-400'
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
                <div className="text-white text-2xl">Loading HydroFlow...</div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
            {/* Header - Mobile Responsive */}
            <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-3 sm:px-4 py-3 sm:py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2 sm:space-x-3">
                            <Train className="w-6 h-6 sm:w-8 sm:h-8 text-blue-400 flex-shrink-0" />
                            <div>
                                <h1 className="text-lg sm:text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                                    HydroFlow 1.0
                                </h1>
                                <p className="text-xs sm:text-sm text-slate-400 hidden sm:block">Metro Crowd Detection System</p>
                            </div>
                        </div>

                        {/* View Tabs - Responsive */}
                        <div className="flex space-x-1 sm:space-x-2">
                            {['map', 'dashboard', 'activity'].map(view => (
                                <button
                                    key={view}
                                    onClick={() => setCurrentView(view)}
                                    className={`px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg transition-all text-xs sm:text-base touch-manipulation ${currentView === view
                                        ? 'bg-blue-500 text-white'
                                        : 'bg-slate-700/50 text-slate-300 active:bg-slate-700'
                                        }`}
                                >
                                    <span className="hidden sm:inline">{view.charAt(0).toUpperCase() + view.slice(1)}</span>
                                    <span className="sm:hidden">{view.charAt(0).toUpperCase()}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-3 sm:px-4 py-4 sm:py-6">
                {/* Stats Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-4 mb-4 sm:mb-6">
                    <StatCard
                        icon={<Users className="w-6 h-6" />}
                        title="Total Passengers"
                        value={summary.totalPassengers?.toLocaleString() || '0'}
                        color="blue"
                    />
                    <StatCard
                        icon={<Train className="w-6 h-6" />}
                        title="Active Trains"
                        value={trainsData.length}
                        color="green"
                    />
                    <StatCard
                        icon={<AlertCircle className="w-6 h-6" />}
                        title="Peak Stations"
                        value={summary.peakStations || 0}
                        color="red"
                    />
                    <StatCard
                        icon={<Activity className="w-6 h-6" />}
                        title="Avg Wait Time"
                        value={`${summary.averageWaitTime || 0} min`}
                        color="amber"
                    />
                </div>

                {/* Main Views */}
                {currentView === 'map' && (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
                        {/* Network Map */}
                        <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-slate-700 p-3 sm:p-6">
                            <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 flex items-center">
                                <MapPin className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-blue-400" />
                                Network Map
                            </h2>
                            <NetworkMap stations={stationsData} trains={trainsData} />
                        </div>

                        {/* Station List - Mobile Responsive */}
                        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-slate-700 p-3 sm:p-6">
                            <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Stations</h2>
                            <div className="space-y-2 max-h-[400px] sm:max-h-[600px] overflow-y-auto">
                                {stationsData.map(station => (
                                    <div
                                        key={station.id}
                                        className="bg-slate-700/30 rounded-lg p-2.5 sm:p-3 active:bg-slate-700/50 transition-all touch-manipulation"
                                    >
                                        <div className="flex items-center justify-between mb-1">
                                            <span className="font-medium text-xs sm:text-sm truncate pr-2">{station.name}</span>
                                            <span className={`px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-semibold ${getStatusColor(station.status)} text-white flex-shrink-0`}>
                                                {station.status}
                                            </span>
                                        </div>
                                        <div className="flex items-center justify-between text-xs text-slate-400">
                                            <span>{station.passengers} passengers</span>
                                            <span className={`capitalize text-xs ${station.trend === 'increasing' ? 'text-red-400' :
                                                station.trend === 'decreasing' ? 'text-green-400' :
                                                    'text-slate-400'
                                                }`}>
                                                {station.trend === 'increasing' ? '↑' :
                                                    station.trend === 'decreasing' ? '↓' : '→'} <span className="hidden sm:inline">{station.trend}</span>
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {currentView === 'dashboard' && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
                        {/* Train Status - Mobile Responsive */}
                        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-slate-700 p-3 sm:p-6">
                            <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 flex items-center">
                                <Train className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-blue-400" />
                                Train Status
                            </h2>
                            <div className="space-y-2 sm:space-y-3">
                                {trainsData.slice(0, 8).map(train => (
                                    <div key={train.id} className="bg-slate-700/30 rounded-lg p-3 sm:p-4 touch-manipulation">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="font-semibold text-sm sm:text-base">{train.id}</span>
                                            <span className={`text-xs sm:text-sm font-medium ${getRushColor(train.seat_rush_level)}`}>
                                                {train.seat_rush_level}
                                            </span>
                                        </div>
                                        <div className="space-y-1 text-xs sm:text-sm text-slate-400">
                                            <div className="flex justify-between">
                                                <span>Occupancy:</span>
                                                <span className="text-white text-xs sm:text-sm">{train.current_occupancy}/{train.total_capacity} ({train.occupancy_percent}%)</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span>Available Seats:</span>
                                                <span className="text-white text-xs sm:text-sm">{train.available_seats}</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span>Next Station:</span>
                                                <span className="text-white text-xs sm:text-sm truncate ml-2">{train.nextStation}</span>
                                            </div>
                                        </div>
                                        {/* Occupancy Bar */}
                                        <div className="mt-2 sm:mt-3 bg-slate-600/30 rounded-full h-1.5 sm:h-2 overflow-hidden">
                                            <div
                                                className={`h-full rounded-full transition-all ${train.occupancy_percent > 70 ? 'bg-red-500' :
                                                    train.occupancy_percent > 40 ? 'bg-amber-500' :
                                                        'bg-green-500'
                                                    }`}
                                                style={{ width: `${train.occupancy_percent}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Peak Stations - Mobile Responsive */}
                        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-slate-700 p-3 sm:p-6">
                            <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 flex items-center">
                                <TrendingUp className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-red-400" />
                                Peak Stations
                            </h2>
                            <div className="space-y-2 sm:space-y-3">
                                {stationsData
                                    .filter(s => s.status === 'HIGH' || s.status === 'PEAK')
                                    .slice(0, 10)
                                    .map(station => (
                                        <div key={station.id} className="bg-gradient-to-r from-red-500/10 to-orange-500/10 rounded-lg p-3 sm:p-4 border border-red-500/20 touch-manipulation">
                                            <div className="flex items-center justify-between mb-2">
                                                <span className="font-semibold text-sm sm:text-base truncate pr-2">{station.name}</span>
                                                <span className={`px-2 sm:px-3 py-0.5 sm:py-1 rounded-full text-xs font-bold ${getStatusColor(station.status)} text-white flex-shrink-0`}>
                                                    {station.status}
                                                </span>
                                            </div>
                                            <div className="text-xs sm:text-sm text-slate-400 space-y-0.5">
                                                <div className="flex justify-between">
                                                    <span>Passengers:</span>
                                                    <span className="text-white font-semibold">{station.passengers}</span>
                                                </div>
                                                <div className="flex justify-between">
                                                    <span>Wait Time:</span>
                                                    <span className="text-white">{station.waitTime} min</span>
                                                </div>
                                                <div className="flex justify-between">
                                                    <span>Line:</span>
                                                    <span className={`font-semibold ${station.line === 'red' ? 'text-metro-red' :
                                                        station.line === 'green' ? 'text-metro-green' :
                                                            'text-metro-blue'
                                                        }`}>
                                                        {station.line.toUpperCase()}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                            </div>
                        </div>
                    </div>
                )}

                {currentView === 'activity' && (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-slate-700 overflow-hidden">
                        <div className="p-3 sm:p-6">
                            <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 flex items-center">
                                <Activity className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-blue-400" />
                                Network Activity
                            </h2>
                        </div>
                        <div className="overflow-x-auto -mx-px">
                            <table className="w-full min-w-[640px]">
                                <thead className="bg-slate-700/50">
                                    <tr>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Station</th>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Line</th>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Status</th>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Passengers</th>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Trend</th>
                                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-semibold uppercase tracking-wider">Wait Time</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-700">
                                    {stationsData.map((station, idx) => (
                                        <tr key={station.id} className={idx % 2 === 0 ? 'bg-slate-800/30' : 'bg-slate-800/10'}>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap font-medium text-xs sm:text-sm">{station.name}</td>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
                                                <span className={`px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-semibold ${station.line === 'red' ? 'bg-metro-red/20 text-metro-red' :
                                                    station.line === 'green' ? 'bg-metro-green/20 text-metro-green' :
                                                        'bg-metro-blue/20 text-metro-blue'
                                                    }`}>
                                                    {station.line.toUpperCase()}
                                                </span>
                                            </td>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
                                                <span className={`px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-semibold ${getStatusColor(station.status)} text-white`}>
                                                    {station.status}
                                                </span>
                                            </td>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm">{station.passengers}</td>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap capitalize text-xs sm:text-sm">
                                                <span className={
                                                    station.trend === 'increasing' ? 'text-red-400' :
                                                        station.trend === 'decreasing' ? 'text-green-400' :
                                                            'text-slate-400'
                                                }>
                                                    {station.trend === 'increasing' ? '↑' :
                                                        station.trend === 'decreasing' ? '↓' : '→'} <span className="hidden sm:inline">{station.trend}</span>
                                                </span>
                                            </td>
                                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm">{station.waitTime} min</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </main>
        </div>
    )
}

function StatCard({ icon, title, value, color }) {
    const colors = {
        blue: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30',
        green: 'from-green-500/20 to-emerald-500/20 border-green-500/30',
        red: 'from-red-500/20 to-orange-500/20 border-red-500/30',
        amber: 'from-amber-500/20 to-yellow-500/20 border-amber-500/30'
    }

    return (
        <div className={`bg-gradient-to-br ${colors[color]} backdrop-blur-sm rounded-lg sm:rounded-xl border p-3 sm:p-6`}>
            <div className="flex flex-col sm:flex-row items-start sm:items-center sm:justify-between gap-2">
                <div className="flex-1 min-w-0">
                    <p className="text-slate-400 text-xs sm:text-sm mb-1 truncate">{title}</p>
                    <p className="text-xl sm:text-3xl font-bold truncate">{value}</p>
                </div>
                <div className={`text-${color}-400 self-end sm:self-auto`}>
                    <div className="w-4 h-4 sm:w-6 sm:h-6">{icon}</div>
                </div>
            </div>
        </div>
    )
}

function NetworkMap({ stations, trains }) {
    return (
        <div className="relative bg-slate-900/50 rounded-lg p-2 sm:p-4 md:p-8 min-h-[300px] sm:min-h-[400px] md:min-h-[600px] overflow-x-auto">
            <svg
                width="100%"
                height="auto"
                viewBox="0 0 700 600"
                className="mx-auto min-h-[300px] sm:min-h-[400px]"
                preserveAspectRatio="xMidYMid meet"
            >
                {/* Metro Lines */}
                {/* Red Line */}
                <path
                    d="M 50 30 L 250 150"
                    stroke="#EF4444"
                    strokeWidth="3"
                    fill="none"
                    opacity="0.5"
                />
                {/* Green Line */}
                <path
                    d="M 650 350 L 250 180"
                    stroke="#10B981"
                    strokeWidth="3"
                    fill="none"
                    opacity="0.5"
                />
                {/* Blue Line */}
                <path
                    d="M 100 200 L 250 230"
                    stroke="#3B82F6"
                    strokeWidth="3"
                    fill="none"
                    opacity="0.5"
                />

                {/* Stations */}
                {stations.map(station => {
                    const statusColor = {
                        'LOW': '#10B981',
                        'MEDIUM': '#F59E0B',
                        'HIGH': '#F97316',
                        'PEAK': '#EF4444'
                    }[station.status] || '#6B7280'

                    return (
                        <g key={station.id} className="cursor-pointer">
                            <circle
                                cx={station.x}
                                cy={station.y}
                                r={station.status === 'PEAK' ? 10 : 8}
                                fill={statusColor}
                                className={station.status === 'PEAK' ? 'animate-pulse-slow' : ''}
                            />
                            <text
                                x={station.x}
                                y={station.y - 15}
                                fontSize="9"
                                fill="white"
                                textAnchor="middle"
                                className="font-semibold select-none"
                                style={{ fontSize: 'clamp(7px, 1.5vw, 10px)' }}
                            >
                                {station.name.length > 15 ? station.name.substring(0, 12) + '...' : station.name}
                            </text>
                        </g>
                    )
                })}

                {/* Trains */}
                {trains.slice(0, 6).map((train, idx) => {
                    const trainColor = {
                        'red': '#EF4444',
                        'green': '#10B981',
                        'blue': '#3B82F6'
                    }[train.line] || '#6B7280'

                    const x = 100 + (idx * 100)
                    const y = 300 + (idx % 3) * 80

                    return (
                        <g key={train.id} className="cursor-pointer">
                            <rect
                                x={x}
                                y={y}
                                width="30"
                                height="15"
                                rx="3"
                                fill={trainColor}
                                className="animate-pulse"
                            />
                            <text
                                x={x + 15}
                                y={y + 11}
                                fontSize="8"
                                fill="white"
                                textAnchor="middle"
                                className="font-bold select-none"
                            >
                                {train.id.substring(1)}
                            </text>
                        </g>
                    )
                })}
            </svg>
        </div>
    )
}

export default App

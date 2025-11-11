import React, { useState, useEffect } from 'react';
import api from '../lib/api';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const WiFiLogsViewer = () => {
  const [wifiLogs, setWifiLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    event_type: '',
    device_name: '',
    ssid: '',
    limit: 100,
  });

  useEffect(() => {
    fetchLogs();
    fetchStats();
  }, [filters]);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.event_type) params.append('event_type', filters.event_type);
      if (filters.device_name) params.append('device_name', filters.device_name);
      if (filters.ssid) params.append('ssid', filters.ssid);
      params.append('limit', filters.limit);

      const response = await api.get(`/server-logs/wifi?${params.toString()}`);
      setWifiLogs(response.data);
    } catch (error) {
      console.error('Error fetching WiFi logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.get('/server-logs/wifi/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching WiFi stats:', error);
    }
  };

  const getEventColor = (eventType) => {
    const colors = {
      connect: 'bg-green-100 text-green-800',
      disconnect: 'bg-red-100 text-red-800',
      auth_failure: 'bg-purple-100 text-purple-800',
      signal_low: 'bg-yellow-100 text-yellow-800',
    };
    return colors[eventType] || 'bg-gray-100 text-gray-800';
  };

  const getEventIcon = (eventType) => {
    const icons = {
      connect: '✅',
      disconnect: '❌',
      auth_failure: '🔐',
      signal_low: '📶',
    };
    return icons[eventType] || '📡';
  };

  const getSignalStrength = (signal) => {
    if (signal >= -50) return { text: 'Excellent', color: 'text-green-600', bars: 5 };
    if (signal >= -60) return { text: 'Good', color: 'text-blue-600', bars: 4 };
    if (signal >= -70) return { text: 'Fair', color: 'text-yellow-600', bars: 3 };
    if (signal >= -80) return { text: 'Weak', color: 'text-orange-600', bars: 2 };
    return { text: 'Very Weak', color: 'text-red-600', bars: 1 };
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('fr-FR', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const eventsData = stats
    ? {
        labels: ['Connections', 'Disconnections', 'Auth Failures', 'Signal Issues'],
        datasets: [
          {
            data: [
              stats.connections,
              stats.disconnections,
              stats.auth_failures,
              stats.signal_issues,
            ],
            backgroundColor: [
              'rgba(34, 197, 94, 0.6)',
              'rgba(239, 68, 68, 0.6)',
              'rgba(168, 85, 247, 0.6)',
              'rgba(251, 191, 36, 0.6)',
            ],
            borderWidth: 1,
          },
        ],
      }
    : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">WiFi Network Logs</h1>
        <button
          onClick={() => {
            fetchLogs();
            fetchStats();
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-100 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Devices</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.active_devices}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-100 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Connections</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.connections}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-100 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Auth Failures</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.auth_failures}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-purple-100 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-purple-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Events</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.total_events}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chart and SSIDs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {eventsData && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Events Distribution</h2>
            <div className="h-64 flex items-center justify-center">
              <Pie data={eventsData} options={{ maintainAspectRatio: false }} />
            </div>
          </div>
        )}

        {stats && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Networks</h2>
            <div className="space-y-3">
              {stats.ssids.map((ssid, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">📡</span>
                    <div>
                      <p className="font-medium text-gray-900">{ssid}</p>
                      <p className="text-sm text-gray-500">2.4 GHz / 5 GHz</p>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-sm font-medium text-green-600">Active</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Event Type</label>
            <select
              value={filters.event_type}
              onChange={(e) => setFilters({ ...filters, event_type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              <option value="connect">Connect</option>
              <option value="disconnect">Disconnect</option>
              <option value="auth_failure">Auth Failure</option>
              <option value="signal_low">Signal Low</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Device Name</label>
            <input
              type="text"
              placeholder="iPhone-John"
              value={filters.device_name}
              onChange={(e) => setFilters({ ...filters, device_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">SSID</label>
            <select
              value={filters.ssid}
              onChange={(e) => setFilters({ ...filters, ssid: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              {stats?.ssids.map((ssid, index) => (
                <option key={index} value={ssid}>
                  {ssid}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Limit</label>
            <select
              value={filters.limit}
              onChange={(e) => setFilters({ ...filters, limit: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="50">50</option>
              <option value="100">100</option>
              <option value="500">500</option>
            </select>
          </div>
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent WiFi Events</h2>
        </div>
        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : wifiLogs.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No WiFi logs found</div>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Event
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Device
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    MAC Address
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    SSID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Signal
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    IP
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {wifiLogs.map((log) => {
                  const signalInfo = log.signal_strength
                    ? getSignalStrength(log.signal_strength)
                    : null;
                  return (
                    <tr key={log.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatTimestamp(log.timestamp)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEventColor(
                            log.event_type
                          )}`}
                        >
                          {getEventIcon(log.event_type)} {log.event_type.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {log.device_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                        {log.device_mac}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {log.ssid}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {signalInfo ? (
                          <div>
                            <span className={`font-medium ${signalInfo.color}`}>
                              {log.signal_strength} dBm
                            </span>
                            <p className="text-xs text-gray-500">{signalInfo.text}</p>
                          </div>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                        {log.device_ip || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default WiFiLogsViewer;

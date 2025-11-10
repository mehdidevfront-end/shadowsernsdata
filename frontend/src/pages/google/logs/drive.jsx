import { useState, useEffect } from 'react';
import LogViewer from '../../components/common/LogViewer';
import { CloudIcon, DocumentIcon, UsersIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

const DriveLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({
    total_storage: '0',
    used_storage: '0',
    file_count: 0,
    shared_files: 0,
    recent_activities: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch logs
        const logsResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/google-logs?service=drive`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        const logsData = await logsResponse.json();
        setLogs(logsData);

        // Fetch stats
        const statsResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/google-logs/drive/stats`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        const statsData = await statsResponse.json();
        setStats(statsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleFilter = async (filters) => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams({
        service: 'drive',
        ...(filters.user && { user: filters.user }),
        ...(filters.startDate && { start_date: filters.startDate }),
        ...(filters.endDate && { end_date: filters.endDate }),
        ...(filters.status && { status: filters.status })
      });

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/google-logs?${queryParams}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      const data = await response.json();
      setLogs(data);
    } catch (error) {
      console.error('Error filtering logs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Logs Google Drive</h1>
        <p className="text-gray-500 mt-1">Suivi des activités et utilisation du stockage</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-blue-100 rounded-full p-3">
              <CloudIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Stockage utilisé</p>
              <h3 className="text-xl font-bold">{stats.used_storage} / {stats.total_storage}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-green-100 rounded-full p-3">
              <DocumentIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Fichiers</p>
              <h3 className="text-xl font-bold">{stats.file_count}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-yellow-100 rounded-full p-3">
              <UsersIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Fichiers partagés</p>
              <h3 className="text-xl font-bold">{stats.shared_files}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-purple-100 rounded-full p-3">
              <ArrowPathIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Activités récentes</p>
              <h3 className="text-xl font-bold">{stats.recent_activities}</h3>
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-500 mt-4">Chargement des logs...</p>
        </div>
      ) : (
        <LogViewer
          logs={logs}
          title="Historique des activités Drive"
          onFilter={handleFilter}
          showServiceFilter={false}
        />
      )}
    </div>
  );
};

export default DriveLogsPage;
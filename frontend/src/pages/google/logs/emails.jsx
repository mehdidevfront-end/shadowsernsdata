import { useState, useEffect } from 'react';
import LogViewer from '../../components/common/LogViewer';
import { ChartBarIcon, EnvelopeIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

const EmailLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({
    total_sent: 0,
    total_received: 0,
    average_size: '0',
    top_senders: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch logs
        const logsResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/google-logs?service=email`,
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
          `${process.env.NEXT_PUBLIC_API_URL}/google-logs/email/stats`,
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
        service: 'email',
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
        <h1 className="text-2xl font-bold text-gray-900">Logs des Emails</h1>
        <p className="text-gray-500 mt-1">Suivi et analyse des activités email</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-blue-100 rounded-full p-3">
              <EnvelopeIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Emails envoyés</p>
              <h3 className="text-xl font-bold">{stats.total_sent}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-green-100 rounded-full p-3">
              <ChartBarIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Emails reçus</p>
              <h3 className="text-xl font-bold">{stats.total_received}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-yellow-100 rounded-full p-3">
              <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Taille moyenne</p>
              <h3 className="text-xl font-bold">{stats.average_size}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="bg-purple-100 rounded-full p-3">
              <CheckCircleIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Top expéditeurs</p>
              <h3 className="text-xl font-bold">{stats.top_senders?.length || 0}</h3>
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
          title="Historique des activités email"
          onFilter={handleFilter}
          showServiceFilter={false}
        />
      )}
    </div>
  );
};

export default EmailLogsPage;
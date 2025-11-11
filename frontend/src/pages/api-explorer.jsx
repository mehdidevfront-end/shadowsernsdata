import React, { useState } from 'react';
import Layout from '@/components/layout/Layout';
import api from '@/lib/api';

const endpoints = [
  { method: 'GET', path: '/health', label: 'Health' },
  { method: 'GET', path: '/compliance', label: 'Compliance' },
  { method: 'GET', path: '/finops', label: 'FinOps' },
  { method: 'GET', path: '/assets', label: 'Legacy Assets' },
  { method: 'GET', path: '/risks', label: 'Legacy Risks' },
  { method: 'GET', path: '/logs', label: 'Logs (placeholder)' },
  { method: 'GET', path: '/stats/', label: 'Stats' },
  { method: 'GET', path: '/api/assets/', label: 'Assets (DB)' },
  { method: 'GET', path: '/api/services/', label: 'Services (DB)' },
  { method: 'GET', path: '/api/ingest/events', label: 'Ingest Events' },
  { method: 'GET', path: '/google-logs/', label: 'Google Logs' },
  { method: 'GET', path: '/server-logs/server', label: 'Server Logs' },
  { method: 'GET', path: '/server-logs/wifi', label: 'WiFi Logs' },
];

const ApiExplorer = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const call = async (ept) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await api({ method: ept.method.toLowerCase(), url: ept.path });
      setResult(res.data);
    } catch (e) {
      setResult({ error: e?.message || 'Erreur' });
    } finally {
      setLoading(false);
    }
  };

  const downloadCsv = () => {
    window.location.href = (process.env.NEXT_PUBLIC_API_URL || '') + '/api/reports/export';
  };

  return (
    <Layout title="API Explorer">
      <div className="p-6 space-y-4">
        <div className="flex flex-wrap gap-2">
          {endpoints.map((e) => (
            <button
              key={e.path}
              onClick={() => call(e)}
              className="px-3 py-2 bg-gray-800 text-white rounded"
            >
              {e.method} {e.path}
            </button>
          ))}
          <button onClick={downloadCsv} className="px-3 py-2 bg-green-700 text-white rounded">
            Download CSV
          </button>
        </div>
        <div className="bg-white rounded shadow p-4 overflow-auto">
          {loading ? (
            'Chargement…'
          ) : (
            <pre className="text-xs">{JSON.stringify(result, null, 2)}</pre>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default ApiExplorer;

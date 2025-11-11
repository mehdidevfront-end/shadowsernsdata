import React, { useEffect, useState } from 'react';
import Layout from '@/components/layout/Layout';
import DataTable from '@/components/common/DataTable';
import api from '@/lib/api';

const IngestEventsPage = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.get('/api/ingest/events');
        setEvents(res.data || []);
      } catch (e) {
        setError(e?.message || 'Erreur');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    {
      key: 'timestamp',
      label: 'Horodatage',
      render: (r) => new Date(r.timestamp).toLocaleString(),
    },
    { key: 'ip', label: 'IP', sortable: true },
    { key: 'mac', label: 'MAC', sortable: true },
    { key: 'domain', label: 'Domaine', sortable: true },
    { key: 'device_id', label: 'Device ID' },
    { key: 'service_id', label: 'Service ID' },
  ];

  return (
    <Layout title="Événements d'ingestion">
      <div className="p-6 space-y-4">
        {loading && <div>Chargement…</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && <DataTable data={events} columns={columns} showActions={false} />}
      </div>
    </Layout>
  );
};

export default IngestEventsPage;

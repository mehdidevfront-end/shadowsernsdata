import React, { useEffect, useState } from 'react';
import Layout from '@/components/layout/Layout';
import DataTable from '@/components/common/DataTable';
import api from '@/lib/api';

const AssetsPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [assets, setAssets] = useState([]);

  const fetchAssets = async () => {
    try {
      setLoading(true);
      const res = await api.get('/api/assets/');
      setAssets(res.data || []);
    } catch (e) {
      setError(e?.message || 'Erreur de chargement');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'hostname', label: 'Hostname', sortable: true },
    { key: 'ip_address', label: 'IP', sortable: true },
    { key: 'mac_address', label: 'MAC', sortable: true },
    {
      key: 'created_at',
      label: 'Créé le',
      render: (row) => new Date(row.created_at).toLocaleString(),
    },
  ];

  return (
    <Layout title="Actifs (Devices)">
      <div className="p-6 space-y-4">
        {loading && <div>Chargement…</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && <DataTable data={assets} columns={columns} showActions={false} />}
      </div>
    </Layout>
  );
};

export default AssetsPage;

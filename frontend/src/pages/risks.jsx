import React, { useEffect, useState } from 'react';
import Layout from '@/components/layout/Layout';
import DataTable from '@/components/common/DataTable';
import api from '@/lib/api';

const RisksPage = () => {
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.get('/risks/');
        setRisks(res.data || []);
      } catch (e) {
        setError(e?.message || 'Erreur');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'title', label: 'Titre' },
    { key: 'severity', label: 'Sévérité' },
    { key: 'asset_id', label: 'Asset' },
    { key: 'description', label: 'Description' },
  ];

  return (
    <Layout title="Risques">
      <div className="p-6 space-y-4">
        {loading && <div>Chargement…</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && <DataTable data={risks} columns={columns} showActions={false} />}
      </div>
    </Layout>
  );
};

export default RisksPage;

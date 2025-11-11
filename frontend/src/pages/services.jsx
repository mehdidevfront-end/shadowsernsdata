import React, { useEffect, useState } from 'react';
import Layout from '@/components/layout/Layout';
import DataTable from '@/components/common/DataTable';
import api from '@/lib/api';

const ServicesPage = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const res = await api.get('/api/services/');
      setServices(res.data || []);
    } catch (e) {
      setError(e?.message || 'Erreur de chargement');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();
  }, []);

  const approve = async (svc) => {
    try {
      await api.post(`/api/services/${svc.id}/approve`);
      fetchServices();
    } catch (e) {
      alert('Erreur approval');
    }
  };

  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Nom', sortable: true },
    { key: 'domain', label: 'Domaine', sortable: true },
    { key: 'risk_score', label: 'Risque', sortable: true },
    { key: 'approved', label: 'Approuvé', render: (row) => (row.approved ? '✅' : '❌') },
    {
      key: 'created_at',
      label: 'Créé le',
      render: (row) => new Date(row.created_at).toLocaleString(),
    },
  ];

  return (
    <Layout title="Services">
      <div className="p-6 space-y-4">
        {loading && <div>Chargement…</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && (
          <DataTable
            data={services}
            columns={columns}
            showActions={true}
            onEdit={(svc) => approve(svc)}
            onDelete={null}
            addButtonLabel=""
          />
        )}
      </div>
    </Layout>
  );
};

export default ServicesPage;

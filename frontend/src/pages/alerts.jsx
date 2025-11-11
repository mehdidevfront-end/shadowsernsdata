import React, { useEffect, useMemo, useState } from 'react';
import Layout from '@/components/layout/Layout';
import api from '@/lib/api';

const AlertsPage = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get('/api/services/');
        setServices(res.data || []);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const alerts = useMemo(() => {
    // Définir une alerte pour les services non approuvés avec un score de risque >= 60
    return (services || []).filter((s) => !s.approved && (s.risk_score || 0) >= 60);
  }, [services]);

  return (
    <Layout title="Alertes">
      <div className="p-6 space-y-4">
        {loading && <div>Chargement…</div>}
        {!loading && alerts.length === 0 && <div>Aucune alerte critique.</div>}
        {!loading && alerts.length > 0 && (
          <div className="space-y-3">
            {alerts.map((a) => (
              <div key={a.id} className="border border-red-300 bg-red-50 text-red-800 p-4 rounded">
                Service non approuvé à risque élevé: <strong>{a.name}</strong> ({a.domain}) — score:{' '}
                {a.risk_score}
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default AlertsPage;

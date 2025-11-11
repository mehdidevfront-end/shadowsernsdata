import React, { useEffect, useState } from 'react';
import Layout from '@/components/layout/Layout';
import api from '@/lib/api';

const StatsPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get('/stats/');
        setStats(res.data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <Layout title="Statistiques API">
      <div className="p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        {loading && <div>Chargement…</div>}
        {!loading && stats && (
          <>
            {Object.entries(stats).map(([k, v]) => (
              <div key={k} className="bg-white rounded shadow p-4">
                <div className="text-gray-500 text-sm">{k}</div>
                <div className="text-2xl font-semibold">{String(v)}</div>
              </div>
            ))}
          </>
        )}
      </div>
    </Layout>
  );
};

export default StatsPage;

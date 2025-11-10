import { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  ExclamationTriangleIcon,
  UserGroupIcon,
  DocumentCheckIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('chart.js/auto'), { ssr: false });

const StatCard = ({ title, value, icon: Icon, trend }) => (
  <div className="bg-white p-6 rounded-lg shadow-sm">
    <div className="flex justify-between items-start">
      <div>
        <p className="text-gray-500 text-sm">{title}</p>
        <h3 className="text-2xl font-bold mt-1">{value}</h3>
        {trend && (
          <p className={`text-sm mt-1 ${trend > 0 ? 'text-green-500' : 'text-red-500'}`}>
            {trend > 0 ? '+' : ''}{trend}% vs mois dernier
          </p>
        )}
      </div>
      <Icon className="h-8 w-8 text-blue-500" />
    </div>
  </div>
);

const ProcessCard = ({ title, description, icon: Icon }) => (
  <div className="bg-white p-6 rounded-lg shadow-sm">
    <div className="flex items-center space-x-4">
      <div className="bg-blue-100 p-3 rounded-full">
        <Icon className="h-6 w-6 text-blue-600" />
      </div>
      <div>
        <h3 className="font-semibold text-lg">{title}</h3>
        <p className="text-gray-500 text-sm mt-1">{description}</p>
      </div>
    </div>
  </div>
);

const DashboardPage = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    shadowIT: 0,
    users: 0,
    compliance: 0,
    alerts: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/stats`);
        const data = await res.json();
        setStats(data);
      } catch (err) {
        console.error('Erreur lors du chargement des statistiques:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const processSteps = [
    {
      title: 'Collecte',
      description: 'Scan automatisé des services et applications utilisés',
      icon: ChartBarIcon,
    },
    {
      title: 'Normalisation',
      description: 'Standardisation des données collectées',
      icon: DocumentCheckIcon,
    },
    {
      title: 'Corrélation',
      description: 'Analyse et détection des patterns',
      icon: ArrowPathIcon,
    },
    {
      title: 'Restitution',
      description: 'Visualisation et rapports détaillés',
      icon: ChartBarIcon,
    },
  ];

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Vue d'ensemble</h1>
        <p className="text-gray-500 mt-1">Tableau de bord Shadow IT et activité utilisateurs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Shadow IT détectés"
          value={loading ? '...' : stats.shadowIT}
          icon={ExclamationTriangleIcon}
          trend={5}
        />
        <StatCard
          title="Utilisateurs actifs"
          value={loading ? '...' : stats.users}
          icon={UserGroupIcon}
          trend={-2}
        />
        <StatCard
          title="Score conformité"
          value={loading ? '...' : `${stats.compliance}%`}
          icon={DocumentCheckIcon}
          trend={3}
        />
        <StatCard
          title="Alertes actives"
          value={loading ? '...' : stats.alerts}
          icon={ExclamationTriangleIcon}
          trend={0}
        />
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <h2 className="text-xl font-semibold mb-6">Actions rapides</h2>
        <div className="flex space-x-4">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Lancer un scan
          </button>
          <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
            Générer un rapport
          </button>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-6">Fonctionnement technique</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {processSteps.map((step, i) => (
            <ProcessCard key={i} {...step} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
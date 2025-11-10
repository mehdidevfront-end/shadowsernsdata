import { useState } from 'react';
import DataTable from '../../components/common/DataTable';

const shadowITData = [
  {
    id: 1,
    application: 'Slack',
    department: 'Marketing',
    users: 15,
    detectedDate: '2025-11-01',
    risk: 'Medium',
    status: 'Active'
  },
  // ... autres détections
];

const columns = [
  { key: 'application', label: 'Application', sortable: true },
  { key: 'department', label: 'Département', sortable: true },
  { key: 'users', label: 'Utilisateurs', sortable: true },
  { key: 'detectedDate', label: 'Date de détection', sortable: true },
  { 
    key: 'risk', 
    label: 'Niveau de risque',
    sortable: true,
    render: (item) => {
      const colors = {
        Low: 'bg-green-100 text-green-800',
        Medium: 'bg-yellow-100 text-yellow-800',
        High: 'bg-red-100 text-red-800'
      };
      return (
        <span className={`px-2 py-1 rounded-full text-xs ${colors[item.risk]}`}>
          {item.risk}
        </span>
      );
    }
  },
  { 
    key: 'status', 
    label: 'Statut',
    sortable: true,
    render: (item) => (
      <span className={`px-2 py-1 rounded-full text-xs ${
        item.status === 'Active' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
      }`}>
        {item.status}
      </span>
    )
  },
];

const ShadowITPage = () => {
  const [detections, setDetections] = useState(shadowITData);

  const handleAddDetection = () => {
    // TODO: Implement add detection modal
    console.log('Add detection clicked');
  };

  const handleEditDetection = (detection) => {
    // TODO: Implement edit detection modal
    console.log('Edit detection:', detection);
  };

  const handleDeleteDetection = (detection) => {
    if (window.confirm(`Voulez-vous vraiment supprimer la détection de ${detection.application} ?`)) {
      setDetections(detections.filter(d => d.id !== detection.id));
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Détection Shadow IT</h1>
        <p className="text-gray-500 mt-1">Identification proactive des applications et services non autorisés</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Applications détectées</h3>
          <p className="text-3xl font-bold text-blue-600">47</p>
          <p className="text-sm text-gray-500 mt-1">+5 ce mois-ci</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Risque élevé</h3>
          <p className="text-3xl font-bold text-red-600">12</p>
          <p className="text-sm text-gray-500 mt-1">Nécessite attention</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Département le plus actif</h3>
          <p className="text-3xl font-bold text-green-600">Marketing</p>
          <p className="text-sm text-gray-500 mt-1">15 applications</p>
        </div>
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

      <DataTable
        data={detections}
        columns={columns}
        onAdd={handleAddDetection}
        onEdit={handleEditDetection}
        onDelete={handleDeleteDetection}
        addButtonLabel="Ajouter une détection"
      />
    </div>
  );
};

export default ShadowITPage;
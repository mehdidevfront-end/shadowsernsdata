import { useState } from 'react';
import DataTable from '../../components/common/DataTable';

const GoogleDrivePage = () => {
  const [files, setFiles] = useState([
    {
      id: 1,
      name: 'Rapport Q4 2025.pdf',
      owner: 'John Doe',
      shared: 'Équipe Marketing',
      lastModified: '2025-11-07',
      size: '2.4 MB'
    },
    // ... autres fichiers
  ]);

  const columns = [
    { key: 'name', label: 'Nom du fichier', sortable: true },
    { key: 'owner', label: 'Propriétaire', sortable: true },
    { key: 'shared', label: 'Partagé avec', sortable: true },
    { key: 'lastModified', label: 'Dernière modification', sortable: true },
    { key: 'size', label: 'Taille', sortable: true }
  ];

  const handleUpload = () => {
    // Implémenter la logique d'upload
    console.log('Upload clicked');
  };

  const handleEdit = (file) => {
    console.log('Edit file:', file);
  };

  const handleDelete = (file) => {
    if (window.confirm(`Voulez-vous vraiment supprimer ${file.name} ?`)) {
      setFiles(files.filter(f => f.id !== file.id));
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Google Drive</h1>
        <p className="text-gray-500 mt-1">Gestion des fichiers et documents partagés</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Espace utilisé</h3>
          <p className="text-3xl font-bold text-blue-600">75%</p>
          <p className="text-sm text-gray-500 mt-1">15 GB sur 20 GB</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Fichiers partagés</h3>
          <p className="text-3xl font-bold text-green-600">142</p>
          <p className="text-sm text-gray-500 mt-1">+12 cette semaine</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Collaboration</h3>
          <p className="text-3xl font-bold text-purple-600">23</p>
          <p className="text-sm text-gray-500 mt-1">Utilisateurs actifs</p>
        </div>
      </div>

      <DataTable
        data={files}
        columns={columns}
        onAdd={handleUpload}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonLabel="Uploader un fichier"
      />
    </div>
  );
};

export default GoogleDrivePage;
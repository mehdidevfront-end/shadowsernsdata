import { useState } from 'react';
import DataTable from '../../components/common/DataTable';

const EmailsPage = () => {
  const [emails, setEmails] = useState([
    {
      id: 1,
      subject: 'Réunion hebdomadaire',
      from: 'alice@company.com',
      to: ['team@company.com'],
      date: '2025-11-07 09:30',
      status: 'Sent'
    },
    // ... autres emails
  ]);

  const columns = [
    { key: 'subject', label: 'Objet', sortable: true },
    { key: 'from', label: 'De', sortable: true },
    { 
      key: 'to', 
      label: 'À',
      sortable: true,
      render: (item) => item.to.join(', ')
    },
    { key: 'date', label: 'Date', sortable: true },
    { 
      key: 'status', 
      label: 'Statut',
      sortable: true,
      render: (item) => (
        <span className={`px-2 py-1 rounded-full text-xs ${
          item.status === 'Sent' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
        }`}>
          {item.status}
        </span>
      )
    }
  ];

  const handleNewEmail = () => {
    // Implémenter la modal de nouvel email
    console.log('New email clicked');
  };

  const handleEdit = (email) => {
    console.log('Edit email:', email);
  };

  const handleDelete = (email) => {
    if (window.confirm(`Voulez-vous vraiment supprimer cet email ?`)) {
      setEmails(emails.filter(e => e.id !== email.id));
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Emails</h1>
        <p className="text-gray-500 mt-1">Gestion des emails professionnels</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Boîte de réception</h3>
          <p className="text-3xl font-bold text-blue-600">28</p>
          <p className="text-sm text-gray-500 mt-1">Non lus</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Envoyés</h3>
          <p className="text-3xl font-bold text-green-600">156</p>
          <p className="text-sm text-gray-500 mt-1">Cette semaine</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Spam</h3>
          <p className="text-3xl font-bold text-red-600">12</p>
          <p className="text-sm text-gray-500 mt-1">À vérifier</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Espace utilisé</h3>
          <p className="text-3xl font-bold text-purple-600">65%</p>
          <p className="text-sm text-gray-500 mt-1">9.8 GB / 15 GB</p>
        </div>
      </div>

      <DataTable
        data={emails}
        columns={columns}
        onAdd={handleNewEmail}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonLabel="Nouveau message"
      />
    </div>
  );
};

export default EmailsPage;
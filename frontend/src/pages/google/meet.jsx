import { useState } from 'react';
import DataTable from '../../components/common/DataTable';
import { VideoCameraIcon } from '@heroicons/react/24/outline';

const GoogleMeetPage = () => {
  const [meetings, setMeetings] = useState([
    {
      id: 1,
      title: 'Réunion équipe',
      organizer: 'John Doe',
      participants: ['Alice', 'Bob', 'Charlie'],
      date: '2025-11-07 14:00',
      duration: '1h',
      status: 'Scheduled'
    },
    // ... autres réunions
  ]);

  const columns = [
    { key: 'title', label: 'Titre', sortable: true },
    { key: 'organizer', label: 'Organisateur', sortable: true },
    { 
      key: 'participants', 
      label: 'Participants',
      sortable: false,
      render: (item) => `${item.participants.length} participants`
    },
    { key: 'date', label: 'Date et heure', sortable: true },
    { key: 'duration', label: 'Durée', sortable: true },
    { 
      key: 'status', 
      label: 'Statut',
      sortable: true,
      render: (item) => (
        <span className={`px-2 py-1 rounded-full text-xs ${
          item.status === 'In Progress' ? 'bg-green-100 text-green-800' :
          item.status === 'Scheduled' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {item.status}
        </span>
      )
    }
  ];

  const handleNewMeeting = () => {
    console.log('New meeting clicked');
  };

  const handleEdit = (meeting) => {
    console.log('Edit meeting:', meeting);
  };

  const handleDelete = (meeting) => {
    if (window.confirm(`Voulez-vous vraiment supprimer la réunion "${meeting.title}" ?`)) {
      setMeetings(meetings.filter(m => m.id !== meeting.id));
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Google Meet</h1>
        <p className="text-gray-500 mt-1">Gestion des visioconférences</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Réunions aujourd'hui</h3>
          <p className="text-3xl font-bold text-blue-600">5</p>
          <p className="text-sm text-gray-500 mt-1">2 en cours</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Temps total</h3>
          <p className="text-3xl font-bold text-green-600">12h</p>
          <p className="text-sm text-gray-500 mt-1">Cette semaine</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Participants</h3>
          <p className="text-3xl font-bold text-purple-600">47</p>
          <p className="text-sm text-gray-500 mt-1">En moyenne par réunion</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">Réunion rapide</h2>
            <p className="text-gray-500">Démarrer une réunion instantanée</p>
          </div>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
            <VideoCameraIcon className="h-5 w-5 mr-2" />
            Démarrer maintenant
          </button>
        </div>
      </div>

      <DataTable
        data={meetings}
        columns={columns}
        onAdd={handleNewMeeting}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonLabel="Planifier une réunion"
      />
    </div>
  );
};

export default GoogleMeetPage;
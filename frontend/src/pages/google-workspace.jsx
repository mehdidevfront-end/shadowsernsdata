import React from 'react';
import Layout from '../../components/layout/Layout';
import { useRouter } from 'next/router';

const GoogleWorkspacePage = () => {
  const router = useRouter();

  const services = [
    {
      name: 'Gmail',
      description: 'Logs des emails professionnels',
      icon: '📧',
      color: 'bg-red-500',
      path: '/google/emails',
    },
    {
      name: 'Google Drive',
      description: 'Activité de stockage et partage de fichiers',
      icon: '📁',
      color: 'bg-blue-500',
      path: '/google/drive',
    },
    {
      name: 'Google Docs',
      description: "Logs d'édition de documents",
      icon: '📄',
      color: 'bg-blue-600',
      path: '/google/docs',
    },
    {
      name: 'Google Sheets',
      description: 'Activité sur les feuilles de calcul',
      icon: '📊',
      color: 'bg-green-500',
      path: '/google/sheets',
    },
    {
      name: 'Google Meet',
      description: 'Logs des réunions et visioconférences',
      icon: '🎥',
      color: 'bg-yellow-500',
      path: '/google/meet',
    },
    {
      name: 'Google Slides',
      description: 'Logs des présentations',
      icon: '📽️',
      color: 'bg-orange-500',
      path: '/google/slides',
    },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Google Workspace Logs</h1>
          <p className="mt-2 text-gray-600">
            Surveillez et analysez l'activité de vos services Google Workspace
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service) => (
            <div
              key={service.name}
              onClick={() => router.push(service.path)}
              className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 cursor-pointer overflow-hidden"
            >
              <div className={`${service.color} h-2`}></div>
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <span className="text-4xl mr-4">{service.icon}</span>
                  <h2 className="text-xl font-semibold text-gray-900">{service.name}</h2>
                </div>
                <p className="text-gray-600">{service.description}</p>
                <div className="mt-4">
                  <button className="text-blue-600 hover:text-blue-800 font-medium flex items-center">
                    Voir les logs
                    <svg
                      className="ml-2 w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-blue-700">
                Les logs Google Workspace permettent de suivre toutes les activités des utilisateurs
                sur les services Google. Utilisez les filtres pour affiner votre recherche par
                utilisateur, date ou type d'action.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default GoogleWorkspacePage;

import { useState } from 'react';
import Layout from '../../components/layout/Layout';

export default function GoogleSheets() {
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Google Sheets</h1>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">
            Surveillance des activités Google Sheets
          </p>
          <div className="mt-6">
            <p className="text-gray-500">Logs et statistiques Google Sheets</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

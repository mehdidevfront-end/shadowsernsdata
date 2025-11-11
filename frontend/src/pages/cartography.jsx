import { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';

export default function Cartography() {
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Cartographie IT</h1>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">
            La cartographie IT permet de visualiser l'ensemble de votre infrastructure informatique.
          </p>
          <div className="mt-6 h-96 bg-gray-100 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Graphique de cartographie à venir</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

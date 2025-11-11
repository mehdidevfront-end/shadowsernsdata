import { useState } from 'react';
import Layout from '../../components/layout/Layout';

export default function GoogleEvents() {
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Google Calendar Events</h1>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">
            Surveillance des événements Google Calendar
          </p>
        </div>
      </div>
    </Layout>
  );
}
